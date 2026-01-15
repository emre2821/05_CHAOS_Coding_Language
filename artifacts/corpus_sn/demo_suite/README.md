# CHAOS Demo Suite (.sn)

A curated set of CHAOS artifacts showing different domains and ethics postures. Use them with `chaos-cli`, `chaos-exec`, or `chaos-validate`.

## Files
- `01_hello_welcome.sn` — Minimal welcome with emotional stance.
- `02_memory_garden_anchor.sn` — Symbolic memory anchor with growth motif.
- `03_consent_gate.sn` — Governance guardrails and refusal path.
- `04_check_in_protocol.sn` — Stepwise check-in respecting silence.
- `05_incident_report.sn` — Outage record without blame, privacy-aware.
- `06_research_brief.sn` — Research summary with explicit consent and anonymization.
- `07_wellbeing_check.sn` — Support posture without pressure or diagnosis.
- `08_meeting_agenda.sn` — Facilitated agenda with inclusion boundaries.
- `09_data_request.sn` — Minimal-scope data access with expiry.
- `10_ai_handoff.sn` — Human-in-the-loop AI approvals.
- `11_transition_ritual.sn` — Stewardship handoff preserving memory.
- `12_retrospective.sn` — Blameless learning ritual with opt-out.

## Quick usage
```bash
# Inspect as JSON
chaos-cli artifacts/corpus_sn/demo_suite/03_consent_gate.sn --json

# Validate
chaos-validate artifacts/corpus_sn/demo_suite/04_check_in_protocol.sn -v

# Run with reporting
chaos-exec artifacts/corpus_sn/demo_suite/05_incident_report.sn --report --emit report.json
```

Each artifact keeps CHAOS priorities: meaning-first narrative, explicit consent/boundaries, and emotional context.
