"""Layer 1 — Path Availability. Gate for the rest of the audit.

See CONCEPTS.md §1 for the precise rules. Pure function, no side effects.
"""

from consent_audit.models import CaptureBundle, Layer1Result, Pathway


def score_layer1(bundle: CaptureBundle) -> Layer1Result:
    """Evaluate whether each of the four pathways is present AND reachable.

    Rules (CONCEPTS.md §1):
      - `reject` and `customize` must be reachable within 2 actions of banner appearance
      - `dismiss` informational only
      - If reject OR customize missing → gate_passed = False
    """
    raise NotImplementedError("implement week 2 — depends on CaptureBundle.path_outcomes")
