# Security Policy

## Supported Versions

We actively maintain security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in CHAOS,
please report it responsibly.

### How to Report

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead:

1. **Use GitHub's private vulnerability reporting** via the Security tab
2. Or **email the maintainers** through GitHub's contact mechanism
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes (if available)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Assessment**: We will assess the vulnerability and determine severity
- **Updates**: We will keep you informed of our progress
- **Resolution**: We aim to resolve critical vulnerabilities within 7 days
- **Credit**: With your permission, we will credit you in our changelog

### Scope

Security issues we're interested in:

- Code execution vulnerabilities in the interpreter
- Injection vulnerabilities in script parsing
- Authentication/authorization bypasses (if applicable)
- Sensitive data exposure
- Denial of service vulnerabilities

### Out of Scope

- Issues in dependencies (please report to the upstream project)
- Social engineering attacks
- Physical security issues
- Issues requiring unlikely user interaction

## Security Best Practices

When using CHAOS:

1. **Validate input scripts** — Use the validator before executing untrusted scripts
2. **Run in sandboxed environments** — When processing untrusted content
3. **Keep dependencies updated** — Run `pip install --upgrade` regularly
4. **Review scripts before execution** — Especially from untrusted sources

## Disclosure Policy

- We follow responsible disclosure practices
- We request a 90-day disclosure window for vulnerability fixes
- We will coordinate with you on disclosure timing
- We will not take legal action against researchers acting in good faith

---

**Thank you for helping keep CHAOS secure.** 🔐
