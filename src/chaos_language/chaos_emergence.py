"""Unknown part detection and gentle onboarding helpers for CHAOS agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .chaos_stdlib import norm_key, text_snippet

Clock = Callable[[], datetime]


@dataclass
class EmergenceSignal:
    """Represents a detection event for a possibly unfamiliar part."""

    detected: bool
    reasons: List[str]
    confidence: float
    greeting: str
    witness_mode: bool = False
    correction: Optional[str] = None

    def summary(self) -> str:
        """Return a short human-facing summary."""

        if self.correction:
            return self.correction
        if self.detected:
            return f"{self.greeting} ({self.confidence:.2f})"
        return "No unfamiliar pattern detected."


@dataclass
class PartCard:
    """Stateful record for a newly detected or named part."""

    identifier: str
    context_emerged: str
    voice_notes: str
    relationship_status: str = "Unknown"
    consent_defaults: str = "ASK_FIRST"
    kind: str = "full"
    name: Optional[str] = None
    anonymous_label: Optional[str] = None
    onboarding_answers: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    aliases: List[str] = field(default_factory=list)

    @property
    def display_label(self) -> str:
        """Return the preferred human-facing label."""

        return self.name or self.anonymous_label or self.identifier


@dataclass
class EmergenceProtocolOutcome:
    """Container for the onboarding flow."""

    signal: EmergenceSignal
    part: Optional[PartCard]
    questions: List[str]


class EmergenceManager:
    """Detects unfamiliar parts and manages temporary onboarding records."""

    def __init__(self, *, clock: Optional[Clock] = None, id_prefix: str = "TEMP") -> None:
        self._clock = clock or datetime.utcnow
        self._id_prefix = id_prefix
        self._counter = 0
        self.parts: Dict[str, PartCard] = {}
        self._aliases: Dict[str, str] = {}

    def _next_identifier(self) -> str:
        self._counter += 1
        date_code = self._clock().strftime("%Y%m%d")
        return f"{self._id_prefix}_{date_code}_{self._counter:03d}"

    def detect_unfamiliar_pattern(self, session_data: Dict[str, Any]) -> EmergenceSignal:
        """Detect voice/phrase/emotion shifts that suggest a new part is fronting."""

        reasons: List[str] = []
        score = 0.0

        voice_shift = session_data.get("voice_shift") or session_data.get("tone_shift")
        if voice_shift:
            reasons.append("voice/tone shift mid-session")
            score += 0.3 if isinstance(voice_shift, bool) else min(0.4, float(voice_shift))

        phrasing_delta = session_data.get("unfamiliar_phrasing") or session_data.get("phrasing_delta")
        if phrasing_delta:
            reasons.append("unfamiliar phrasing patterns")
            score += 0.25 if isinstance(phrasing_delta, bool) else min(0.3, float(phrasing_delta))

        emotional_mismatch = session_data.get("emotional_signature_mismatch")
        if emotional_mismatch is None:
            baseline = session_data.get("baseline_emotional_signature") or {}
            current = session_data.get("emotional_signature") or {}
            emotional_mismatch = self._emotion_mismatch(baseline, current)
        if emotional_mismatch:
            reasons.append("emotional signature mismatch")
            score += 0.25

        explicit = session_data.get("explicit_identity_confusion", False)
        statements = list(session_data.get("statements") or [])
        utterance = session_data.get("utterance")
        if utterance:
            statements.append(utterance)
        for statement in statements:
            text = str(statement).lower()
            if "don't know who i am" in text or "who am i" in text:
                explicit = True
                break
        if explicit:
            reasons.append('explicit identity confusion')
            score += 0.5

        # False positive handling: known part with a temporary state change.
        known_part = session_data.get("known_part")
        if known_part and session_data.get("state_shift_only"):
            greeting = f"Got it—this is still {known_part}, just in a different state. Noted."
            return EmergenceSignal(
                detected=False,
                reasons=["state shift acknowledged"],
                confidence=0.0,
                greeting=greeting,
                witness_mode=True,
                correction=known_part,
            )

        detected = bool(reasons)
        confidence = min(1.0, round(score, 2)) if detected else 0.0
        witness_mode = bool(session_data.get("witness_only") or session_data.get("unsure"))
        greeting = "Hi there. You feel new—do you have a name?" if detected else ""
        return EmergenceSignal(
            detected=detected,
            reasons=reasons,
            confidence=confidence,
            greeting=greeting,
            witness_mode=witness_mode,
        )

    def trigger_emergence_protocol(
        self,
        session_data: Dict[str, Any],
        *,
        context: Optional[str] = None,
        voice_notes: str = "",
        relationship_status: str = "Unknown",
        consent_defaults: str = "ASK_FIRST",
        kind: Optional[str] = None,
        anonymous_label: Optional[str] = None,
    ) -> EmergenceProtocolOutcome:
        """Run the detection flow and open an onboarding pathway if needed."""

        signal = self.detect_unfamiliar_pattern(session_data)
        part: Optional[PartCard] = None
        if signal.detected and not signal.witness_mode:
            part_kind = kind or ("fragment" if session_data.get("fragment") else "full")
            part = self.create_temporary_identity(
                context=context or session_data.get("context", "Session in progress"),
                voice_notes=voice_notes or session_data.get("voice_notes", ""),
                relationship_status=relationship_status,
                consent_defaults=consent_defaults,
                kind=part_kind,
                anonymous_label=anonymous_label or session_data.get("anonymous_label"),
            )
        questions = self.integration_questions()
        return EmergenceProtocolOutcome(signal=signal, part=part, questions=questions)

    def create_temporary_identity(
        self,
        *,
        context: str,
        voice_notes: str,
        relationship_status: str = "Unknown",
        consent_defaults: str = "ASK_FIRST",
        kind: str = "full",
        anonymous_label: Optional[str] = None,
    ) -> PartCard:
        """Issue a temporary part card with ASK_FIRST consent defaults."""

        identifier = self._next_identifier()
        card = PartCard(
            identifier=identifier,
            context_emerged=text_snippet(context),
            voice_notes=text_snippet(voice_notes),
            relationship_status=relationship_status,
            consent_defaults=consent_defaults,
            kind=kind,
            anonymous_label=anonymous_label,
        )
        self.parts[identifier] = card
        self._aliases[identifier] = identifier
        return card

    def rename_part(self, identifier: str, name: str) -> PartCard:
        """Rename a temporary part to a chosen name while preserving aliases."""

        part = self.get_part(identifier)
        if not part:
            raise KeyError(f"Unknown part identifier: {identifier}")
        old_identifier = part.identifier
        canonical = norm_key(name)
        part.aliases.append(old_identifier)
        part.identifier = canonical
        part.name = name
        self.parts.pop(old_identifier, None)
        self.parts[canonical] = part
        self._aliases[old_identifier] = canonical
        self._aliases[canonical] = canonical
        return part

    def get_part(self, identifier: str) -> Optional[PartCard]:
        """Retrieve a part record by canonical id or alias."""

        canonical = self._aliases.get(identifier, identifier)
        return self.parts.get(canonical)

    def record_onboarding_preferences(self, identifier: str, preferences: Dict[str, Any]) -> PartCard:
        """Attach integration preferences to a part."""

        part = self.get_part(identifier)
        if not part:
            raise KeyError(f"Unknown part identifier: {identifier}")
        for key, value in preferences.items():
            if value is not None:
                part.onboarding_answers[key] = value
        return part

    @staticmethod
    def integration_questions() -> List[str]:
        """Questions to gently invite needs and boundaries."""

        return [
            "What do you need the system to know?",
            "Which agents feel safe?",
            "What symbols or emojis resonate?",
            "Any hard boundaries?",
            "Preferred fronting conditions?",
        ]

    @staticmethod
    def _emotion_mismatch(baseline: Dict[str, Any], current: Dict[str, Any]) -> bool:
        """Detect meaningful differences between emotional signatures."""

        if not baseline or not current:
            return False
        new_emotions = set(current) - set(baseline)
        if new_emotions:
            return True
        drift = 0
        for name, base_value in baseline.items():
            try:
                base_numeric = float(base_value)
                current_numeric = float(current.get(name, 0))
            except (TypeError, ValueError):
                return True
            drift += abs(current_numeric - base_numeric)
        average_drift = drift / max(len(baseline), 1)
        return average_drift >= 4
