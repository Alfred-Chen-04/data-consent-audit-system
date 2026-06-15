"""Browser agent: Playwright + VLM loop that walks the four consent pathways.

Flow (per site):
    1. Launch Chromium with a fresh user-data-dir (no stale cookies).
    2. Navigate to URL, wait for consent banner to render.
    3. Take first-layer screenshot + DOM snapshot.
    4. Ask VLM to locate candidate elements for each Pathway (Accept/Reject/Customize/Dismiss).
    5. For each Pathway: attempt click → observe outcome → record PathOutcome.
    6. If Customize opens a second-layer panel: capture it too.
    7. Compute fingerprint, assemble CaptureBundle.

See AGENTS.md §2 principle 3 — dynamic navigation is required, not optional.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from re import search
from typing import Any
from urllib.parse import urlparse

from pydantic import HttpUrl

from consent_audit.capture.fingerprint import compute_fingerprint
from consent_audit.models import (
    CaptureBundle,
    ElementRef,
    EventLogRef,
    LayerSnapshot,
    PathOutcome,
    Pathway,
)

_CONSENT_RENDER_WAIT_MS = 3_000


@dataclass(frozen=True)
class CandidateElement:
    selector: str
    visible_text: str
    context_text: str = ""
    in_initial_viewport: bool = True


@dataclass(frozen=True)
class DomSnapshot:
    html: str
    warnings: list[str]


async def capture_site(url: HttpUrl, *, timeout_seconds: int = 180) -> CaptureBundle:
    """Perform one dynamic capture of a site's consent interface.

    Returns a complete CaptureBundle. On unrecoverable errors (CAPTCHA walls,
    timeouts), raises CaptureFailedError with a reason that the orchestrator can log.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:  # pragma: no cover - depends on optional runtime install
        raise CaptureFailedError("Playwright is not installed in this environment") from exc

    timeout_ms = timeout_seconds * 1000
    captured_at = datetime.now(UTC)
    timestamp = captured_at.strftime("%Y%m%d_%H%M%S")
    capture_dir = Path("data") / "captures" / "sites" / f"{_slug(url)}_{timestamp}"
    capture_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = capture_dir / "layer1.png"
    dom_path = capture_dir / "layer1.html"

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            locale="en-US",
            viewport={"width": 1440, "height": 900},
        )
        page = await context.new_page()
        try:
            await page.goto(str(url), wait_until="domcontentloaded", timeout=timeout_ms)
            await page.wait_for_timeout(_CONSENT_RENDER_WAIT_MS)
            dom_snapshot = await snapshot_dom_html(page)
            dom_html = dom_snapshot.html
            capture_warnings = dom_snapshot.warnings
            visible_text = await _body_text(page)
            await page.screenshot(path=str(screenshot_path), full_page=False, timeout=10_000)
            dom_path.write_text(dom_html, encoding="utf-8")
            candidates = await _collect_candidates(page)
            succeeded_pathways = await _attempt_pathway_clicks(
                browser, str(url), candidates, timeout_ms
            )
        except Exception as exc:  # pragma: no cover - requires browser integration
            raise CaptureFailedError(str(exc)) from exc
        finally:
            await context.close()
            await browser.close()

    fingerprint = compute_fingerprint(
        dom_html=dom_html,
        screenshot_path=screenshot_path,
        visible_text=visible_text,
    )
    path_outcomes = build_path_outcomes(candidates, succeeded_pathways=succeeded_pathways)
    return CaptureBundle(
        url=url,
        captured_at=captured_at,
        layers=[
            LayerSnapshot(
                layer_index=1,
                screenshot_ref=str(screenshot_path),
                dom_snapshot_ref=str(dom_path),
                visible_text=visible_text,
            )
        ],
        path_outcomes=path_outcomes,
        fingerprint=fingerprint,
        event_log=build_event_log(path_outcomes),
        capture_warnings=capture_warnings,
    )


def classify_pathway_label(label: str) -> Pathway | None:
    normalized = " ".join(label.lower().split())
    if not normalized:
        return None

    if search(r"\b(accept|agree|allow|yes|ok)\b", normalized):
        return Pathway.ACCEPT
    if search(r"\b(reject|decline|deny|refuse|disagree)\b", normalized) or "no, i" in normalized:
        return Pathway.REJECT
    if search(r"\b(close|dismiss|continue without|necessary only)\b", normalized) or normalized == "x":
        return Pathway.DISMISS
    if "preference center" in normalized and not search(
        r"\b(confirm|save|manage|settings?|options?|choices?)\b",
        normalized,
    ):
        return None
    if search(
        r"\b(customi[sz]e|manage|settings?|preferences?|options?|confirm my choices|save my choices)\b",
        normalized,
    ):
        return Pathway.CUSTOMIZE
    return None


