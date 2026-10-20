#!/usr/bin/env python3
"""Write the navigation support files (scripted effect and monthly on_action).

Usage: python3 -B build_nav.py <out_dir>
"""
import os
import sys

OUT = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav_spec  # noqa: E402

# Saves made before a choice group was enabled: set the missing flag and re-check.
MIGRATE = ""
for _name, _enabled, _members in nav_spec.CHOICE_GROUPS:
    if not _enabled:
        continue
    for _fid in _members:
        _flag = nav_spec.choice_flag(_fid)
        MIGRATE += (f"\tif = {{\n\t\tlimit = {{\n\t\t\thas_completed_focus = {_fid}\n"
                    f"\t\t\tNOT = {{ has_country_flag = {_flag} }}\n\t\t}}\n"
                    f"\t\tset_country_flag = {_flag}\n\t\tupdate_focus_tree_obsolete_branches = yes\n\t}}\n")
FILES = {
    "common/scripted_effects/99_OBT_navigation_scripted_effects.txt": """# Operation Blue Tiger: focus tree navigation
# Re-checks which focus tree branches are shown (allow_branch) whenever the ruling party changes,
# using Millennium Dawn's update_focus_tree_obsolete_branches (respects the Obsolete focus branches rule).
TAI_refresh_branch_visibility = {
@@MIGRATE@@\t# Games where Form the Cabinet was completed before this was added
\tif = {
\t\tlimit = {
\t\t\thas_completed_focus = TAI_su_form_cabinet
\t\t\tNOT = { has_country_flag = TAI_first_cabinet_formed }
\t\t}
\t\tset_country_flag = TAI_first_cabinet_formed
\t\tupdate_focus_tree_obsolete_branches = yes
\t}
\tif = {
\t\tlimit = {
\t\t\tNOT = { check_variable = { TAI_visible_ruling_party = ruling_party } }
\t\t}
\t\tset_variable = { TAI_visible_ruling_party = ruling_party }
\t\tupdate_focus_tree_obsolete_branches = yes
\t}
}
""",
    "common/on_actions/99_OBT_navigation_on_actions.txt": """# Operation Blue Tiger: focus tree navigation
on_actions = {
\ton_monthly_TAI = {
\t\teffect = {
\t\t\tTAI_refresh_branch_visibility = yes
\t\t}
\t}
}
""",
}
for rel, text in FILES.items():
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.replace("@@MIGRATE@@", MIGRATE))
print(f"navigation files: {len(FILES)}")
