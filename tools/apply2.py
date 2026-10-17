#!/usr/bin/env python3
"""Apply Operation Blue Tiger milestone 2 (events) to a Millennium Dawn checkout.

Usage: python3 -I -B apply2.py <repo_root> <events_out_dir> [--dry-run]
Run gen.py + apply.py first so the focus tree carries the event calls.
"""
import os
import re
import sys

REPO, OUT = sys.argv[1], sys.argv[2]
DRY = "--dry-run" in sys.argv
MARK2 = "Operation Blue Tiger milestone 2"
done, skipped, problems = [], [], []


def p(*a):
    return os.path.join(REPO, *a)


def rd(path, bom=False):
    with open(path, encoding="utf-8-sig" if bom else "utf-8") as fh:
        return fh.read()


def wr(path, text, bom=False):
    if DRY:
        done.append("(dry) " + os.path.relpath(path, REPO))
        return
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)
    done.append(os.path.relpath(path, REPO))


events_txt = rd(os.path.join(OUT, "Taiwan_Blue_Tiger.txt"))
loc_new = rd(os.path.join(OUT, "events_loc.yml"))
ideas2 = rd(os.path.join(OUT, "ideas2_block.txt"))
sched_lines = rd(os.path.join(OUT, "schedule.txt")).splitlines()
target_ev = p("events", "Taiwan_Blue_Tiger.txt")

# ---- pre-flight
for fn in os.listdir(p("events")):
    fp = p("events", fn)
    if fn.endswith(".txt") and fp != target_ev and "add_namespace = blue_tiger" in rd(fp):
        problems.append(f"namespace blue_tiger already declared in events/{fn}")
new_keys = re.findall(r"^ ([A-Za-z0-9_.]+):", loc_new, re.M)
existing = set()
for fn in os.listdir(p("localisation", "english")):
    if fn.endswith(".yml"):
        txt = rd(p("localisation", "english", fn), bom=True)
        if fn == "MD_focus_TAI_l_english.yml" and " # " + MARK2 in txt:
            txt = txt.split(" # " + MARK2)[0]
        existing.update(re.findall(r"^ ([A-Za-z0-9_.]+):", txt, re.M))
for k in new_keys:
    if k in existing:
        problems.append("loc key exists: " + k)
for idea in re.findall(r"^\t\t(TAI_\w+) = \{", ideas2, re.M):
    ideas_txt = rd(p("common", "ideas", "05_taiwan.txt"))
    if MARK2 not in ideas_txt and re.search(rf"^\t\t{idea} = \{{", ideas_txt, re.M):
        problems.append("idea exists: " + idea)
focus_txt = rd(p("common", "national_focus", "05_taiwan.txt"))
if "blue_tiger.20" not in focus_txt:
    problems.append("focus file does not call the events yet: run gen.py + apply.py first")
if problems:
    print("PRE-FLIGHT FAILED", *problems, sep="\n  ")
    sys.exit(1)

# ---- 1. events file
if os.path.exists(target_ev) and rd(target_ev) == events_txt:
    skipped.append("events file already current")
else:
    wr(target_ev, events_txt)

# ---- 2. ideas
fp = p("common", "ideas", "05_taiwan.txt")
txt = rd(fp)
if MARK2 in txt:
    skipped.append("milestone 2 ideas present")
else:
    tail = "\t}\n}\n"
    assert txt.endswith(tail)
    wr(fp, txt[: -len(tail)] + ideas2 + tail)

# ---- 3. localisation
fp = p("localisation", "english", "MD_focus_TAI_l_english.yml")
txt = rd(fp, bom=True)
if " # " + MARK2 in txt:
    skipped.append("milestone 2 localisation present")
else:
    wr(fp, txt.rstrip("\n") + "\n # " + MARK2 + "\n" + loc_new.rstrip("\n") + "\n", bom=True)

# ---- 4. yearly schedule
fp = p("common", "scripted_effects", "00_yearly_effects.txt")
txt = rd(fp)
if "blue_tiger." in txt:
    skipped.append("schedule present")
else:
    by_year, cur = {}, None
    for line in sched_lines:
        if re.fullmatch(r"\d{4}", line):
            cur = int(line)
            by_year[cur] = []
        else:
            by_year[cur].append(line)
    for y, lines in by_year.items():
        if y == 2000:
            anchor = "\tTAI = {\n\t\tcountry_event = { id = taiwan.18 days = 30 random_days = 150 }\n"
            assert txt.count(anchor) == 1, "2000 anchor"
            txt = txt.replace(anchor, anchor + "\n".join(lines) + "\n")
        else:
            anchor = f"trigger_year_{y}_events = {{\n"
            assert txt.count(anchor) == 1, f"{y} anchor"
            txt = txt.replace(anchor, anchor + "\tTAI = {\n" + "\n".join(lines) + "\n\t}\n")
    wr(fp, txt)

print("WROTE:", *done, sep="\n  ")
print("SKIPPED:", *skipped, sep="\n  ")
