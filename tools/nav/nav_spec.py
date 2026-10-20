# Operation Blue Tiger: focus tree navigation (branch hiding).
#
# Uses the same technique as Millennium Dawn's Poland and Greece trees: allow_branch on a branch root
# hides that branch, and update_focus_tree_obsolete_branches (Millennium Dawn's wrapper around
# mark_focus_tree_layout_dirty) makes the game re-check the condition. Hiding follows Millennium
# Dawn's "Obsolete focus branches" game rule: with the rule set to Show, nothing is hidden.
# Nothing is deleted: completed focuses stay completed and keep their rewards, and every focus ID
# is unchanged.
#
# The conditions use country flags set in the same completion reward, before the re-check, rather
# than has_completed_focus on the focus being completed (which may not count as completed yet when
# the re-check runs).
#
# Loaded at the end of spec.py:  import nav_spec; nav_spec.integrate(sys.modules[__name__])
# Set OBT_SKIP_NAV=1 to build the tree without branch hiding.

import os

PARTY_ROOTS = {
    "TAI_su_kmt_rebuild": "TAI_kmt_in_power = yes",
    "TAI_su_pfp_people_first": "TAI_pfp_in_power = yes",
    "TAI_su_dpp_four_noes": "TAI_pan_green_in_power = yes",
    "TAI_su_tsu_founding": "TAI_pan_green_in_power = yes",
    "TAI_su_gpt_root": "TAI_pan_green_in_power = yes",
}
DEMOCRATIC_CAPSTONES = [
    "TAI_su_kmt_roc_on_taiwan", "TAI_su_pfp_third_force", "TAI_su_dpp_own_path",
    "TAI_su_tsu_taiwan_consensus", "TAI_su_gpt_conscience", "TAI_df_political_dna",
]
PNG_ROOT = "TAI_restart_project_national_glory"
SHOW = "has_game_rule = { rule = obsolete_focus_branches_visibility option = SHOW }"
REFRESH = "raw:update_focus_tree_obsolete_branches = yes"
CABINET_FLAG = "TAI_first_cabinet_formed"
DEMOCRATIC_FLAG = "TAI_democratic_capstone_completed"


def integrate(S):
    A = {f["id"]: f for b in S.BRANCHES for f in b["focuses"]}

    # Party branches: all visible until the first cabinet is formed; afterwards only the governing
    # camp's branches, plus any branch the player has already started.
    for root, governs in PARTY_ROOTS.items():
        A[root].setdefault("allow", []).append(
            "raw:OR = {\n"
            f"\t{SHOW}\n"
            f"\tNOT = {{ has_country_flag = {CABINET_FLAG} }}\n"
            f"\thas_completed_focus = {root}\n"
            f"\t{governs}\n"
            "}")

    # Project National Glory: hidden once a democratic capstone is completed or the
    # Return to the Mainland rule is Blocked, unless the player has already started it.
    A[PNG_ROOT].setdefault("allow", []).append(
        "raw:OR = {\n"
        f"\t{SHOW}\n"
        f"\thas_completed_focus = {PNG_ROOT}\n"
        "\tAND = {\n"
        f"\t\tNOT = {{ has_country_flag = {DEMOCRATIC_FLAG} }}\n"
        "\t\tNOT = { has_game_rule = { rule = TAI_return_to_mainland option = BLOCKED } }\n"
        "\t}\n"
        "}")

    # Set the flag first, then re-check visibility.
    def add(fid, flag=None):
        eff = A[fid]["eff"]
        if flag:
            eff.append(f"raw:set_country_flag = {flag}")
        eff.append(REFRESH)

    add("TAI_su_form_cabinet", CABINET_FLAG)
    caps = DEMOCRATIC_CAPSTONES + [c for c in ("TAI_su_dpp_pragmatic_sovereignty",) if c in A]
    for c in caps:
        add(c, DEMOCRATIC_FLAG)
    add(PNG_ROOT)
    integrate_choice_groups(S)


# ---------------------------------------------------------------- progressive hiding: choice groups
# Mutually exclusive choices whose unchosen side is hidden once one side is completed.
# Each member sets its own flag before the re-check; every other member is hidden while any other
# member's flag is set, unless it was itself completed. The Show Obsolete Branches rule disables it.
# Groups are enabled one at a time so each can be tested on its own.
CHOICE_GROUPS = [
    # (name, enabled, members)
    ("judicial_reform", True, ["TAI_df_special_division", "TAI_df_ordinary_prosecutors"]),
    ("nuclear_policy", False, ["TAI_maanshan_nuclear_power_military_expansion", "TAI_su_gpt_nuclear_free"]),
    ("national_identity", False, ["TAI_su_dpp_status_quo", "TAI_su_dpp_name_rectification"]),
    ("constitutional_reform", True, ["TAI_second_repbulic_constitution", "TAI_su_kmt_roc_on_taiwan"]),
]


def choice_flag(fid):
    return "TAI_nav_chose_" + fid[4:] if fid.startswith("TAI_") else "TAI_nav_chose_" + fid


def integrate_choice_groups(S):
    A = {f["id"]: f for b in S.BRANCHES for f in b["focuses"]}
    for name, enabled, members in CHOICE_GROUPS:
        if not enabled or os.environ.get("OBT_SKIP_CHOICE_" + name.upper()) == "1":
            continue
        for fid in members:
            others = [m for m in members if m != fid]
            A[fid].setdefault("allow", []).append(
                "raw:OR = {\n"
                f"\t{SHOW}\n"
                f"\thas_completed_focus = {fid}\n"
                + "".join(f"\tNOT = {{ has_country_flag = {choice_flag(o)} }}\n" for o in others)
                + "}")
            eff = A[fid]["eff"]
            flag = f"raw:set_country_flag = {choice_flag(fid)}"
            if REFRESH in eff:
                eff.insert(eff.index(REFRESH), flag)
            else:
                eff += [flag, REFRESH]
