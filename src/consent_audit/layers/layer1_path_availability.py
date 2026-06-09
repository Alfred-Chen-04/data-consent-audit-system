"""Layer 1 — Path Availability. Gate for the rest of the audit.

See CONCEPTS.md §1 for the precise rules. Pure function, no side effects.
"""

from consent_audit.models import CaptureBundle, ElementRef, Layer1Result, Pathway

_TWO_ACTION_GATE_PATHS = {Pathway.REJECT, Pathway.CUSTOMIZE}


def score_layer1(bundle: CaptureBundle) -> Layer1Result:
    """Evaluate whether each of the four pathways is present AND reachable.

    Rules (CONCEPTS.md §1):
      - `reject` and `customize` must be reachable within 2 actions of banner appearance
      - `dismiss` informational only
      - If reject OR customize missing → gate_passed = False
    """
    availability: dict[Pathway, bool] = {}
    evidence: dict[Pathway, ElementRef] = {}

    for pathway in Pathway:
        outcome = bundle.path_outcomes.get(pathway)
        available = outcome is not None and outcome.attempted and outcome.succeeded
        if outcome is not None and available and pathway in _TWO_ACTION_GATE_PATHS:
            available = outcome.click_depth <= 2

        availability[pathway] = available
        if available and outcome is not None and outcome.trigger_element is not None:
            evidence[pathway] = outcome.trigger_element

    missing_paths = [pathway for pathway in Pathway if not availability[pathway]]
    gate_passed = availability[Pathway.REJECT] and availability[Pathway.CUSTOMIZE]

    return Layer1Result(
        accept_available=availability[Pathway.ACCEPT],
        reject_available=availability[Pathway.REJECT],
        customize_available=availability[Pathway.CUSTOMIZE],
        dismiss_available=availability[Pathway.DISMISS],
        missing_paths=missing_paths,
        evidence=evidence,
        gate_passed=gate_passed,
    )
