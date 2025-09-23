"""Validation helpers for CHAOS scripts.

The business promise of CHAOS depends on every ritual including three
interlocking layers:

* a **structured core** that captures telemetry fields,
* an **emotive layer** that records affect and symbolic resonance, and
* a **chaosfield narrative** that carries the qualitative story.

`validate_chaos` preflights a script by running it through the lexer and parser
and then inspecting the resulting AST.  When a layer is missing or malformed we
raise :class:`ChaosValidationError` with a targeted message so operators know
how to repair the ritual quickly.
"""

from __future__ import annotations

from typing import Dict, List

from chaos_errors import ChaosValidationError
from chaos_lexer import ChaosLexer
from chaos_parser import ChaosParser, Node, NodeType


def validate_chaos(source: str) -> None:
    """Validate that ``source`` contains the full CHAOS ritual.

    Parameters
    ----------
    source:
        Raw CHAOS script text.

    Raises
    ------
    ChaosValidationError
        If the script cannot be tokenized, parsed, or fails structural checks.
    """

    if not isinstance(source, str):
        raise ChaosValidationError("CHAOS source must be textual input")

    try:
        tokens = ChaosLexer().tokenize(source)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise ChaosValidationError(f"CHAOS Validation Failed during lexing: {exc}") from exc

    # ``tokenize`` always emits an EOF token, so a single token means "empty".
    if len(tokens) <= 1:
        raise ChaosValidationError(
            "CHAOS script is empty; expected structured_core, emotive_layer, and chaosfield_layer"
        )

    try:
        ast = ChaosParser(tokens).parse()
    except Exception as exc:
        raise ChaosValidationError(f"CHAOS Validation Failed during parsing: {exc}") from exc

    _require(ast is not None, "Parser did not return a program node")
    _require(ast.type == NodeType.PROGRAM, "Top-level CHAOS node must be PROGRAM")
    _require(len(ast.children) == 3, "Expected 3 layers: structured_core, emotive_layer, chaosfield_layer")

    structured, emotive, chaosfield = ast.children
    _validate_structured_core(structured)
    _validate_emotive_layer(emotive)
    _validate_chaosfield_layer(chaosfield)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ChaosValidationError(message)


def _validate_structured_core(node: Node) -> None:
    _require(node.type == NodeType.STRUCTURED_CORE, "First layer must be STRUCTURED_CORE")
    core = node.value or {}
    _require(isinstance(core, dict), "Structured core must be a mapping of tags to values")
    _require(core, "Structured core must include at least one [TAG]: value pair")
    for key in core:
        _require(isinstance(key, str) and key.strip(), "Structured core tags must be non-empty strings")


def _validate_emotive_layer(node: Node) -> None:
    _require(node.type == NodeType.EMOTIVE_LAYER, "Second layer must be EMOTIVE_LAYER")
    emotions: List[Dict[str, object]] = node.value or []
    _require(isinstance(emotions, list), "Emotive layer must contain a list of emotion entries")
    _require(emotions, "Emotive layer must include at least one EMOTION ritual tag")

    for idx, entry in enumerate(emotions):
        _require(isinstance(entry, dict), f"Emotion entry #{idx + 1} is malformed")
        name = entry.get("name")
        _require(isinstance(name, str) and name.strip(), f"Emotion entry #{idx + 1} is missing a name")
        intensity = entry.get("intensity")
        _require(isinstance(intensity, int), f"Emotion '{name}' must record an integer intensity")
        _require(
            0 <= intensity <= 10,
            f"Emotion '{name}' intensity {intensity} is out of bounds (expected 0-10)",
        )


def _validate_chaosfield_layer(node: Node) -> None:
    _require(node.type == NodeType.CHAOSFIELD_LAYER, "Third layer must be CHAOSFIELD_LAYER")
    narrative = node.value or ""
    _require(isinstance(narrative, str), "Chaosfield layer must be narrative text")
    _require(narrative.strip(), "Chaosfield layer must include narrative text inside { ... }")
