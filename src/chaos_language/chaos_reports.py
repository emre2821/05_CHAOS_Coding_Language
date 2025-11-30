"""Business-facing reporting helpers for CHAOS environments."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List

from .chaos_stdlib import text_snippet, uniq


def _normalize_emotions(emotions: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Coerce raw emotion payloads into a predictable structure.

    Each entry becomes ``{"name": <UPPER>, "intensity": <int>} `` with intensities
    clamped to ``0-10``. Unknown payloads are ignored gracefully.
    """

    out: List[Dict[str, Any]] = []
    for emo in emotions or []:
        if not isinstance(emo, dict):
            continue
        name = str(emo.get("name") or emo.get("type") or "").upper().strip()
        if not name:
            continue
        raw = emo.get("intensity", 0)
        try:
            intensity = max(0, min(int(raw), 10))
        except Exception:
            intensity = 0
        out.append({"name": name, "intensity": intensity})
    out.sort(key=lambda e: (-e["intensity"], e["name"]))
    return out


def generate_business_report(env: Dict[str, Any], *, include_timestamp: bool = True) -> Dict[str, Any]:
    """Project a CHAOS environment into an executive snapshot.

    Parameters
    ----------
    env:
        Environment emitted by :func:`chaos_runtime.run_chaos` or the agent.
    include_timestamp:
        When true, add ``generated_at`` to the payload.
    """

    structured = env.get("structured_core") or {}
    emotions = _normalize_emotions(env.get("emotive_layer"))
    narrative = text_snippet(env.get("chaosfield_layer", ""), 280)

    tags = uniq([k for k in structured.keys() if k.isupper()])
    top_emotion = emotions[0]["name"] if emotions else None

    report: Dict[str, Any] = {
        "structured": structured,
        "emotions": emotions,
        "top_emotion": top_emotion,
        "narrative": narrative,
        "tags": tags,
        "insight": _craft_insight(structured, top_emotion, narrative),
    }
    if include_timestamp:
        report["generated_at"] = datetime.now(timezone.utc).isoformat()
    return report


def render_report_lines(report: Dict[str, Any]) -> List[str]:
    """Render a report payload into CLI-friendly lines."""

    lines = [
        "=== CHAOS Business Report ===",
        f"Generated: {report.get('generated_at', 'n/a')}",
        f"Top emotion: {report.get('top_emotion') or 'None'}",
    ]
    structured = report.get("structured") or {}
    if structured:
        lines.append("-- Structured Core --")
        for key, value in structured.items():
            lines.append(f"{key}: {value}")
    emotions = report.get("emotions") or []
    if emotions:
        lines.append("-- Emotive Layer --")
        for emo in emotions:
            lines.append(f"{emo['name']}: {emo['intensity']}")
    if report.get("narrative"):
        lines.append("-- Chaosfield Narrative --")
        lines.append(report["narrative"])
    if report.get("insight"):
        lines.append("-- Insight --")
        lines.append(report["insight"])
    return lines


def _craft_insight(structured: Dict[str, Any], top_emotion: str | None, narrative: str) -> str:
    account = structured.get("ACCOUNT") or structured.get("ACCOUNT_ID") or structured.get("CLIENT")
    stage = structured.get("STAGE") or structured.get("STATUS")
    pieces: List[str] = []
    if account:
        pieces.append(f"Account {account}")
    if stage:
        pieces.append(f"is at {stage}")
    if top_emotion:
        pieces.append(f"feeling {top_emotion.lower()}")
    summary = " ".join(pieces).strip()
    if narrative:
        summary = f"{summary}. Narrative: {narrative}" if summary else f"Narrative: {narrative}"
    return summary
