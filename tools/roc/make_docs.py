#!/usr/bin/env python3
"""Write archive/roc_dev/ROC_DEV_MAPPING.md from roc_spec.MAPPING. Usage: python3 -B make_docs.py <out_dir>"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import roc_spec as R  # noqa: E402

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
rows = ["# RoC-development focus mapping", "",
        "Every focus in AUG's RoC-development tree (`common/national_focus/taiwan.txt`, upstream/RoC-development `ceb1a0c1f5`) and where it lives in the unified Taiwan tree.",
        "", "Classifications:", "",
        "- **Retain unchanged**: the focus keeps its ID, reward and text, with a place in the OBT layout and a date gate where history needs one.",
        "- **Integrate into OBT focus**: an OBT focus already covers the same event or policy; AUG's unique reward is added to it and the AUG ID is retired. A few integrated focuses keep their ID as a follow-on focus inside the OBT line (noted below).",
        "- **Rework (alt-history)**: the focus keeps its ID and reward but is gated, re-routed or adjusted to fit OBT's systems and the Pressure Is Not Control rule.",
        "- **Archive / optional**: the focus keeps its ID and reward as written, hidden unless an off-by-default game rule is switched on.",
        ""]
counts = {}
for m in R.MAPPING:
    counts[m[2]] = counts.get(m[2], 0) + 1
rows.append("| Classification | Focuses |")
rows.append("| --- | --- |")
for k in (R.INT, R.REW, R.RET, R.OPT):
    rows.append(f"| {k} | {counts.get(k, 0)} |")
rows.append(f"| **Total** | **{len(R.MAPPING)}** |")
rows.append("")
grp = None
for i, (fid, g, cls, dest, note) in enumerate(R.MAPPING, 1):
    if g != grp:
        grp = g
        rows += ["", f"## {g}", "", "| # | AUG focus ID | Name | Classification | Destination in the unified tree | Notes |", "| --- | --- | --- | --- | --- | --- |"]
    nm = R._clean(R.AUG_LOC.get(fid, fid))
    rows.append(f"| {i} | `{fid}` | {nm} | {cls} | {dest} | {note} |")
open(os.path.join(out, "ROC_DEV_MAPPING.md"), "w", encoding="utf-8", newline="\n").write("\n".join(rows) + "\n")
print("mapping rows", len(R.MAPPING), counts)
