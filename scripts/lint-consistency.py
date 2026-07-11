#!/usr/bin/env python3
"""Consistency lint for the krukit skills tree (HARNESS-IMPROVEMENTS item 4).

Checks every skills/*/SKILL.md for: valid frontmatter, correct "Stage N of 7"
numbering, duplicated flow-state templates matching the canonical structure
(krukit-flow), and referenced local paths that exist. Exit 1 on any issue.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
STAGES = ["recon", "grill", "design", "plan", "act", "verify", "review"]
STAGE_ROWS = [f"- [ ] {i} {s}" for i, s in enumerate(STAGES, 1)]

errors = []


def err(path: Path, msg: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


checked = 0
for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
    checked += 1
    text = skill_md.read_text()

    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(skill_md, "missing frontmatter")
        continue
    name = re.search(r"^name:\s*(\S+)", m.group(1), re.M)
    desc = re.search(r"^description:\s*(.+)", m.group(1), re.M)
    if not name or name.group(1) != skill_md.parent.name:
        err(skill_md, f"frontmatter name != directory ({name.group(1) if name else 'absent'})")
    if not desc or not desc.group(1).strip():
        err(skill_md, "frontmatter description missing or empty")

    stage_name = skill_md.parent.name.removeprefix("krukit-")
    if stage_name in STAGES:
        expect = STAGES.index(stage_name) + 1
        sm = re.search(r"Stage (\d) of 7", text)
        if not sm or int(sm.group(1)) != expect:
            err(skill_md, f"stage numbering: expected 'Stage {expect} of 7', found "
                          f"{'Stage ' + sm.group(1) + ' of 7' if sm else 'none'}")

    tpl_marker = "# Krukit Flow: <feature-slug>"
    if tpl_marker in text:
        start = text.index(tpl_marker)
        fence = text.find("```", start)
        block = text[start:fence if fence != -1 else start + 600]
        if "Started:" not in block:
            err(skill_md, "flow-state template: missing 'Started:' line")
        if not re.search(r"^\s*Task:", block, re.M):
            err(skill_md, "flow-state template: missing 'Task:' line (drifted from canonical in krukit-flow)")
        for row in STAGE_ROWS:
            if row not in block:
                err(skill_md, f"flow-state template: missing row '{row}'")

    for ref in re.findall(r"`(references/[^`\s]+)`", text):
        if not (skill_md.parent / ref).exists():
            err(skill_md, f"referenced path does not exist: {ref}")

if errors:
    print("\n".join(errors))
    print(f"\nFAIL: {len(errors)} issue(s) in {checked} skills")
    sys.exit(1)
print(f"OK: {checked} skills checked, no consistency issues")
