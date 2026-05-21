#!/usr/bin/env python3
"""Validate skill-vetter files."""
import sys

errors = []

# Check required files
import os
for f in ["SKILL.md", "references/red-flags.md", "LICENSE"]:
    if not os.path.exists(f):
        errors.append(f"Missing: {f}")

# Check SKILL.md frontmatter
if os.path.exists("SKILL.md"):
    with open("SKILL.md") as f:
        content = f.read()
    required = ["name:", "description:", "version:", "author:", "license:"]
    for field in required:
        if field not in content:
            errors.append(f"SKILL.md missing: {field}")

# Check red-flags.md non-empty
if os.path.exists("references/red-flags.md"):
    with open("references/red-flags.md") as f:
        lines = len(f.readlines())
    if lines < 20:
        errors.append(f"red-flags.md too short: {lines} lines")

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)
print("All checks passed.")
