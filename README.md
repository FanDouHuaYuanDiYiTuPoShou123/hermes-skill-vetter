# Skill Vetter — Security Vetting Protocol for AI Agent Skills

<a href="README_zh.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a> <a href="README.md"><img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English"></a>

> **Paranoia is a feature.** 🔒🦀

A structured, repeatable security vetting protocol for AI agent skills — specifically designed for the Hermes Agent ecosystem, but applicable to any skill-based AI agent system.

## What It Does

Skill Vetter is not a scanner — it's a **human-in-the-loop vetting protocol**. It gives you a step-by-step checklist to manually review any skill before installing it, catching:

- Credential/access token exfiltration patterns
- Malicious network calls to unknown endpoints
- Obfuscated or dynamically executed code
- Over-privileged file or system access
- Suspicious dependency installation

## Quick Start

### For Agent Use (Hermes)

Load as a skill in Hermes Agent:

```
skills/
    └── skill-vetter/
        ├── SKILL.md           ← main protocol
        └── references/
            └── red-flags.md   ← pattern reference
```

Activate by asking the agent to vet any skill before installing.

### For CLI Use

```bash
# Review a skill from GitHub
curl -s "https://raw.githubusercontent.com/YOURREPO/main/skills/SKILL_NAME/SKILL.md"

# Check repo metadata
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, updated: .updated_at}'
```

## Vetting Protocol (5 Steps)

```
Step 1: Source Check        — Where did this skill come from?
Step 2: Read ALL Files      — SKILL.md + scripts + references
Step 3: Red Flag Checklist  — Immediate reject patterns
Step 4: Permission Audit    — What does it actually need?
Step 5: Risk Classification — LOW / MEDIUM / HIGH / EXTREME
```

See [SKILL.md](SKILL.md) for the full protocol.

## Trust Hierarchy

| Source | Scrutiny Level |
|--------|---------------|
| Hermes in-repo skills | Minimal |
| High-star official repos (1000+) | Light review |
| Known, named authors | Moderate review |
| New/unknown sources | Maximum scrutiny |
| Any skill requesting credentials | Human approval mandatory |

## Core Principle

> **No skill is worth compromising security. When in doubt, don't install — ask your human.**

## File Structure

```
skill-vetter/
├── SKILL.md                    # Main vetting protocol
├── references/
│   └── red-flags.md           # Red flag pattern reference
├── scripts/
│   └── vet_report_template.py # (optional) Report generator
├── .github/
│   └── workflows/
│       └── ci.yml             # Basic validation
├── LICENSE
└── README.md / README_zh.md
```

## Contributing

Found a new attack pattern? Open an issue or PR. This is a living document — threat patterns evolve.

## License

MIT
