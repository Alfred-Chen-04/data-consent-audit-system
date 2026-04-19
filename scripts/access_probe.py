"""Week 0 access feasibility probe.

For each URL in a CSV, headlessly loads the page and records:
  - http_status, load_time_ms, final_url (after redirects), page_title
  - banner_detected: does the DOM contain an obvious consent banner?
  - block_signal: CAPTCHA / Cloudflare / 403 / timeout markers
  - screenshot saved to data/captures/access_probe/<slug>.png

Intended to be a single evening's run. No LLM/VLM calls, no database —
just Playwright + CSV in, CSV out.

Usage:
    uv run python scripts/access_probe.py \\
        --sites data/sites.csv \\
        --out data/access_probe_v0.csv \\
        --concurrency 4
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeout,
    async_playwright,
)

DEFAULT_TIMEOUT_MS = 30_000
DEFAULT_CONCURRENCY = 4

# CSS selectors commonly used by consent banners. Deliberately broad — this is
# a feasibility probe, not a classifier. False positives are fine here.
# Order matters: specific CMP vendor IDs first (most reliable), generic last.
BANNER_SELECTORS = [
    # Common CMP vendors (specific IDs — very reliable signal)
    "#onetrust-banner-sdk",
    "#onetrust-consent-sdk",
    "#CybotCookiebotDialog",
    "#didomi-popup",
    "#didomi-notice",
    "#truste-consent-track",
    "#qc-cmp2-container",
    ".qc-cmp2-container",
    "#usercentrics-root",
    "#cmpbox",
    "#sp_message_container_",
    '[id^="sp_message_container"]',
    # Generic patterns
    '[id*="cookie" i]',
    '[class*="cookie-banner" i]',
    '[class*="cookie-notice" i]',
    '[class*="cookie-consent" i]',
    '[id*="consent" i]',
    '[class*="consent-banner" i]',
    '[class*="consent-notice" i]',
    '[id*="gdpr" i]',
    '[class*="gdpr" i]',
    '[aria-label*="cookie" i]',
    '[aria-label*="consent" i]',
    '[data-testid*="cookie" i]',
    '[data-testid*="consent" i]',
]

# Content signatures that indicate an anti-bot wall rather than the real site.
BLOCK_PATTERNS = {
    "cloudflare_challenge": re.compile(
        r"(checking your browser|cf[-_]chl[-_]|cloudflare|ray id)", re.IGNORECASE
    ),
    "captcha": re.compile(r"(captcha|hcaptcha|recaptcha|are you a human)", re.IGNORECASE),
    "access_denied": re.compile(r"(access denied|forbidden|blocked|403)", re.IGNORECASE),
}


@dataclass
class ProbeResult:
    url: str
    final_url: str = ""
    http_status: int | None = None
    load_time_ms: int | None = None
    page_title: str = ""
    banner_detected: bool = False
    banner_selector_hit: str = ""
    block_signal: str = ""  # empty if clean; else name of the matched pattern
    screenshot_path: str = ""
    error: str = ""
    notes: list[str] = field(default_factory=list)


def slugify(url: str) -> str:
    host = urlparse(url).netloc or url
    return re.sub(r"[^a-z0-9]+", "_", host.lower()).strip("_") or "site"


async def probe_one(
    url: str,
    context,  # playwright BrowserContext
    screenshot_dir: Path,
    timeout_ms: int,
) -> ProbeResult:
    result = ProbeResult(url=url)
    page = await context.new_page()
    start = time.perf_counter()
    try:
        response = await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        result.load_time_ms = int((time.perf_counter() - start) * 1000)
        result.final_url = page.url
        if response is not None:
            result.http_status = response.status

        # Give dynamic banners a beat to render. Most CMP SDKs lazy-inject
        # banners after the main page is interactive, so we wait for either
        # networkidle or a fixed grace period.
        try:
            await page.wait_for_load_state("networkidle", timeout=8_000)
        except PlaywrightTimeout:
            result.notes.append("networkidle timeout (likely ok)")
        await page.wait_for_timeout(2_000)  # grace for late-injected CMPs

        result.page_title = (await page.title()) or ""

        body_text = ""
        try:
            body_text = await page.inner_text("body", timeout=5_000)
        except (PlaywrightTimeout, PlaywrightError):
            result.notes.append("could not read body text")

        for name, pattern in BLOCK_PATTERNS.items():
            if pattern.search(body_text):
                result.block_signal = name
                break

        # Check main frame + all iframes (many CMPs like TrustArc, Quantcast
        # render inside an iframe).
        frames = [page.main_frame, *page.frames]
        for selector in BANNER_SELECTORS:
            hit = False
            for frame in frames:
                try:
                    locator = frame.locator(selector).first
                    if await locator.count() > 0:
                        visible = False
                        try:
                            visible = await locator.is_visible()
                        except (PlaywrightTimeout, PlaywrightError):
                            pass
                        # Even if not visible (e.g. display:none until consent flow starts),
                        # presence of a vendor-specific CMP ID is a strong signal.
                        if visible or selector.startswith("#") or selector.startswith('[id^='):
                            result.banner_detected = True
                            result.banner_selector_hit = selector
                            if frame is not page.main_frame:
                                result.notes.append("banner in iframe")
                            hit = True
                            break
                except (PlaywrightTimeout, PlaywrightError):
                    continue
            if hit:
                break

        shot_path = screenshot_dir / f"{slugify(url)}.png"
        try:
            await page.screenshot(path=str(shot_path), full_page=False, timeout=10_000)
            result.screenshot_path = str(shot_path.relative_to(screenshot_dir.parent.parent))
        except (PlaywrightTimeout, PlaywrightError) as e:
            result.notes.append(f"screenshot failed: {e}")

    except PlaywrightTimeout:
        result.error = "timeout"
        result.load_time_ms = int((time.perf_counter() - start) * 1000)
    except PlaywrightError as e:
        result.error = f"playwright_error: {e}".splitlines()[0][:200]
    finally:
        await page.close()

    return result


async def run(sites: list[str], out_csv: Path, concurrency: int, timeout_ms: int) -> None:
    screenshot_dir = out_csv.parent / "captures" / "access_probe"
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 900},
            locale="en-US",
        )

        sem = asyncio.Semaphore(concurrency)
        results: list[ProbeResult] = []

        async def bounded(u: str, idx: int, total: int) -> None:
            async with sem:
                print(f"[{idx:>3}/{total}] {u}", file=sys.stderr, flush=True)
                r = await probe_one(u, context, screenshot_dir, timeout_ms)
                results.append(r)

        await asyncio.gather(
            *(bounded(u, i + 1, len(sites)) for i, u in enumerate(sites))
        )

        await context.close()
        await browser.close()

    fieldnames = list(asdict(ProbeResult(url="")).keys())
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = asdict(r)
            row["notes"] = "; ".join(r.notes)
            writer.writerow(row)

    total = len(results)
    loaded = sum(1 for r in results if r.http_status and r.http_status < 400 and not r.error)
    banner = sum(1 for r in results if r.banner_detected)
    blocked = sum(1 for r in results if r.block_signal or r.error)
    print(
        f"\nDone. total={total}  loaded={loaded}  banner_detected={banner}  blocked_or_error={blocked}",
        file=sys.stderr,
    )
    print(f"Results: {out_csv}", file=sys.stderr)
    print(f"Screenshots: {screenshot_dir}", file=sys.stderr)


def load_sites(path: Path) -> list[str]:
    urls: list[str] = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = (row.get("url") or "").strip()
            if not url or url.startswith("#"):
                continue
            urls.append(url)
    return urls


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sites", type=Path, default=Path("data/sites.csv"))
    ap.add_argument("--out", type=Path, default=Path("data/access_probe_v0.csv"))
    ap.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    ap.add_argument("--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS)
    args = ap.parse_args()

    if not args.sites.exists():
        print(f"sites file not found: {args.sites}", file=sys.stderr)
        sys.exit(2)

    sites = load_sites(args.sites)
    if not sites:
        print(f"no URLs in {args.sites} (header-only or all commented out)", file=sys.stderr)
        sys.exit(2)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(run(sites, args.out, args.concurrency, args.timeout_ms))


if __name__ == "__main__":
    main()
