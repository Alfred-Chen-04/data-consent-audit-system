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

from pydantic import HttpUrl

from consent_audit.models import CaptureBundle


async def capture_site(url: HttpUrl, *, timeout_seconds: int = 180) -> CaptureBundle:
    """Perform one dynamic capture of a site's consent interface.

    Returns a complete CaptureBundle. On unrecoverable errors (CAPTCHA walls,
    timeouts), raises CaptureFailed with a reason that the orchestrator can log.
    """
    raise NotImplementedError("implement in week 2 — see plan §5")


class CaptureFailed(Exception):
    """Raised when a site could not be captured (CAPTCHA, timeout, blocked)."""
