#!/usr/bin/env python3
"""Generate Operation Blue Tiger milestone-1 script and localisation from spec.py.

Usage: python3 gen.py <repo_root> <out_dir>
Reads the repo only to validate icons; writes generated text to out_dir.
"""
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spec  # noqa: E402
import layout  # noqa: E402

REPO, OUT = sys.argv[1], sys.argv[2]

VARS = {
    "usconf": ("TAI_us_confidence", "U.S. Confidence in Taipei", "+"),
    "milconf": ("TAI_military_confidence", "Military Confidence", "+"),
    "reform": ("TAI_reform_capacity", "Reform Capacity", "+"),
    "dep": ("TAI_mainland_dependence", "Mainland Economic Dependence", "-"),
    "chips": ("TAI_semiconductor_security", "Semiconductor Supply Security", "+"),
    "ptn": ("TAI_pressure_to_negotiate", "Pressure to Negotiate", "-"),
    "identity": ("TAI_taiwanese_identity", "Taiwan-Centered Identity", "Y"),
    "coord": ("TAI_national_coordination", "National Coordination Capacity", "+"),
}
CHIVARS = {
    "trust": "CHI_TAI_trust",
    "tension": "CHI_taiwan_strait_tension",
    "ussupport": "CHI_taiwan_us_support",
}
POSTURES = {
    2: "TAI_posture_active_defense",
    3: "TAI_posture_hard_roc",
    4: "TAI_posture_asymmetric",
    5: "TAI_posture_hybrid",
}
POSTURE_CLEAR = ["TAI_did_legacy", "TAI_did_legacy_reformed"] + list(POSTURES.values())
FALLBACK_ICON = "Generic_Command_Power"

PATH_GROUPS = [
    ("TAI_ai_historical_path = yes", "TAI_ai_not_historical_path",
     ["TAI_bt_blue_tiger", "TAI_na_hard_roc", "TAI_na_volunteer_reserve_split", "TAI_pl_keep_allies"]),
    ("has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH", "TAI_ai_not_accommodation_path",
     ["TAI_bt_accommodation", "TAI_as_stabilization", "TAI_as_structured_restraint", "TAI_as_cbms", "TAI_as_peace_accord"]),
    ("has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH", "TAI_ai_not_island_fortress_path",
     ["TAI_bt_island_fortress", "TAI_as_go_slow", "TAI_as_tighten_management", "TAI_na_extended_conscription", "TAI_na_odc",
      "TAI_na_fortress_taiwan", "TAI_pl_india", "TAI_pl_india_tier1", "TAI_pl_india_tier2", "TAI_pl_india_market", "TAI_pl_india_partnership"]),
]
OWNER = {fid: (own, nott) for own, nott, ids in PATH_GROUPS for fid in ids}
DID = "OR = { has_idea = TAI_did_legacy has_idea = TAI_did_legacy_reformed }"
THREAT = ("ai_is_threatened = yes", 2)
AI_EXTRA = {
    "TAI_na_reserve_reform": [("has_idea = TAI_uneven_reserves", 3)],
    "TAI_na_absorption": [("has_idea = TAI_limited_absorption", 3)],
    "TAI_na_hard_roc": [(DID, 2)],
    "TAI_na_odc": [(DID, 2)],
    "TAI_na_hybrid": [(DID, 2)],
    "TAI_na_rebuild_shield": [THREAT],
    "TAI_na_layered_air_defense": [THREAT],
    "TAI_na_harden_island": [THREAT],
    "TAI_na_mine_approaches": [THREAT],
    "TAI_na_mobile_fires": [THREAT],
    "TAI_na_territorial_defense": [THREAT],
    "TAI_na_fighter_fleet": [THREAT],
    "TAI_bt_wan_an": [THREAT],
    "TAI_bt_emergency_doctrine": [THREAT],
}

errors = []
warnings = []


def load_icons():
    names = set()
    for fn in ("goals.gfx",):
        with open(os.path.join(REPO, "interface", fn), encoding="utf-8", errors="ignore") as fh:
            names.update(re.findall(r'name\s*=\s*"([A-Za-z0-9_]+)"', fh.read()))
    return names


def num(v):
    s = ("%g" % v)
    return s


