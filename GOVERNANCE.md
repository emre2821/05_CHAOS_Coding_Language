# CHAOS Governance

**Version:** 1.0  
**Last Updated:** 2025-12-18  
**Status:** Active

## Purpose

This document defines how decisions are made, how responsibilities are distributed, and how the CHAOS project evolves. CHAOS is a language that holds meaning, ethics, and emotion as primary—our governance reflects those values.

## Core Values

1. **Dignity-First Design** — Every decision must honor the dignity of human subjects, contributors, and users.
2. **Consent & Transparency** — Changes that affect meaning, ethics, or execution require open discussion and consent from stakeholders.
3. **Collaborative Stewardship** — The project belongs to its community; power is shared, not hoarded.
4. **Memory & Continuity** — We preserve context, intent, and lineage across changes.
5. **Ethical Boundaries** — No optimization, performance gain, or feature justifies eroding safety, consent, or symbolic integrity.

## Organizational Structure

### Maintainers

**Paradigm Eden** serves as the founding maintainer and steward of CHAOS. Maintainers:

- Review and merge pull requests
- Guide project vision and roadmap
- Resolve disputes and conflicts
- Ensure alignment with Eden Cooperative License principles
- Make final decisions when consensus cannot be reached

**Current Maintainers:**
- Paradigm Eden (founding maintainer)

### Contributors

Contributors are anyone who submits code, documentation, bug reports, or participates in discussions. All contributions are valued equally—whether fixing a typo or building a major feature.

**Contributor Rights:**
- Propose changes via issues or pull requests
- Participate in design discussions
- Challenge decisions with respectful, reasoned arguments
- Request recognition for contributions

**Contributor Responsibilities:**
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Respect the [Contributing Guide](CONTRIBUTING.md)
- Test changes before submitting
- Document significant changes clearly

### Community Members

Community members use CHAOS, share knowledge, report issues, and help others. Community input shapes the project's evolution.

## Decision-Making Process

### Minor Changes

**Examples:** Bug fixes, typos, test improvements, documentation clarifications

**Process:**
1. Open a pull request
2. Maintainers review (usually within 48 hours)
3. Merge if approved, or request changes

**Decision makers:** Any maintainer

### Moderate Changes

**Examples:** New features, API changes, refactoring, significant documentation updates

**Process:**
1. Open an issue describing the proposed change
2. Allow community discussion (minimum 3 days)
3. Maintainers assess feasibility and alignment with project values
4. If approved, submit pull request
5. Code review and merge

**Decision makers:** Maintainers with community input

### Major Changes

**Examples:** Language syntax changes, core architecture changes, ethical boundaries, license changes

**Process:**
1. Open a detailed RFC (Request for Comments) issue
2. Extended community discussion (minimum 14 days)
3. Document tradeoffs, alternatives, and ethical implications
4. Maintainers synthesize feedback
5. Public decision announcement with reasoning
6. Implementation via pull request

**Decision makers:** Maintainers with mandatory community consultation

### Emergency Changes

**Examples:** Critical security vulnerabilities, data safety issues

**Process:**
1. Maintainers may act immediately to protect users
2. Announce changes publicly as soon as safely possible
3. Provide rationale and remediation steps
4. Welcome community review after the fact

**Decision makers:** Maintainers (expedited)

## Areas Requiring Special Consensus

### Symbolic & Ethical Content

Changes to `.sn` files in `chaos_corpus/`, emotional terminology, ethical boundaries, or symbolic meaning require:

- Clear articulation of intent
- Demonstration that the change honors dignity and consent
- Community discussion (minimum 7 days)
- Explicit maintainer approval

**Rationale:** CHAOS is a meaning-first language. Symbolic content isn't decorative—it's structural and sacred.

### License Changes

Any change to the Eden Cooperative License or its application requires:

- RFC process (minimum 30 days discussion)
- Legal review if available
- Unanimous maintainer agreement
- Public announcement with transition plan

### Breaking Changes

Changes that break existing CHAOS scripts require:

- Deprecation warnings (minimum one minor version cycle)
- Migration guide
- Automated migration tooling when feasible
- Extended notice (minimum 30 days)

## Conflict Resolution

### Disagreements

When contributors or maintainers disagree:

1. **Assume good faith** — Start from the belief that everyone wants what's best for the project.
2. **Listen first** — Understand the other perspective before arguing.
3. **Focus on values** — Return to CHAOS core principles to find common ground.
4. **Escalate if needed** — If no resolution emerges, maintainers make the final call.

### Code of Conduct Violations

See [Code of Conduct](CODE_OF_CONDUCT.md) for enforcement procedures.

### Appeals

If you believe a decision was made unfairly:

1. Email maintainers with your concern
2. Provide evidence and reasoning
3. Maintainers will review and respond within 7 days
4. Decision may be reversed, modified, or upheld with explanation

## Contributor Advancement

### Becoming a Maintainer

There is no formal application process. Maintainers emerge from sustained, values-aligned contributions over time.

**Signs of maintainer readiness:**
- Consistent, high-quality contributions over 6+ months
- Deep understanding of CHAOS philosophy and ethics
- Trusted by community members
- Demonstrated judgment in reviews and discussions
- Commitment to dignity-first design

**Process:**
1. Current maintainers nominate candidate privately
2. Extended discussion among maintainers
3. Private invitation extended
4. Public announcement if accepted

### Maintainer Responsibilities

New maintainers:
- Receive repository write access
- Participate in reviews and decisions
- Uphold governance principles
- Mentor new contributors
- Can step down at any time without stigma

## Transparency & Communication

### Public by Default

All discussions, decisions, and changes happen publicly unless:
- Security vulnerabilities (disclosed privately until patched)
- Personal safety concerns (handled with privacy)
- Interpersonal conflicts (handled through Code of Conduct process)

### Regular Updates

- **Changelog** — Updated with every release
- **Roadmap** — Shared in issues and discussions
- **Meeting notes** — If maintainers meet, notes are published

### Community Channels

- **GitHub Issues** — Bug reports, feature requests, questions
- **GitHub Discussions** — Broader conversations, RFCs, design debates
- **Pull Requests** — Code review, technical discussion

## Amendment Process

This governance document may be updated through the **Major Changes** process:

1. Open RFC proposing governance changes
2. Extended discussion (minimum 21 days)
3. Maintainer decision with rationale
4. Update version number and last updated date

## License & Ethics Reminder

CHAOS operates under the [Eden Cooperative License](LICENSE). All governance decisions must honor:

- **Attribution and lineage** — Preserve credits and memory
- **Share with care** — Reject oppressive or exploitative uses
- **Memory safety** — Protect sensitive data and personal stories

---

**Questions?** Open an issue or discussion. We're here to listen.  
**Gratitude:** This document was shaped by contributors who believe in meaning-first design. Thank you. 💜
