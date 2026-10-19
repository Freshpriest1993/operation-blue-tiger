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
    for c in DEMOCRATIC_CAPSTONES:
        add(c, DEMOCRATIC_FLAG)
    add(PNG_ROOT)
