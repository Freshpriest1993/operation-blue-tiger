# Operation Blue Tiger: section layout (Diplomacy, Politics, Domestic, Economy, Defence).
#
# Layout only: no focus, prerequisite or reward changes. The National Army is laid out as two blocks,
# "core" (civil-military reform, manpower, procurement) and "doctrine" (from Reassess Defense-in-Depth),
# so the planned doctrine paths and masteries can sit below the core instead of widening the tree.
# Branch offsets (BRANCH_NUDGE) were chosen with tools/sections/optimize_layout.py to reduce lines between
# branches and line crossings while keeping every section in place.
#
# Loaded at the end of spec.py:  import sections_spec; sections_spec.integrate(sys.modules[__name__])
# Set OBT_SKIP_SECTIONS=1 to build with the previous 88x36 layout.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TIERS = [["pl", "su", "ss"],
         ["dpp", "tsu", "gpt", "kmt", "pfp"],
         [["as", ("sp", "png")], ["df", "isl"], "bt", ["na", "nd"]]]


def split_national_army(S):
    na = next(b for b in S.BRANCHES if b["key"] == "na")
    children = {}
    for f in na["focuses"]:
        for p in f["pre"]:
            for q in (p if isinstance(p, tuple) else (p,)):
                children.setdefault(q, []).append(f["id"])
    sub, stack = set(), ["TAI_na_reassess_did"]
    while stack:
        x = stack.pop()
        if x not in sub:
            sub.add(x)
            stack += children.get(x, [])
    nd = dict(na)
    nd["key"] = "nd"
    nd["name"] = na["name"] + ": Doctrine"
    nd["focuses"] = [f for f in na["focuses"] if f["id"] in sub]
    na["focuses"] = [f for f in na["focuses"] if f["id"] not in sub]
    S.BRANCHES.insert(S.BRANCHES.index(na) + 1, nd)


def integrate(S):
    split_national_army(S)
    S.TIERS = TIERS
    S.TIER_GAP = 3
    S.TIER_VGAP = 2
    with open(os.path.join(HERE, "nudge.json"), encoding="utf-8") as fh:
        S.BRANCH_NUDGE = {k: tuple(v) for k, v in json.load(fh).items()}
    cpos = os.path.join(HERE, "continuous.json")
    if os.path.exists(cpos):
        with open(cpos, encoding="utf-8") as fh:
            S.CONTINUOUS_POS = tuple(json.load(fh))