def is_consent_candidate(candidate: CandidateElement) -> bool:
    """Return whether a candidate is plausibly part of a consent interface."""

    if not candidate.in_initial_viewport:
        return False

    if classify_pathway_label(candidate.visible_text) is None:
        return False

    label = _normalize(candidate.visible_text)
    context = _normalize(candidate.context_text)
    combined = f"{label} {context}".strip()

    if _has_consent_terms(combined):
        return True

    return bool(
        search(
            r"\b(accept all|reject all|manage options|manage preferences|privacy choices)\b",
            combined,
        )
    )


def filter_consent_candidates(candidates: list[CandidateElement]) -> list[CandidateElement]:
    return [candidate for candidate in candidates if is_consent_candidate(candidate)]


async def snapshot_dom_html(page: Any) -> DomSnapshot:
    try:
        return DomSnapshot(html=str(await page.content()), warnings=[])
    except Exception as exc:
        content_error = str(exc)
        try:
            fallback_html = await page.evaluate(
                """() => document.documentElement
                    ? document.documentElement.outerHTML
                    : ''
                """
            )
        except Exception as fallback_exc:
            raise RuntimeError(
                f"page.content failed ({content_error}); DOM fallback failed ({fallback_exc})"
            ) from exc
        return DomSnapshot(
            html=str(fallback_html or ""),
            warnings=[
                "page.content failed; used document.documentElement.outerHTML fallback: "
                f"{content_error}"
            ],
        )


def build_path_outcomes(
    candidates: list[CandidateElement],
    *,
    succeeded_pathways: set[Pathway] | None = None,
) -> dict[Pathway, PathOutcome]:
    outcomes: dict[Pathway, PathOutcome] = {}
    for pathway in Pathway:
        match = next(
            (
                candidate
                for candidate in candidates
                if classify_pathway_label(candidate.visible_text) == pathway
            ),
            None,
        )
        if match is None:
            outcomes[pathway] = PathOutcome(
                pathway=pathway,
                attempted=False,
                succeeded=False,
                click_depth=0,
                failure_reason="no_candidate_detected",
            )
            continue

        succeeded = succeeded_pathways is None or pathway in succeeded_pathways
        outcomes[pathway] = PathOutcome(
            pathway=pathway,
            attempted=True,
            succeeded=succeeded,
            click_depth=1,
            trigger_element=ElementRef(
                dom_selector=match.selector,
                visible_text=match.visible_text,
            ),
            failure_reason=None if succeeded else "click_failed",
        )
    return outcomes


def build_event_log(outcomes: dict[Pathway, PathOutcome]) -> list[EventLogRef]:
    events: list[EventLogRef] = []
    for pathway in Pathway:
        outcome = outcomes[pathway]
        if not outcome.attempted:
            continue
        events.append(
            EventLogRef(
                event_index=len(events),
                action=f"click_{pathway.value}",
                target=outcome.trigger_element,
                outcome="success" if outcome.succeeded else "blocked",
            )
        )
    return events


async def _body_text(page: Any) -> str:
    try:
        return str(await page.inner_text("body", timeout=5_000))
    except Exception:
        return ""


async def _collect_candidates(page: Any) -> list[CandidateElement]:
    candidates: list[CandidateElement] = []
    for frame_index, frame in enumerate(page.frames):
        candidates.extend(await _collect_candidates_from_frame(frame, frame_index=frame_index))
    return filter_consent_candidates(candidates)


async def _collect_candidates_from_frame(frame: Any, *, frame_index: int) -> list[CandidateElement]:
    selector = "button, [role=button], a, input[type=button], input[type=submit], [aria-label]"
    locator = frame.locator(selector)
    count = await locator.count()
    candidates: list[CandidateElement] = []
    for index in range(min(count, 200)):
        item = locator.nth(index)
        try:
            if not await item.is_visible(timeout=500):
                continue
            text = await _candidate_label_text(item)
            if classify_pathway_label(text) is None:
                continue
            context_text = await _candidate_context_text(item)
            candidates.append(
                CandidateElement(
                    selector=f"frame[{frame_index}] >> {selector} >> nth={index}",
                    visible_text=text,
                    context_text=context_text,
                    in_initial_viewport=await _candidate_is_in_initial_viewport(item),
                )
            )
        except Exception:
            continue
    return candidates


