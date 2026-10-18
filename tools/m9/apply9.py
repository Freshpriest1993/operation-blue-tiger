#!/usr/bin/env python3
"""Apply OBT milestone 9 to a Millennium Dawn checkout (idempotent).

Usage: python3 -I -B apply9.py <repo_root> <build_out_dir>
"""
import io, os, shutil, sys
R, O = sys.argv[1:3]
TEX = "gfx/interface/scripted_gui/countries/TAI"
done = []
for root, _d, files in os.walk(O):
    for f in files:
        src = os.path.join(root, f)
        rel = os.path.relpath(src, O).replace(os.sep, "/")
        dst_rel = f"{TEX}/{f}" if rel.startswith("gfx/") else rel
        dst = os.path.join(R, *dst_rel.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        done.append(dst_rel)

# Special Defense Budget showdown: record which projects each outcome funds
p = os.path.join(R, "events", "Taiwan_Blue_Tiger.txt")
raw = io.open(p, "rb").read()
bom = raw.startswith(b"\xef\xbb\xbf")
t = raw.decode("utf-8-sig")
if "OBT_budget_vote_held" not in t:
    adds = {
        "a": ["set_country_flag = OBT_budget_vote_held", "set_country_flag = OBT_budget_kidd", "set_country_flag = OBT_budget_full", "custom_effect_tooltip = OBT_budget_full_tt"],
        "b": ["set_country_flag = OBT_budget_vote_held", "set_country_flag = OBT_budget_kidd", "custom_effect_tooltip = OBT_budget_trim_tt"],
        "c": ["set_country_flag = OBT_budget_vote_held", "custom_effect_tooltip = OBT_budget_stall_tt"],
    }
    for o, lines in adds.items():
        anchor = f'log = "[GetDateText]: [This.GetName]: blue_tiger.23.{o} executed"\n'
        assert t.count(anchor) == 1, o
        t = t.replace(anchor, anchor + "".join(f"\t\t{l}\n" for l in lines))
    io.open(p, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n").write(t)
    done.append("events/Taiwan_Blue_Tiger.txt (blue_tiger.23 funding flags)")
print("\n".join(done))
