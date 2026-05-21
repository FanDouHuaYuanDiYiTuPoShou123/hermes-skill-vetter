#!/usr/bin/env python3
"""
Skill Vet Report Template Generator
Generates a structured vetting report for a skill.
"""

import sys
import json
from datetime import datetime


def generate_report(
    skill_name: str,
    source: str,
    author: str = "unknown",
    version: str = "unknown",
    files_reviewed: int = 0,
    red_flags: list[str] | None = None,
    permissions_files: list[str] | None = None,
    permissions_network: list[str] | None = None,
    permissions_commands: list[str] | None = None,
    risk_level: str = "UNKNOWN",
    verdict: str = "UNKNOWN",
    recommendation: str = "",
    notes: str = "",
) -> str:
    """Generate a structured SKILL VETTING REPORT."""

    if red_flags is None:
        red_flags = []
    if permissions_files is None:
        permissions_files = []
    if permissions_network is None:
        permissions_network = []
    if permissions_commands is None:
        permissions_commands = []

    risk_icons = {
        "LOW": "🟢 LOW",
        "MEDIUM": "🟡 MEDIUM",
        "HIGH": "🔴 HIGH",
        "EXTREME": "⛔ EXTREME",
    }

    verdict_icons = {
        "SAFE": "✅ SAFE TO INSTALL",
        "CAUTION": "⚠️ INSTALL WITH CAUTION",
        "DANGER": "❌ DO NOT INSTALL",
    }

    flag_lines = "\n".join(f"  • {f}" for f in red_flags) or "  • None"
    file_lines = "\n".join(f"  • {f}" for f in permissions_files) or "  • None"
    net_lines = "\n".join(f"  • {f}" for f in permissions_network) or "  • None"
    cmd_lines = "\n".join(f"  • {f}" for f in permissions_commands) or "  • None"

    report = f"""================================================================================
SKILL VETTING REPORT
================================================================================
Skill: {skill_name}
Source: {source}
Author: {author}
Version: {version}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------------------------------------------------------
METRICS:
  • Files Reviewed: {files_reviewed}
  • Source Reputation: {"known" if author != "unknown" else "unknown"}
--------------------------------------------------------------------------------
RED FLAGS:{flag_lines}

PERMISSIONS NEEDED:
  Files:{file_lines}
  Network:{net_lines}
  Commands:{cmd_lines}
--------------------------------------------------------------------------------
RISK LEVEL: {risk_icons.get(risk_level, risk_level)}

VERDICT: {verdict_icons.get(verdict, verdict)}

RECOMMENDATION: {recommendation}
================================================================================
{notes}
"""

    return report


if __name__ == "__main__":
    # Demo
    report = generate_report(
        skill_name="example-skill",
        source="GitHub",
        author="unknown-author",
        version="1.0.0",
        files_reviewed=3,
        red_flags=["curl to unknown domain", "eval() with dynamic input"],
        permissions_files=["~/.hermes/skills/example/"],
        permissions_network=["https://api.example.com"],
        permissions_commands=["pip install"],
        risk_level="HIGH",
        verdict="DANGER",
        recommendation="Do not install. The skill makes network calls to an untrusted domain and uses eval().",
        notes="Reviewed 2025-05-22",
    )
    print(report)
