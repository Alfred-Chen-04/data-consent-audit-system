"""Access-feasibility probe for candidate consent-audit sites."""

from __future__ import annotations

import asyncio
import csv
import re
import sys
import time
from contextlib import suppress
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import BrowserContext, async_playwright
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeout

from consent_audit.site_list import validate_site_list

DEFAULT_TIMEOUT_MS = 30_000
DEFAULT_CONCURRENCY = 4

BANNER_SELECTORS = [
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
    block_signal: str = ""
    screenshot_path: str = ""
    error: str = ""
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AccessProbeSummary:
    total: int
    loaded: int
    banner_detected: int
    blocked_or_error: int
    out_csv: Path
    screenshot_dir: Path


def slugify(url: str) -> str:
    host = urlparse(url).netloc or url
    return re.sub(r"[^a-z0-9]+", "_", host.lower()).strip("_") or "site"


async def probe_one(
    url: str,
    context: BrowserContext,
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
            result.block_signal = _status_block_signal(response.status)

        try:
            await page.wait_for_load_state("networkidle", timeout=8_000)
        except PlaywrightTimeout:
            result.notes.append("networkidle timeout (likely ok)")
        await page.wait_for_timeout(2_000)

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

        frames = [page.main_frame, *page.frames]
        for selector in BANNER_SELECTORS:
            hit = False
            for frame in frames:
                try:
                    locator = frame.locator(selector).first
                    if await locator.count() > 0:
                        visible = False
                        with suppress(PlaywrightTimeout, PlaywrightError):
                            visible = await locator.is_visible()
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
        except (PlaywrightTimeout, PlaywrightError) as exc:
            result.notes.append(f"screenshot failed: {exc}")

    except PlaywrightTimeout:
        result.error = "timeout"
        result.load_time_ms = int((time.perf_counter() - start) * 1000)
    except PlaywrightError as exc:
        result.error = f"playwright_error: {exc}".splitlines()[0][:200]
    finally:
        await page.close()

    return result


def _status_block_signal(status: int | None) -> str:
    if status is None or status < 400:
        return ""
    return f"http_{status}"


async def run_access_probe_from_csv(
    sites_csv: Path,
    out_csv: Path,
    *,
    concurrency: int = DEFAULT_CONCURRENCY,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
) -> AccessProbeSummary:
    if not sites_csv.exists():
        raise ValueError(f"sites file not found: {sites_csv}")

    validation = validate_site_list(sites_csv)
    if validation.errors:
        issue_codes = ", ".join(issue.code for issue in validation.errors)
        raise ValueError(f"site list validation failed before access probe: {issue_codes}")

    sites = load_probe_sites(sites_csv)
    if not sites:
        raise ValueError(f"no URLs in {sites_csv} (header-only or all commented out)")

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    return await run_access_probe(sites, out_csv, concurrency, timeout_ms)


async def run_access_probe(
    sites: list[str],
    out_csv: Path,
    concurrency: int,
    timeout_ms: int,
) -> AccessProbeSummary:
    screenshot_dir = out_csv.parent / "captures" / "access_probe"
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
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

        async def bounded(url: str, index: int, total: int) -> None:
            async with sem:
                print(f"[{index:>3}/{total}] {url}", file=sys.stderr, flush=True)
                result = await probe_one(url, context, screenshot_dir, timeout_ms)
                results.append(result)

        await asyncio.gather(
            *(bounded(url, index + 1, len(sites)) for index, url in enumerate(sites))
        )

        await context.close()
        await browser.close()

    fieldnames = list(asdict(ProbeResult(url="")).keys())
    with out_csv.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            row = asdict(result)
            row["notes"] = "; ".join(result.notes)
            writer.writerow(row)

    total = len(results)
    loaded = sum(
        1 for result in results if result.http_status and result.http_status < 400 and not result.error
    )
    banner_detected = sum(1 for result in results if result.banner_detected)
    blocked_or_error = sum(1 for result in results if result.block_signal or result.error)
    return AccessProbeSummary(
        total=total,
        loaded=loaded,
        banner_detected=banner_detected,
        blocked_or_error=blocked_or_error,
        out_csv=out_csv,
        screenshot_dir=screenshot_dir,
    )


def load_probe_sites(path: Path) -> list[str]:
    urls: list[str] = []
    with path.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            url = (row.get("url") or "").strip()
            if not url or url.startswith("#"):
                continue
            urls.append(url)
    return urls


def format_access_probe_summary(summary: AccessProbeSummary) -> str:
    return (
        "Completed access probe "
        f"(total={summary.total}, "
        f"loaded={summary.loaded}, "
        f"banner_detected={summary.banner_detected}, "
        f"blocked_or_error={summary.blocked_or_error})\n"
        f"Results: {summary.out_csv}\n"
        f"Screenshots: {summary.screenshot_dir}"
    )
