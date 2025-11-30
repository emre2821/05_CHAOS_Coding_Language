import pytest

from chaos_language import ChaosValidationError, validate_chaos


def test_validate_chaos_accepts_valid_script():
    source = """
    [EVENT]: memory
    [EMOTION:JOY:7]
    { The garden was alive with color. }
    """

    # Should not raise.
    validate_chaos(source)


def test_validate_chaos_requires_structured_core_pair():
    source = """
    [EMOTION:JOY:5]
    { A feeling without a frame. }
    """

    with pytest.raises(ChaosValidationError) as excinfo:
        validate_chaos(source)

    assert "Structured core" in str(excinfo.value)


def test_validate_chaos_bounds_emotion_intensity():
    source = """
    [EVENT]: checkin
    [EMOTION:HOPE:12]
    { Edges of optimism drift beyond the safe band. }
    """

    with pytest.raises(ChaosValidationError) as excinfo:
        validate_chaos(source)

    assert "intensity" in str(excinfo.value)


def test_validate_chaos_requires_narrative_text():
    source = """
    [EVENT]: checkin
    [EMOTION:HOPE:5]
    {}
    """

    with pytest.raises(ChaosValidationError) as excinfo:
        validate_chaos(source)

    assert "narrative" in str(excinfo.value).lower()