async def _candidate_label_text(item: Any) -> str:
    try:
        metadata = await item.evaluate(
            """element => {
                const tag = element.tagName.toLowerCase();
                const role = (element.getAttribute('role') || '').toLowerCase();
                const aria = element.getAttribute('aria-label') || '';
                const value = element.getAttribute('value') || '';
                const text = (element.innerText || element.textContent || '').trim();
                return { tag, role, aria, value, text };
            }"""
        )
    except Exception:
        text = str(await item.inner_text(timeout=500)).strip()
        if not text:
            text = str(await item.get_attribute("aria-label") or "").strip()
        return text

    tag = str(metadata.get("tag") or "")
    role = str(metadata.get("role") or "")
    aria = str(metadata.get("aria") or "").strip()
    value = str(metadata.get("value") or "").strip()
    text = str(metadata.get("text") or "").strip()
    is_interactive = tag in {"button", "a", "input"} or role == "button"

    if not is_interactive and aria:
        return aria
    return text or value or aria


async def _candidate_context_text(item: Any) -> str:
    try:
        return str(
            await item.evaluate(
                """element => {
                    const consentPattern = (
                        /\\b(cookie|cookies|consent|privacy|tracking|advertising|personalised|personalized|partners?|data choices?)\\b/i
                    );
                    let node = element;
                    let fallback = '';
                    while (node && node.nodeType === Node.ELEMENT_NODE) {
                        const text = (node.innerText || node.textContent || '').trim();
                        if (text && !fallback) {
                            fallback = text;
                        }
                        if (text && consentPattern.test(text)) {
                            return text.slice(0, 1500);
                        }
                        if (node === document.body || node === document.documentElement) {
                            break;
                        }
                        node = node.parentElement;
                    }
                    const root = element.closest(
                        '[id*="cookie" i], [class*="cookie" i], '
                        + '[id*="consent" i], [class*="consent" i], '
                        + '[id*="privacy" i], [class*="privacy" i], '
                        + '[id*="notice" i], [class*="notice" i], '
                        + '[role="dialog"], section, aside, form, div'
                    ) || element.parentElement || element;
                    return ((root.innerText || root.textContent || fallback) || '').slice(0, 1500);
                }"""
            )
        )
    except Exception:
        return ""


async def _candidate_is_in_initial_viewport(item: Any) -> bool:
    try:
        box = await item.bounding_box()
        if box is None or box["width"] <= 0 or box["height"] <= 0:
            return False
        viewport = await item.evaluate(
            """element => {
                const view = element.ownerDocument.defaultView;
                return view ? { width: view.innerWidth, height: view.innerHeight } : null;
            }"""
        )
        if not viewport:
            return True
        return bool(
            box["x"] < viewport["width"]
            and box["x"] + box["width"] > 0
            and box["y"] < viewport["height"]
            and box["y"] + box["height"] > 0
        )
    except Exception:
        return True


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _has_consent_terms(text: str) -> bool:
    return bool(
        search(
            r"\b(cookie|cookies|consent|privacy|tracking|advertising|personalised|personalized|partners?|data choices?)\b",
            text,
        )
    )


async def _attempt_pathway_clicks(
    browser: Any,
    url: str,
    candidates: list[CandidateElement],
    timeout_ms: int,
) -> set[Pathway]:
    succeeded: set[Pathway] = set()
    for pathway in Pathway:
        candidate = next(
            (
                item
                for item in candidates
                if classify_pathway_label(item.visible_text) == pathway
            ),
            None,
        )
        if candidate is None:
            continue

        context = await browser.new_context(
            locale="en-US",
            viewport={"width": 1440, "height": 900},
        )
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            await page.wait_for_timeout(_CONSENT_RENDER_WAIT_MS)
            if await _click_candidate_in_any_frame(page, candidate.visible_text):
                succeeded.add(pathway)
        except Exception:
            continue
        finally:
            await context.close()
    return succeeded


async def _click_candidate_in_any_frame(page: Any, visible_text: str) -> bool:
    for frame in page.frames:
        for locator in (
            frame.get_by_role("button", name=visible_text, exact=True),
            frame.get_by_text(visible_text, exact=True),
        ):
            if await _click_first_visible_match(locator):
                return True
    return False


async def _click_first_visible_match(locator: Any) -> bool:
    try:
        count = await locator.count()
    except Exception:
        return False

    for index in range(min(count, 20)):
        item = locator.nth(index)
        try:
            if not await item.is_visible(timeout=500):
                continue
            await item.click(timeout=2_000)
            return True
        except Exception:
            continue
    return False


def _slug(url: HttpUrl) -> str:
    host = urlparse(str(url)).netloc or "site"
    return "".join(character if character.isalnum() else "_" for character in host).strip("_")


class CaptureFailedError(Exception):
    """Raised when a site could not be captured (CAPTCHA, timeout, blocked)."""


CaptureFailed = CaptureFailedError
