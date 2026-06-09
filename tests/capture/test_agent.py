"""Tests for browser-agent helper logic that does not need a live browser."""

import pytest

from consent_audit.capture.agent import (
    CandidateElement,
    build_event_log,
    build_path_outcomes,
    classify_pathway_label,
    filter_consent_candidates,
    is_consent_candidate,
    snapshot_dom_html,
)
from consent_audit.models import Pathway


class DynamicNavigationPage:
    def __init__(self) -> None:
        self.evaluate_script = ""

    async def content(self) -> str:
        raise RuntimeError(
            "Page.content: Unable to retrieve content because the page is navigating "
            "and changing the content."
        )

    async def evaluate(self, script: str) -> str:
        self.evaluate_script = script
        return "<html><body>Fallback consent DOM</body></html>"


def test_classify_pathway_label_maps_common_consent_labels() -> None:
    assert classify_pathway_label("Accept All Cookies") == Pathway.ACCEPT
    assert classify_pathway_label("No, I decline") == Pathway.REJECT
    assert classify_pathway_label("Manage cookie preferences") == Pathway.CUSTOMIZE
    assert classify_pathway_label("Close") == Pathway.DISMISS
    assert classify_pathway_label("Privacy Policy") is None


@pytest.mark.asyncio
async def test_snapshot_dom_html_falls_back_when_page_content_churns() -> None:
    page = DynamicNavigationPage()

    snapshot = await snapshot_dom_html(page)

    assert snapshot.html == "<html><body>Fallback consent DOM</body></html>"
    assert "document.documentElement.outerHTML" in page.evaluate_script
    assert snapshot.warnings == [
        "page.content failed; used document.documentElement.outerHTML fallback: "
        "Page.content: Unable to retrieve content because the page is navigating "
        "and changing the content."
    ]


def test_is_consent_candidate_requires_consent_context_for_generic_labels() -> None:
    assert is_consent_candidate(
        CandidateElement(
            selector="button.accept",
            visible_text="Accept all",
            context_text="We use cookies to improve your experience.",
        )
    )
    assert is_consent_candidate(
        CandidateElement(
            selector="button.reject",
            visible_text="Reject all",
            context_text="Manage privacy choices for advertising partners.",
        )
    )
    assert not is_consent_candidate(
        CandidateElement(
            selector="button.settings",
            visible_text="Settings",
            context_text="Open account and display settings.",
        )
    )
    assert not is_consent_candidate(
        CandidateElement(
            selector="button.allow",
            visible_text="Allow",
            context_text="Allow location for local weather.",
        )
    )
    assert not is_consent_candidate(
        CandidateElement(
            selector="a.privacy-settings",
            visible_text="Privacy settings",
            context_text="Learn more in our privacy policy and cookie policy.",
            in_initial_viewport=False,
        )
    )


def test_filter_consent_candidates_discards_page_navigation_noise() -> None:
    candidates = [
        CandidateElement(
            selector="a.settings",
            visible_text="Settings",
            context_text="Account settings and notifications",
        ),
        CandidateElement(
            selector="button.accept",
            visible_text="Accept all",
            context_text="We use cookies and similar technologies.",
        ),
        CandidateElement(
            selector="button.manage",
            visible_text="Manage options",
            context_text="Privacy choices for cookies and personalised ads.",
        ),
    ]

    filtered = filter_consent_candidates(candidates)

    assert [item.selector for item in filtered] == ["button.accept", "button.manage"]


def test_build_path_outcomes_uses_first_candidate_per_pathway() -> None:
    outcomes = build_path_outcomes(
        [
            CandidateElement(selector="button.accept", visible_text="Accept All"),
            CandidateElement(selector="button.reject", visible_text="Reject All"),
            CandidateElement(selector="button.settings", visible_text="Cookie Settings"),
            CandidateElement(selector="button.close", visible_text="Close"),
            CandidateElement(selector="button.accept2", visible_text="Agree"),
        ]
    )

    assert set(outcomes) == set(Pathway)
    assert outcomes[Pathway.ACCEPT].succeeded
    assert outcomes[Pathway.ACCEPT].trigger_element is not None
    assert outcomes[Pathway.ACCEPT].trigger_element.dom_selector == "button.accept"
    assert outcomes[Pathway.REJECT].succeeded
    assert outcomes[Pathway.CUSTOMIZE].succeeded
    assert outcomes[Pathway.DISMISS].succeeded


def test_build_path_outcomes_records_missing_pathways_as_unattempted() -> None:
    outcomes = build_path_outcomes(
        [CandidateElement(selector="button.accept", visible_text="Accept All")]
    )

    assert outcomes[Pathway.ACCEPT].succeeded
    assert not outcomes[Pathway.REJECT].attempted
    assert not outcomes[Pathway.REJECT].succeeded
    assert outcomes[Pathway.REJECT].failure_reason == "no_candidate_detected"


def test_build_path_outcomes_separates_candidate_detection_from_click_success() -> None:
    outcomes = build_path_outcomes(
        [
            CandidateElement(selector="button.accept", visible_text="Accept All"),
            CandidateElement(selector="button.reject", visible_text="Reject All"),
        ],
        succeeded_pathways={Pathway.ACCEPT},
    )

    assert outcomes[Pathway.ACCEPT].attempted
    assert outcomes[Pathway.ACCEPT].succeeded
    assert outcomes[Pathway.REJECT].attempted
    assert not outcomes[Pathway.REJECT].succeeded
    assert outcomes[Pathway.REJECT].failure_reason == "click_failed"


def test_build_event_log_records_attempted_path_clicks() -> None:
    outcomes = build_path_outcomes(
        [
            CandidateElement(selector="button.accept", visible_text="Accept All"),
            CandidateElement(selector="button.reject", visible_text="Reject All"),
        ],
        succeeded_pathways={Pathway.ACCEPT},
    )

    events = build_event_log(outcomes)

    assert len(events) == 2
    assert events[0].action == "click_accept"
    assert events[0].outcome == "success"
    assert events[1].action == "click_reject"
    assert events[1].outcome == "blocked"
