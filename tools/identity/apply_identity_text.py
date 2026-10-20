#!/usr/bin/env python3
"""Add the Pragmatic Sovereignty spirit and the text of the two National Identity focuses to existing files.

Exact, idempotent insertions: each one is skipped if its new text is already present, and the script
stops with an error if the anchor text is missing or not unique.

Usage: python3 -B apply_identity_text.py <millennium_dawn_root> [<tools_dir>]
"""
import os
import sys

OWN_PATH_IDEA = """\t\tTAI_dpp_own_path = {
\t\t\tpicture = democracy
\t\t\tallowed_civil_war = { always = yes }
\t\t\tmodifier = {
\t\t\t\tpolitical_power_gain = 0.25
\t\t\t\tstability_factor = 0.1
\t\t\t\tresearch_speed_factor = 0.05
\t\t\t\twar_support_factor = 0.05
\t\t\t}
\t\t}
"""
# Held alongside DPP programme II (the capstone does not remove it). Provisional values.
PS_IDEA = """\t\tTAI_dpp_pragmatic_sovereignty = {
\t\t\tpicture = democracy
\t\t\tallowed_civil_war = { always = yes }
\t\t\tmodifier = {
\t\t\t\tstability_factor = 0.05
\t\t\t\tforeign_influence_defense_modifier = 0.10
\t\t\t\ttrade_opinion_factor = 0.05
\t\t\t}
\t\t}
"""
FOCUS_ANCHOR = ' TAI_su_dpp_own_path_desc: "A democracy that chose its own government, settled its own past and decides its own future."\n'
FOCUS_LOC = (
    ' TAI_su_dpp_roc_taiwan: "The Republic of China (Taiwan)"\n'
    ' TAI_su_dpp_roc_taiwan_desc: "Taiwan is already a sovereign state, and under the constitution its name is the Republic of China. No formal change is needed, and our partners abroad can count on us not to alter the status quo."\n'
    ' TAI_su_dpp_pragmatic_sovereignty: "Pragmatic Sovereignty"\n'
    ' TAI_su_dpp_pragmatic_sovereignty_desc: "Our sovereignty rests on our democracy, not on a declaration. We will defend it through strong institutions and trusted partners abroad, without needless escalation."\n'
)
IDEA_ANCHOR = ' TAI_dpp_own_path_desc: "A democracy that chose its own government and decides its own future."\n'
IDEA_LOC = (
    ' TAI_dpp_pragmatic_sovereignty: "Pragmatic Sovereignty"\n'
    ' TAI_dpp_pragmatic_sovereignty_desc: "Taiwan governs itself as a sovereign democracy and works with its partners abroad, without needless confrontation."\n'
)

EDITS = {
    "common/ideas/05_taiwan.txt": [(OWN_PATH_IDEA, OWN_PATH_IDEA + PS_IDEA)],
    "localisation/english/MD_focus_TAI_l_english.yml": [(FOCUS_ANCHOR, FOCUS_ANCHOR + FOCUS_LOC), (IDEA_ANCHOR, IDEA_ANCHOR + IDEA_LOC)],
}
SPEC_EDITS = [
    (OWN_PATH_IDEA, OWN_PATH_IDEA + PS_IDEA),
    ('    ("TAI_dpp_own_path_desc", "A democracy that chose its own government and decides its own future."),\n',
     '    ("TAI_dpp_own_path_desc", "A democracy that chose its own government and decides its own future."),\n'
     '    ("TAI_dpp_pragmatic_sovereignty", "Pragmatic Sovereignty"),\n'
     '    ("TAI_dpp_pragmatic_sovereignty_desc", "Taiwan governs itself as a sovereign democracy and works with its partners abroad, without needless confrontation."),\n'),
]


def apply(path, edits):
    with open(path, encoding="utf-8-sig") as fh:
        raw = fh.read()
    bom = open(path, "rb").read(3) == b"\xef\xbb\xbf"
    s, n = raw, 0
    for old, new in edits:
        if new in s:
            continue
        if s.count(old) != 1:
            sys.exit(f"ERROR {path}: anchor found {s.count(old)} times: {old[:60]!r}")
        s = s.replace(old, new)
        n += 1
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(s)
    print(f"{path}: {n} edit(s)")


if __name__ == "__main__":
    root = sys.argv[1]
    for rel, edits in EDITS.items():
        apply(os.path.join(root, rel), edits)
    if len(sys.argv) > 2:
        apply(os.path.join(sys.argv[2], "events_spec.py"), SPEC_EDITS)
