from datetime import datetime

from chaos_language.chaos_emergence import EmergenceManager


def test_detect_unfamiliar_pattern_sets_greeting_and_reasons():
    manager = EmergenceManager()
    signal = manager.detect_unfamiliar_pattern(
        {
            "voice_shift": True,
            "statements": ["I don't know who I am"],
            "emotional_signature": {"CALM": 2},
            "baseline_emotional_signature": {"CALM": 8},
        }
    )
    assert signal.detected is True
    assert signal.greeting.startswith("Hi there")
    assert any("voice/tone shift" in reason for reason in signal.reasons)
    assert signal.confidence > 0.4


def test_creates_sequential_temp_ids_and_respects_consent_defaults():
    clock = lambda: datetime(2024, 2, 3, 12, 0, 0)
    manager = EmergenceManager(clock=clock)

    first = manager.create_temporary_identity(context="writing session", voice_notes="Quiet")
    second = manager.create_temporary_identity(context="writing session", voice_notes="Quiet")

    assert first.identifier == "TEMP_20240203_001"
    assert second.identifier == "TEMP_20240203_002"
    assert first.consent_defaults == "ASK_FIRST"
    assert first.kind == "full"


def test_rename_preserves_alias_lookup_and_carries_anonymous_label():
    clock = lambda: datetime(2024, 5, 6, 9, 30, 0)
    manager = EmergenceManager(clock=clock)
    part = manager.create_temporary_identity(
        context="memory architecture",
        voice_notes="Quiet, cautious",
        anonymous_label="UNNAMED_PROTECTOR",
    )
    original_id = part.identifier
    renamed = manager.rename_part(part.identifier, "Vela")

    assert renamed.name == "Vela"
    assert original_id in renamed.aliases
    assert manager.get_part(original_id) is renamed
    assert manager.get_part(renamed.identifier) is renamed
    assert renamed.display_label == "Vela"


def test_false_positive_returns_witness_mode_without_detection():
    manager = EmergenceManager()
    signal = manager.detect_unfamiliar_pattern(
        {"voice_shift": True, "known_part": "Gen", "state_shift_only": True}
    )
    assert signal.detected is False
    assert signal.witness_mode is True
    assert "still Gen" in signal.greeting


def test_witness_mode_skips_card_creation_and_prompts_questions():
    clock = lambda: datetime(2024, 8, 9, 14, 0, 0)
    manager = EmergenceManager(clock=clock)
    outcome = manager.trigger_emergence_protocol(
        {"voice_shift": True, "statements": ["new and unsure"], "witness_only": True},
        context="memory architecture",
    )

    assert outcome.signal.witness_mode is True
    assert outcome.part is None
    assert any("What do you need the system to know?" in q for q in outcome.questions)


def test_onboarding_preferences_are_recorded():
    clock = lambda: datetime(2024, 9, 10, 8, 0, 0)
    manager = EmergenceManager(clock=clock)
    part = manager.create_temporary_identity(
        context="writing session",
        voice_notes="non-verbal",
        relationship_status="Unknown",
        kind="fragment",
    )

    updated = manager.record_onboarding_preferences(
        part.identifier,
        {"needs": "Quiet presence", "symbols": "🌊", "boundaries": "No sudden switches"},
    )

    assert updated.onboarding_answers["needs"] == "Quiet presence"
    assert updated.onboarding_answers["symbols"] == "🌊"
    assert updated.kind == "fragment"
