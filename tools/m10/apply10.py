#!/usr/bin/env python3
"""Apply OBT milestone 10 (starting OOB rebuild and reserve mobilization) to a Millennium Dawn checkout. Idempotent.

Usage: python3 -I -B apply10.py <repo_root> <out_dir>
"""
import os, shutil, sys
R, O = sys.argv[1:3]
done = []
for root, _d, files in os.walk(O):
    for f in files:
        src = os.path.join(root, f)
        rel = os.path.relpath(src, O)
        dst = os.path.join(R, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        done.append(rel.replace(os.sep, "/"))
p = os.path.join(R, "common", "units", "names_divisions", "TAI_names_divisions.txt")
t = open(p, encoding="utf-8").read()
if "TAI_RES =" not in t:
    t = t.rstrip("\n") + '''

# Operation Blue Tiger: reserve brigades raised by the Reserve Mobilization decisions. Generic numbering only, so no
# reserve brigade number from 2002 or later appears in a 2000 game. Only the locked "Reserve Infantry Brigade" template uses it.
TAI_RES = {
	name = "Reserve Infantry Brigades"
	for_countries = { TAI }
	division_types = { "Militia_Bat" }

	fallback_name = "%d Reserve Infantry Brigade"
}
'''
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    done.append("common/units/names_divisions/TAI_names_divisions.txt (TAI_RES pool)")
print("\n".join(done))