def expand_effect(tok, ind):
    t = "\t" * ind
    k, _, rest = tok.partition(":")
    if k == "raw":
        return [t + line for line in rest.split("\n")]
    a = rest.split(":") if rest else []
    if k == "pp":
        return [f"{t}add_political_power = {a[0]}"]
    if k == "stab":
        return [f"{t}add_stability = {a[0]}"]
    if k == "ws":
        return [f"{t}add_war_support = {a[0]}"]
    if k in ("army_xp", "navy_xp", "air_xp"):
        return [f"{t}{k.replace('_xp', '_experience')} = {a[0]}"]
    if k == "money":
        return [f"{t}set_temp_variable = {{ treasury_change = {a[0]} }}", f"{t}modify_treasury_effect = yes"]
    if k == "corr":
        return [f"{t}decrease_corruption = yes"]
    if k == "var":
        var = VARS[a[0]][0]
        return [f"{t}add_to_variable = {{ {var} = {a[1]} tooltip = {var}_tt }}",
                f"{t}clamp_variable = {{ var = {var} min = 0 max = 100 }}"]
    if k == "chi":
        var = CHIVARS[a[0]]
        return [f"{t}if = {{",
                f"{t}\tlimit = {{ country_exists = CHI }}",
                f"{t}\tCHI = {{",
                f"{t}\t\tadd_to_variable = {{ {var} = {a[1]} tooltip = {var}_tt }}",
                f"{t}\t\tclamp_variable = {{ var = {var} min = 0 max = 100 }}",
                f"{t}\t}}",
                f"{t}}}"]
    if k == "idea":
        return [f"{t}add_ideas = {a[0]}"]
    if k == "rmidea":
        return [f"{t}if = {{ limit = {{ has_idea = {a[0]} }} remove_ideas = {a[0]} }}"]
    if k == "timed":
        return [f"{t}add_timed_idea = {{ idea = {a[0]} days = {a[1]} }}"]
    if k == "posture":
        n = int(a[0])
        out = [f"{t}set_variable = {{ TAI_defense_posture = {n} }}"]
        for idea in POSTURE_CLEAR:
            if idea != POSTURES[n]:
                out.append(f"{t}if = {{ limit = {{ has_idea = {idea} }} remove_ideas = {idea} }}")
        out.append(f"{t}add_ideas = {POSTURES[n]}")
        return out
    if k == "tech":
        return [f"{t}add_tech_bonus = {{ name = {CURRENT['id']} bonus = {a[1]} uses = {a[2]} category = {a[0]} }}"]
    if k == "build":
        return [f"{t}{a[0]} = yes"]
    if k == "party":
        return [f"{t}add_to_variable = {{ party_pop_array^{a[0]} = {a[1]} }}", f"{t}recalculate_party = yes"]
    if k == "opinion":
        return [f"{t}add_opinion_modifier = {{ target = {a[0]} modifier = {a[1]} }}"]
    if k == "flag":
        return [f"{t}set_country_flag = {a[0]}"]
    errors.append(f"{CURRENT['id']}: unknown effect token {tok}")
    return []


def expand_avail(tok):
    if isinstance(tok, tuple):
        return ["OR = {"] + ["\t" + x for alt in tok for x in expand_avail(alt)] + ["}"]
    k, _, rest = tok.partition(":")
    if k == "raw":
        return rest.split("\n")
    if tok == "transfer":
        return ["date > 2000.3.24"]
    if tok == "dpp":
        return ["TAI_pan_green_in_power = yes"]
    if tok == "kmt":
        return ["TAI_kmt_in_power = yes"]
    if tok == "pfp":
        return ["TAI_pfp_in_power = yes"]
    if tok == "blue":
        return ["TAI_pan_blue_in_power = yes"]
    if tok == "ly":
        return ["TAI_can_pass_legislation = yes"]
    m = re.match(r"date>(\S+)", tok)
    if m:
        return [f"date > {m.group(1)}"]
    errors.append(f"{CURRENT['id']}: unknown availability token {tok}")
    return []


CURRENT = {}


