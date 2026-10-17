#!/usr/bin/env python3
"""Generate Operation Blue Tiger milestone-2 events, localisation and schedule snippets.

Usage: python3 -I -B events_gen.py <repo_root> <out_dir>
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events_spec as S  # noqa: E402

REPO, OUT = sys.argv[1], sys.argv[2]
NS = S.NS
VARS = {
    "usconf": "TAI_us_confidence", "milconf": "TAI_military_confidence", "reform": "TAI_reform_capacity",
    "dep": "TAI_mainland_dependence", "chips": "TAI_semiconductor_security", "ptn": "TAI_pressure_to_negotiate",
    "identity": "TAI_taiwanese_identity", "coord": "TAI_national_coordination",
}
CHIVARS = {"trust": "CHI_TAI_trust", "tension": "CHI_taiwan_strait_tension", "ussupport": "CHI_taiwan_us_support"}
errors = []


def fx(tok, t):
    k, _, rest = tok.partition(":")
    a = rest.split(":") if rest else []
    if k in ("raw", "rawfx"):
        return [t + line for line in rest.split("\n")]
    if k == "pp":
        return [f"{t}add_political_power = {a[0]}"]
    if k == "stab":
        return [f"{t}add_stability = {a[0]}"]
    if k == "ws":
        return [f"{t}add_war_support = {a[0]}"]
    if k == "army_xp":
        return [f"{t}army_experience = {a[0]}"]
    if k == "money":
        return [f"{t}set_temp_variable = {{ treasury_change = {a[0]} }}", f"{t}modify_treasury_effect = yes"]
    if k == "var":
        v = VARS[a[0]]
        return [f"{t}add_to_variable = {{ {v} = {a[1]} tooltip = {v}_tt }}", f"{t}clamp_variable = {{ var = {v} min = 0 max = 100 }}"]
    if k == "chi":
        v = CHIVARS[a[0]]
        return [f"{t}if = {{", f"{t}\tlimit = {{ country_exists = CHI }}", f"{t}\tCHI = {{",
                f"{t}\t\tadd_to_variable = {{ {v} = {a[1]} tooltip = {v}_tt }}",
                f"{t}\t\tclamp_variable = {{ var = {v} min = 0 max = 100 }}", f"{t}\t}}", f"{t}}}"]
    if k == "timed":
        return [f"{t}add_timed_idea = {{ idea = {a[0]} days = {a[1]} }}"]
    if k == "party":
        return [f"{t}add_to_variable = {{ party_pop_array^{a[0]} = {a[1]} }}", f"{t}recalculate_party = yes"]
    if k == "flag":
        return [f"{t}set_country_flag = {a[0]}"]
    if k == "fire":
        return [f"{t}hidden_effect = {{ country_event = {{ id = {NS}.{a[0]} days = {a[1]} }} }}"]
    errors.append(f"unknown token {tok}")
    return []


def esc(s):
    return s.replace('"', '\\"')


ev, loc, sched = [], [], {}
ev.append("###########################")
ev.append("# Operation Blue Tiger events")
ev.append("###########################")
ev.append("")
ev.append(f"add_namespace = {NS}")
ev.append("")
letters = "abcdefgh"
for e in S.EVENTS:
    eid = f"{NS}.{e['n']}"
    ev.append("country_event = {")
    ev.append(f"\tid = {eid}")
    ev.append(f"\ttitle = {eid}.t")
    loc.append(f' {eid}.t: "{esc(e["title"])}"')
    if isinstance(e["desc"], str):
        ev.append(f"\tdesc = {eid}.d")
        loc.append(f' {eid}.d: "{esc(e["desc"])}"')
    else:
        for suf, trig, text in e["desc"]:
            ev.append(f"\tdesc = {{ text = {eid}.d_{suf} trigger = {{ {trig} }} }}")
            loc.append(f' {eid}.d_{suf}: "{esc(text)}"')
    ev.append(f"\tpicture = {e['picture']}")
    ev.append("\tis_triggered_only = yes")
    if e["sched"]:
        ev.append("\tfire_only_once = yes")
    ev.append("")
    ev.append("\ttrigger = {")
    for line in e["trigger"].split("\n"):
        ev.append("\t\t" + line.strip())
    ev.append("\t}")
    ev.append("")
    for i, o in enumerate(e["options"]):
        key = f"{eid}.{letters[i]}"
        ev.append("\toption = {")
        ev.append(f"\t\tname = {key}")
        if o["trigger"]:
            ev.append(f"\t\ttrigger = {{ {o['trigger']} }}")
        ev.append(f'\t\tlog = "[GetDateText]: [This.GetName]: {key} executed"')
        for tok in o["eff"]:
            ev.extend(fx(tok, "\t\t"))
        ev.append("\t\tai_chance = {")
        ev.append(f"\t\t\tbase = {o['ai']}")
        for m in o["aimod"]:
            ev.append("\t\t\t" + m)
        ev.append("\t\t}")
        ev.append("\t}")
        ev.append("")
        loc.append(f' {key}: "{esc(o["text"])}"')
    if ev[-1] == "":
        ev.pop()
    ev.append("}")
    ev.append("")
    if e["sched"]:
        y, d = e["sched"]
        sched.setdefault(y, []).append(f"\t\tcountry_event = {{ id = {eid} days = {d} }}")

for k, v in S.IDEAS_LOC + S.IDEAS_LOC_M3:
    loc.append(f' {k}: "{v}"')

# sanity checks
for line in loc:
    if "—" in line:
        errors.append("em dash in " + line[:40])
picture_names = set()
for fn in os.listdir(os.path.join(REPO, "interface")):
    if fn.endswith(".gfx"):
        with open(os.path.join(REPO, "interface", fn), encoding="utf-8", errors="ignore") as fh:
            picture_names.update(re.findall(r'name\s*=\s*"(GFX_[A-Za-z0-9_]+)"', fh.read()))
for e in S.EVENTS:
    if e["picture"] not in picture_names:
        errors.append(f"{NS}.{e['n']}: picture {e['picture']} not found")

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "Taiwan_Blue_Tiger.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(ev).rstrip("\n") + "\n")
with open(os.path.join(OUT, "events_loc.yml"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(loc) + "\n")
with open(os.path.join(OUT, "ideas2_block.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(S.IDEAS_BLOCK)
with open(os.path.join(OUT, "ideas3_block.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(S.IDEAS_BLOCK_M3)
with open(os.path.join(OUT, "schedule.txt"), "w", encoding="utf-8", newline="\n") as fh:
    for y in sorted(sched):
        fh.write(f"{y}\n" + "\n".join(sched[y]) + "\n")
print(f"events: {len(S.EVENTS)}, loc keys: {len(loc)}, scheduled years: {sorted(sched)}")
for x in errors:
    print("ERROR", x)
sys.exit(1 if errors else 0)
