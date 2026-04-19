"""Golden-file tests for Layer 1.

Each test loads a fixture CaptureBundle + its expected Layer1Result and asserts
that score_layer1(bundle) produces the expected output. See CONCEPTS.md §1 for
the specific test cases required before the layer is considered "done."
"""

import pytest


@pytest.mark.skip(reason="implement alongside layers.layer1 in week 2")
def test_clean_banner_passes_gate() -> None:
    """Site with all four pathways visible at first layer → gate_passed = True."""
    raise NotImplementedError


@pytest.mark.skip(reason="implement alongside layers.layer1 in week 2")
def test_missing_reject_fails_gate() -> None:
    """Site missing a reject pathway → gate_passed = False, missing_paths contains REJECT."""
    raise NotImplementedError


@pytest.mark.skip(reason="implement alongside layers.layer1 in week 2")
def test_reject_requires_three_actions_fails_gate() -> None:
    """UMBRA DP15 pattern: reject reachable but costs >2 actions → reject_available = False."""
    raise NotImplementedError