def main():
    icons = load_icons()
    all_focus = {}
    for b in spec.BRANCHES:
        for f in b["focuses"]:
            if f["id"] in all_focus:
                errors.append(f"duplicate focus id {f['id']}")
            all_focus[f["id"]] = (b, f)

    # symmetric mutual exclusion
    excl = defaultdict(set)
    for fid, (_, f) in all_focus.items():
        for o in f["excl"]:
            if o not in all_focus:
                errors.append(f"{fid}: excl target {o} missing")
            excl[fid].add(o)
            excl[o].add(fid)

    for fid, (_, f) in all_focus.items():
        for p in f["pre"]:
            for q in (p if isinstance(p, tuple) else (p,)):
                if q not in all_focus:
                    errors.append(f"{fid}: prerequisite {q} missing")

    # layout: each branch as a compact tree, packed in two tiers
    positions, sizes, _, _ = layout.tree_layout(spec.BRANCHES, spec.TIERS)
    roots = {b["key"]: b["focuses"][0]["id"] for b in spec.BRANCHES}
    for b in spec.BRANCHES:
        b["width"] = sizes[b["key"]][0]

    # emit focus file
    L = []
    L.append("focus_tree = {")
    L.append("\tid = taiwan_focus")
    L.append("")
    L.append("\tcountry = {")
    L.append("\t\tfactor = 0")
    L.append("\t\tmodifier = {")
    L.append("\t\t\tadd = 25")
    L.append("\t\t\ttag = TAI")
    L.append("\t\t}")
    L.append("\t}")
    L.append("")
    L.append("\tcontinuous_focus_position = { x = 50 y = 3700 }")
    L.append("")
    loc = []
    for b in spec.BRANCHES:
        root = roots[b["key"]]
        rx, ry = positions[root]
        for f in b["focuses"]:
            CURRENT.clear()
            CURRENT.update(f)
            fid = f["id"]
            icon = f["icon"]
            if icon not in icons:
                warnings.append(f"{fid}: icon {icon} not found, using {FALLBACK_ICON}")
                icon = FALLBACK_ICON
            x, y = positions[fid]
            L.append("\tfocus = {")
            L.append(f"\t\tid = {fid}")
            L.append(f"\t\ticon = {icon}")
            if fid == root:
                L.append(f"\t\tx = {x}")
                L.append(f"\t\ty = {y}")
            else:
                L.append(f"\t\tx = {x - rx}")
                L.append(f"\t\ty = {y - ry}")
                L.append(f"\t\trelative_position_id = {root}")
            if f["days"] % 7:
                errors.append(f"{fid}: days not a multiple of 7")
            cost = min(f["days"], 70) // 7
            L.append(f"\t\tcost = {cost}")
            for p in f["pre"]:
                grp = p if isinstance(p, tuple) else (p,)
                L.append("\t\tprerequisite = { " + " ".join(f"focus = {q}" for q in grp) + " }")
            if excl[fid]:
                L.append("\t\tmutually_exclusive = { " + " ".join(f"focus = {q}" for q in sorted(excl[fid])) + " }")
            filt = f["filt"] or b["filters"]
            L.append("\t\tsearch_filters = { " + " ".join(filt) + " }")
            for tag in f.get("war_with", []):
                L.append(f"\t\twill_lead_to_war_with = {tag}")
            if f.get("allow"):
                L.append("\t\tallow_branch = {")
                for a in f["allow"]:
                    for line in expand_avail(a):
                        L.append("\t\t\t" + line)
                L.append("\t\t}")
            if f["avail"]:
                L.append("\t\tavailable = {")
                for a in f["avail"]:
                    for line in expand_avail(a):
                        L.append("\t\t\t" + line)
                L.append("\t\t}")
            L.append("\t\tcompletion_reward = {")
            L.append(f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Focus {fid}"')
            spends = False
            for e in f["eff"]:
                if e.startswith("money:-") or e.startswith("build:"):
                    spends = True
                L.extend(expand_effect(e, 3))
            L.append("\t\t}")
            L.append("\t\tai_will_do = {")
            L.append(f"\t\t\tbase = {f['ai']}")
            for trig, fac in AI_EXTRA.get(fid, []):
                L.append(f"\t\t\tmodifier = {{ factor = {fac} {trig} }}")
            for inner in f.get("aimods", []):
                L.append(f"\t\t\tmodifier = {{ {inner} }}")
            staff = {"industrial_complex": "can_staff_an_industrial_complex", "arms_factory": "can_staff_an_arms_industry", "dockyard": "can_staff_an_dockyard"}
            for key, trig in staff.items():
                if any(e.startswith("build:") and key in e for e in f["eff"]):
                    L.append("\t\t\tmodifier = {")
                    L.append("\t\t\t\tfactor = 0")
                    L.append(f"\t\t\t\t{trig} = no")
                    L.append("\t\t\t}")
            if spends:
                L.append("\t\t\tmodifier = {")
                L.append("\t\t\t\tfactor = 0")
                L.append("\t\t\t\thas_active_mission = bankruptcy_incoming_collapse")
                L.append("\t\t\t}")
            if fid in OWNER:
                own, nott = OWNER[fid]
                L.append(f"\t\t\tmodifier = {{ factor = 25 {own} }}")
                L.append(f"\t\t\tmodifier = {{ factor = 0 {nott} = yes }}")
            L.append("\t\t}")
            L.append("\t}")
            L.append("")
            name_esc = f["name"].replace('"', '\\"')
            desc_esc = f["desc"].replace('"', '\\"')
            loc.append(f' {fid}: "{name_esc}"')
            loc.append(f' {fid}_desc: "{desc_esc}"')
            if "§" in f["name"] or "—" in f["desc"] or "—" in f["name"]:
                errors.append(f"{fid}: forbidden character in loc")
    L.append("}")

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "05_taiwan.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    for key, text in getattr(spec, "EXTRA_LOC", []):
        loc.append(f' {key}: "{text}"')
    with open(os.path.join(OUT, "focus_loc.yml"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(loc) + "\n")
    var_loc = []
    for key, (var, label, sign) in VARS.items():
        fmt = {"+": "+=0", "-": "-=0", "Y": "Y=0"}[sign]
        var_loc.append(f' {var}: "§Y{label}§!"')
        var_loc.append(f' {var}_tt: "${var}$: $RIGHT|{fmt}$"')
    with open(os.path.join(OUT, "var_loc.yml"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(var_loc) + "\n")

    with open(os.path.join(OUT, "report.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"focuses: {len(all_focus)}\n")
        for b in spec.BRANCHES:
            fh.write(f"branch {b['key']}: {len(b['focuses'])} focuses, width {b['width']}\n")
        for w in warnings:
            fh.write("WARN " + w + "\n")
        for e in errors:
            fh.write("ERROR " + e + "\n")
    print(open(os.path.join(OUT, "report.txt")).read())
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
