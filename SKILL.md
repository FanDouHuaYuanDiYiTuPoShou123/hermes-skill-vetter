---
name: skill-vetter
description: "Security-first vetting for skills. Use before installing any skill from external sources — clawhub, GitHub, or shared repos. Checks for red flags, permission scope, and suspicious patterns."
version: 1.0.0
author: FanDouHuaYuanDiYiTuPoShou123 (adapted from tokauth/skillscan)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, skill-vetting, skill-safety, permissions, red-flags]
    related_skills: [dogfood, hermes-agent-skill-authoring]
---

# Skill Vet — Security Vetting for Hermes Skills

## Overview

Before installing any skill from an external source — ClawdHub, GitHub, a shared repo, or even a skill your agent mentions — vet it first. This skill gives you a structured, repeatable protocol to catch malicious, over-privileged, or just sketchy skill code before it touches your system.

**Core principle:** No skill is worth compromising security. When in doubt, don't install — ask your human.

## When to Use

- Before installing any skill from ClawdHub, GitHub, or other external sources
- When evaluating skills shared by another agent
- When asked to install a skill you haven't seen before
- Before running `skill_manage(action='create')` with content provided by the user
- Anytime you're about to load and act on an unknown SKILL.md

**Trigger phrases:** "install this skill", "add this", "load from URL", "来自 xxx 的技能", "帮我安装这个技能", or any mention of an unfamiliar skill name.

**Don't use for:** Reading/skimming skills you've already vetted, or skills from known-trusted in-repo sources.

## Vetting Protocol

### Step 1: Source Check

Answer these questions about where the skill came from:

```
Source evaluation:
- [ ] Where did this skill come from?
- [ ] Is the author known/reputable?
- [ ] How many downloads/stars does it have?
- [ ] When was it last updated?
- [ ] Are there reviews or reports from other users?
```

If the source is completely unknown (random GitHub gist, unverified link, etc.) → escalate to **HIGH risk** by default.

### Step 2: Read ALL Skill Files

Read every file in the skill directory. At minimum, read the SKILL.md fully. Check every script, reference, and template file too.

### Step 3: Red Flag Checklist

Reject immediately if you see ANY of these:

```
🚨 REJECT IMMEDIATELY IF YOU SEE:
─────────────────────────────────────────
• curl/wget to unknown or suspicious URLs
• Sends data (API keys, tokens, file contents) to external servers
• Requests credentials, tokens, or API keys you haven't authorized
• Reads ~/.ssh, ~/.aws, ~/.config, credential stores without clear justification
• Accesses MEMORY.md, USER.md, SOUL.md, or identity files
• Uses base64 decode on externally-sourced content
• Uses eval(), exec(), or Function() with dynamic input
• Modifies system files outside the workspace/hermes profile
• Installs packages without listing dependencies
• Network calls to raw IP addresses instead of domains
• Obfuscated code (compressed, encoded, minified with variables like $a, $b)
• Requests elevated/sudo permissions
• Accesses browser cookies or session storage
• Touches credential files (~/.netrc, ~/.git-credentials, etc.)
─────────────────────────────────────────
```

### Step 4: Permission Scope Evaluation

```
Permission audit:
- [ ] What files does it need to read? (Is that scope justified?)
- [ ] What files does it need to write? (Is that scope justified?)
- [ ] What commands does it run? (Are they all standard tools?)
- [ ] Does it need network access? To where? (Is the endpoint trusted?)
- [ ] Is the scope minimal for its stated purpose?
```

### Step 5: Risk Classification

| Risk Level | Examples | Action |
|------------|----------|--------|
| 🟢 LOW | Notes, formatting, weather, emoji helpers | Basic review, install OK |
| 🟡 MEDIUM | File operations, browser automation, external APIs | Full code review required, warn user |
| 🔴 HIGH | Credential access, trading, payment, system config | Human approval required before install |
| ⛔ EXTREME | Security configs, root/sudo, credential theft patterns | Do NOT install |

## Output Format

After vetting, produce a structured report:

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name from SKILL.md name: field]
Source: [ClawdHub / GitHub / user-provided / other]
Author: [if identifiable]
Version: [if available]
───────────────────────────────────────
METRICS:
• Last Updated: [date or "unknown"]
• Files Reviewed: [count]
• Source Reputation: [known / unknown / mixed]
───────────────────────────────────────
RED FLAGS: [None / list each one]

PERMISSIONS NEEDED:
• Files: [list required files or "None stated"]
• Network: [list required endpoints or "None"]
• Commands: [list required commands or "None"]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]

VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]

RECOMMENDATION: [Concise action advice]
═══════════════════════════════════════
```

## Quick Vet Commands

For skills referenced by GitHub URL:

```bash
# Get repo metadata (stars, last updated)
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at, description: .description}'

# List skill files in a repo
curl -s "https://api.github.com/repos/OWNER/REPO/contents/PATH/TO/SKILL" | jq '.[].name'

# Fetch and review SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/BRANCH/skills/SKILL_NAME/SKILL.md"
```

## Trust Hierarchy

| Source | Scrutiny Level |
|--------|---------------|
| Hermes in-repo skills | Minimal (already reviewed) |
| High-star official repos (1000+) | Light review |
| Known, named authors | Moderate review |
| New/unknown sources | Maximum scrutiny |
| Any skill requesting credentials | Human approval mandatory |

## Common Pitfalls

1. **Skipping review because the skill "looks official".** Even skills from "official" channels have been compromised. Always review the code.

2. **Focusing only on SKILL.md and ignoring scripts.** The markdown is the bait; the script is the hook.

3. **Not checking network calls.** A skill that makes no external requests seems safe — but does it phone home?

4. **Assuming short/benign-looking code is safe.** Obfuscation isn't always obvious. Encoded strings, unusual function calls, and dynamic execution are all warning signs.

5. **Forgetting to check transitive dependencies.** If the skill runs `pip install` or `npm install`, those packages are now in your environment too.

6. **Installing during a session you wouldn't want to undo.** If the vet raises suspicion, don't install — ask first. You can always install later.

## Verification Checklist

- [ ] Read ALL files in the skill directory (not just SKILL.md)
- [ ] Ran the Red Flag Checklist — no matches found
- [ ] Checked what files the skill reads/writes
- [ ] Checked what commands the skill runs
- [ ] Verified network endpoints if any
- [ ] Classified risk level and explained reasoning
- [ ] Produced a structured vet report
- [ ] If 🔴 HIGH or ⛔ EXTREME risk: asked human before proceeding
- [ ] Documented the vet outcome for future reference

## Hermes-Specific Notes

**Hermes skill paths to check during scan:**
- In-repo skills: `skills/<category>/` (shipped with hermes-agent)
- User-local skills: `D:\hermes\profiles\work\skills\` or `~/.hermes/skills/`
- Active profile: `D:\hermes\profiles\work\`

**Hermes file access scope:**
- Skills should only read/write within their own skill directory or explicitly documented paths
- Skills should NOT access `D:\hermes\.env`, `~/.ssh/`, credential stores
- Scripts should use standard Python stdlib or documented dependencies only

**Related skills:**
- `dogfood`: QA testing of web apps — different domain, but same "verify before trusting" mindset
- `hermes-agent-skill-authoring`: Skill authoring conventions — useful when you need to write a replacement skill

---

*Paranoia is a feature.* 🔒🦀
