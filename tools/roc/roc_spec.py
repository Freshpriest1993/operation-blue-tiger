# Operation Blue Tiger: integration of AUG's RoC-development focus tree into the unified Taiwan tree.
#
# Source: upstream/RoC-development, commit ceb1a0c1f5 ("Taiwan Focus import", cc578de16f7, August 2025, author AUG).
# The original files are preserved byte-exact in archive/roc_dev/ on the integration branch.
#
# Every one of AUG's 92 focus IDs is listed in MAPPING with its destination. Focuses classed as
# Retain, Rework or Archive/optional keep their original ID inside the unified tree; focuses classed
# as Integrate have their unique rewards folded into the OBT focus that already covers the same
# event or policy (MERGES below), and their ID is retired.
#
# Loaded at the end of spec.py:  import roc_spec; roc_spec.integrate(sys.modules[__name__])
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
AH = "Alternate history. "

# ---------------------------------------------------------------- AUG's localisation
AUG_LOC = {}
with open(os.path.join(HERE, "aug_loc.yml"), encoding="utf-8-sig") as _fh:
    for _line in _fh:
        _m = re.match(r'\s*([A-Za-z0-9_.]+):\d*\s*"(.*)"\s*$', _line)
        if _m:
            AUG_LOC[_m.group(1)] = _m.group(2)

NAME_EDITS = {
    "TAI_labour_reform": "Labour Reform",
    "TAI_one_fixed_day_off_and_one_flexible_rest_day": "One Fixed Day Off and One Flexible Rest Day",
    "TAI_social_walfare": "Social Welfare Reform",
    "TAI_long_term_care": "Long-Term Care of Taiwan",
    "TAI_sustainable_development": "Sustainable Development in the 21st Century",
    "TAI_indigenous_defence_warships": "Self-Made Warship Project",
    "TAI_expansion_naval_producing_ability": "Expand Shipbuilding Capabilities",
    "TAI_in_peaceful_way": "Road to Peace",
    "TAI_road_to_war": "Road to War",
    "TAI_nra_garrisoning_south_east_nations": "ROC Forces Guard Southeast Asia",
    "TAI_war_with_malaysia": "Declaration of War on Malaysia",
    "TAI_toward_communism": "Toward Communism",
    "TAI_destory_democracy": "Destroy Democracy",
    "TAI_back_to_one_china": "Return to One China",
    "TAI_usa_garrisoning_taiwan": "The U.S. Announces It Will Help Defend Taiwan",
    "TAI_ask_to_join_nato": "Request to Join NATO",
}
DESC_EDITS = {
    "TAI_social_walfare": "Social welfare is the basic institutional guarantee that protects and improves people's livelihoods, maintains social equity and raises well-being. It is an essential part of balanced economic and social development.",
    "TAI_force_students_serving": "Project National Glory requires a large number of troops. Calling up university students can close part of the gap, with the age of 24 as the dividing line.",
    "TAI_new_taiwan_republic": "A new constitution has been written for the island alone. Proclaiming the Republic of Taiwan would end the claim to govern China, give up the outlying Fujian islands and ask the world to accept a new state. Beijing has always said this would mean war; Washington has always said it opposes any unilateral change.",
    "TAI_back_to_one_china": "The revolutionary government now asks the people to approve talks on the island's return to China. Under our constitution no settlement can take effect without the assent of the people of Taiwan.",
    "TAI_nra_garrisoning_south_east_nations": "Our armed forces will help protect our Southeast Asian partners, with the right of military access throughout the treaty area.",
}
ALT = {
    # alternate-history focuses get the same prefix OBT uses for the Return to the Mainland path
    "TAI_restart_project_national_glory", "TAI_follow_chiang_teach", "TAI_operation_plan", "TAI_infiltrate_coast",
    "TAI_mobilized_reserve_troops", "TAI_army_first_special_force", "TAI_launch_our_plan", "TAI_internal_society_control",
    "TAI_reorganize_garrison_command", "TAI_force_students_serving", "TAI_political_education", "TAI_early_economy_control_apply",
    "TAI_total_economy_control_apply", "TAI_government_control_labor_union", "TAI_enforced_labor_work",
    "TAI_toward_communism", "TAI_obscurantism", "TAI_communist_infiltrate_government", "TAI_destory_democracy", "TAI_back_to_one_china",
    "TAI_second_repbulic_constitution", "TAI_new_taiwan_republic", "TAI_usa_garrisoning_taiwan", "TAI_ask_to_join_nato",
    "TAI_south_east_nations_sign_regional_security_treaty", "TAI_nra_garrisoning_south_east_nations",
    "TAI_road_to_war", "TAI_war_with_philippine", "TAI_ask_philippine_to_surrender", "TAI_war_with_malaysia",
    "TAI_ask_malaysia_to_surrender", "TAI_war_with_vietnam", "TAI_ask_vietnam_to_surrender", "TAI_war_with_thailand",
    "TAI_ask_thailand_to_surrender", "TAI_war_with_indonesia", "TAI_ask_indonesia_to_surrender",
}


def _clean(text):
    for q in ("\u2018", "\u2019", "\u201c", "\u201d"):
        text = text.replace(q, "'")
    return text.replace('"', "'").replace("—", ", ").replace("~", "").strip()


def name(fid):
    return NAME_EDITS.get(fid) or _clean(AUG_LOC[fid])


def desc(fid):
    d = DESC_EDITS.get(fid) or _clean(AUG_LOC.get(fid + "_desc", ""))
    return (AH + d) if fid in ALT else d


# ---------------------------------------------------------------- effect helpers (raw script)
def money(n):
    return f"money:{n}"


def state_build(state, typ, lvl, slots=0):
    lines = [f"{state} = {{"]
    if slots:
        lines.append(f"\tadd_extra_state_shared_building_slots = {slots}")
    lines.append(f"\tadd_building_construction = {{ type = {typ} level = {lvl} instant_build = yes }}")
    lines.append("}")
    return "raw:" + "\n".join(lines)


def random_build(typ, lvl, slots):
    return ("raw:random_owned_controlled_state = {\n"
            f"\tlimit = {{ free_building_slots = {{ building = {typ} size > 0 include_locked = yes }} }}\n"
            f"\tadd_extra_state_shared_building_slots = {slots}\n"
            f"\tadd_building_construction = {{ type = {typ} level = {lvl} instant_build = yes }}\n"
            "}")


def opinion_both(tags, mod):
    out = []
    for t in tags:
        out.append(f"if = {{\n\tlimit = {{ country_exists = {t} }}\n\t{t} = {{ add_opinion_modifier = {{ target = ROOT modifier = {mod} }} }}\n\tadd_opinion_modifier = {{ target = {t} modifier = {mod} }}\n}}")
    return "raw:" + "\n".join(out)


def opinion_in(tags, mod):
    return "raw:" + "\n".join(f"if = {{\n\tlimit = {{ country_exists = {t} }}\n\t{t} = {{ add_opinion_modifier = {{ target = ROOT modifier = {mod} }} }}\n}}" for t in tags)


def if_exists(tag, body):
    inner = "\n".join("\t\t" + l for l in body.split("\n"))
    return f"raw:if = {{\n\tlimit = {{ country_exists = {tag} }}\n\t{tag} = {{\n{inner}\n\t}}\n}}"


def wargoal(tags):
    return "raw:" + "\n".join(f"if = {{\n\tlimit = {{ country_exists = {t} }}\n\tcreate_wargoal = {{ target = {t} type = annex_everything }}\n}}" for t in tags)


def ultimatum(tag, ev):
    return f"raw:if = {{\n\tlimit = {{ country_exists = {tag} }}\n\t{tag} = {{ country_event = {{ id = roc_dev.{ev} days = 1 }} }}\n}}"


def party(i, v):
    return f"party:{i}:{v}"


REMOVE_MAINLAND_CLAIMS = ("raw:every_state = {\n\tlimit = { is_greater_china_state = yes }\n\tremove_core_of = ROOT\n\tremove_claim_by = ROOT\n}\n"
                          "1011 = { remove_claim_by = ROOT }\n"
                          "every_state = {\n\tlimit = { is_taiwan_area_state = yes }\n\tadd_core_of = ROOT\n}")

# AI gating: the alternate-history paths are taken only when the matching AI behaviour option is chosen.
PNG_AI = "add = 10 has_global_flag = TAI_PNG_FOCUS_PATH"
UNITE_AI = "add = 10 has_global_flag = TAI_UNITE_CHANNEL_FOCUS_PATH"
SPLIT_AI = "add = 10 has_global_flag = TAI_ROAD_TO_SPLIT_FOCUS_PATH"
NOT_HISTORICAL = "factor = 0 TAI_ai_historical_path = yes"

# ---------------------------------------------------------------- the 92 focus IDs
# (AUG id, AUG branch, classification, destination, note)
MAPPING = []


def M(fid, grp, cls, dest, note):
    MAPPING.append((fid, grp, cls, dest, note))


ID = "Internal Development"
NM = "National Mobilization"
SP = "Southern Policy"
PNG = "Project National Glory"
MT = "Mainland Threat"
RET, INT, REW, OPT = "Retain unchanged", "Integrate into OBT focus", "Rework (alt-history)", "Archive / optional"

M("TAI_focus_on_internal_development", ID, INT, "TAI_ss_root", "Industry tech bonus (TAI_industry_bonus) added to the Silicon Island root; the root also opens the Economic Policy decision category. The 150 political power is not duplicated.")
M("TAI_develop_rural_district", ID, RET, "Silicon Island, after TAI_ss_trading_economy", "Reward unchanged.")
M("TAI_form_central_taiwan_science_park", ID, INT, "TAI_ss_central_park", "Same project. OBT's two random factories are replaced by AUG's larger grant in Hsinchu and Taichung.")
M("TAI_oil_production_of_gaoxiong", ID, RET, "Silicon Island, after TAI_ss_energy_review", "Keeps the TAI_cpc spirit and the 2001 date gate.")
M("TAI_expand_industrial_in_taipei", ID, RET, "Silicon Island, after TAI_oil_production_of_gaoxiong", "Reward unchanged.")
M("TAI_expand_industrial_for_war", ID, RET, "Operation Blue Tiger, after TAI_bt_adaptation_office", "War-gated, unchanged.")
M("TAI_expand_205th_arsenal", ID, INT, "National Army, follow-on to TAI_na_csist (ID kept)", "Joins the CSIST defense-industry line; reward unchanged.")
M("TAI_cooperate_with_aidc", ID, INT, "TAI_na_idf_upgrade", "fighter_production_bonus added once; air experience raised to AUG's 40.")
M("TAI_indigenous_defence_warships", ID, RET, "National Army, after TAI_expand_205th_arsenal", "Keeps the TAI_idw spirit.")
M("TAI_expansion_naval_producing_ability", ID, RET, "National Army, after TAI_indigenous_defence_warships", "Reward unchanged.")
M("TAI_maanshan_nuclear_power_military_expansion", ID, REW, "Silicon Island, after TAI_ss_energy_review", "Mutually exclusive with TAI_su_gpt_nuclear_free.")
M("TAI_rebuilt_ruined_district_of_921_earthquake", ID, RET, "Island Society branch root", "Removes the TAI_921_earthquake starting spirit, as written.")
M("TAI_taiwan_high_speed_rail_construction_I", ID, INT, "TAI_ss_challenge_2008", "Phase I (2002 start of construction) is covered by Challenge 2008; its 150 political power is not duplicated.")
M("TAI_taiwan_high_speed_rail_construction_II", ID, INT, "TAI_ss_high_speed_rail", "TAI_highspeed_train spirit added to Finish the High-Speed Rail.")
M("TAI_taiwan_high_speed_rail_construction_III", ID, INT, "TAI_ss_ten_projects", "Phase III is covered by the Ten New Major Construction Projects; its 150 political power is not duplicated.")
M("TAI_taiwan_high_speed_rail_construction_IV", ID, INT, "TAI_ss_high_speed_rail", "Infrastructure in the six western-corridor states replaces OBT's two random upgrades; cost reduced from 50 to 15 billion (see balance notes).")
M("TAI_labour_reform", ID, RET, "Island Society, labour line", "Reward unchanged.")
M("TAI_one_fixed_day_off_and_one_flexible_rest_day", ID, RET, "Island Society, labour line", "Date gate 2016.12.1 added (law passed December 2016).")
M("TAI_pension_reform", ID, RET, "Island Society, labour line", "Date gate 2017.6.1 added (passed June 2017).")
M("TAI_act_748", ID, RET, "Island Society, labour line", "Date gate 2019.5.17 added; fires roc_dev.22 (was taiwan.22).")
M("TAI_energy_and_resource_reform", ID, INT, "TAI_ss_renewables", "TAI_renewable_energy spirit added to the Renewable Energy Act.")
M("TAI_social_walfare", ID, RET, "Island Society, welfare line root", "ID kept for compatibility; display name corrected to Social Welfare Reform.")
M("TAI_long_term_care", ID, RET, "Island Society, welfare line", "Date gate 2007.1.1 added (ten-year long-term care plan).")
M("TAI_sustainable_development", ID, INT, "Island Society, welfare line (ID kept)", "Can follow either Long-Term Care or the Green Party's Ecological Tax Reform.")
M("TAI_affordable_housing", ID, RET, "Island Society, welfare line", "Date gate 2016.5.20 added (social housing programme).")
M("TAI_welfare_state", ID, RET, "Island Society capstone", "Reward unchanged.")
M("TAI_legislate_national_mobilization_law", NM, INT, "TAI_na_manpower_question", "TAI_national_mob_law spirit added (All-out Defense Mobilization Act, 2001).")
M("TAI_make_army_ready", NM, INT, "TAI_na_reserve_audit", "Army experience raised to AUG's 60.")
M("TAI_army_reserve_command", NM, INT, "TAI_na_reserve_reform", "TAI_afrc spirit added (Reserve Command, 2002).")
M("TAI_expand_reserve_force_members", NM, INT, "TAI_na_territorial_defense", "TAI_expand_soldiers spirit added; the flat 50,000 manpower grant is removed to avoid doubling reserves.")
M("TAI_prepare_for_enemy_invasions", NM, INT, "TAI_na_reserve_reform", "Becomes +15 Reserve Readiness in the OBT reserve system instead of 200 political power.")
M("TAI_first_level_mobilization", NM, INT, "OBT_partial_mobilization_dec", "Same mechanic; the OBT reserve system is the single mobilization system.")
M("TAI_northern_district_second_level_mobilization", NM, INT, "Decision TAI_reserve_army_northern_district_second_level_mobilization", "Regional theater option during OBT General Mobilization.")
M("TAI_central_district_second_level_mobilization", NM, INT, "Decision TAI_reserve_army_central_district_second_level_mobilization", "Regional theater option during OBT General Mobilization.")
M("TAI_southern_district_second_level_mobilization", NM, INT, "Decision TAI_reserve_army_southern_district_second_level_mobilization", "Regional theater option during OBT General Mobilization.")
M("TAI_total_mobilization", NM, INT, "Decision TAI_total_mobilization_decision", "Outlying-island militia once all three theaters are mobilized in a war with China.")
M("TAI_southern_policy", SP, REW, "Southern Policy branch root, after TAI_as_go_south", "Reward unchanged.")
M("TAI_in_peaceful_way", SP, RET, "Southern Policy, peaceful path", "Exclusive with Road to War, as written.")
M("TAI_establish_economic_relationships", SP, INT, "TAI_as_go_south", "Mutual trade-agreement opinion with Vietnam, Indonesia, Malaysia, the Philippines and Thailand added to Go South.")
M("TAI_establish_unoffical_diplomatic_relationships", SP, RET, "Southern Policy, peaceful path", "Follows Road to Peace (its former prerequisite merged into Go South).")
M("TAI_south_east_nations_sign_regional_security_treaty", SP, REW, "Southern Policy, peaceful capstone", "Requires stability 60% and U.S. support for Taiwan above 59.")
M("TAI_nra_garrisoning_south_east_nations", SP, REW, "Southern Policy, peaceful capstone", "Military access only; display name no longer uses National Revolutionary Army.")
M("TAI_road_to_war", SP, OPT, "Southern Policy, hidden unless the Southern Expansion game rule is on", "Kept as written behind an off-by-default rule.")
M("TAI_war_with_philippine", SP, OPT, "Southern Expansion rule", "annex_everything wargoal, as written.")
M("TAI_ask_philippine_to_surrender", SP, OPT, "Southern Expansion rule", "Fires roc_dev.24 (was taiwan.24).")
M("TAI_war_with_malaysia", SP, OPT, "Southern Expansion rule", "Wargoals on Malaysia, Singapore and Brunei.")
M("TAI_ask_malaysia_to_surrender", SP, OPT, "Southern Expansion rule", "Fires roc_dev.25.")
M("TAI_war_with_vietnam", SP, OPT, "Southern Expansion rule", "Wargoals on Vietnam, Cambodia and Laos.")
M("TAI_ask_vietnam_to_surrender", SP, OPT, "Southern Expansion rule", "Fires roc_dev.26.")
M("TAI_war_with_thailand", SP, OPT, "Southern Expansion rule", "Wargoal on Thailand.")
M("TAI_ask_thailand_to_surrender", SP, OPT, "Southern Expansion rule", "Fires roc_dev.27.")
M("TAI_war_with_indonesia", SP, OPT, "Southern Expansion rule", "Wargoal on Indonesia.")
M("TAI_ask_indonesia_to_surrender", SP, OPT, "Southern Expansion rule", "Fires roc_dev.28.")
M("TAI_restart_project_national_glory", PNG, REW, "Project National Glory branch root", "Requires the Return to the Mainland rule; exclusive with the democratic capstones.")
M("TAI_follow_chiang_teach", PNG, REW, "Project National Glory", "Also lowers U.S. confidence and U.S. support and raises Cross-Strait Tension.")
M("TAI_operation_plan", PNG, REW, "Project National Glory", "Reward unchanged.")
M("TAI_infiltrate_coast", PNG, REW, "Project National Glory", "Reward unchanged.")
M("TAI_mobilized_reserve_troops", PNG, REW, "Project National Glory", "complete_national_focus on two retired mobilization focuses replaced by their OBT rewards; also allows OBT mobilization without a crisis.")
M("TAI_army_first_special_force", PNG, REW, "Project National Glory", "Reward unchanged.")
M("TAI_launch_our_plan", PNG, REW, "Project National Glory", "Opens the Project National Glory decision; the empty uprising check now fires roc_dev.18.")
M("TAI_return_of_nationalist_china", PNG, INT, "OBT Return to the Mainland: reclamation.20 (The Republic Restored)", "Fires roc_dev.19 (was taiwan.19): permanent Security Council seat, political power and stability.")
M("TAI_internal_society_control", PNG, REW, "Project National Glory, internal control line", "Reward unchanged.")
M("TAI_reorganize_garrison_command", PNG, REW, "Project National Glory, internal control line", "Spirit ID TAI_gastapo kept; displayed as Taiwan Garrison Command.")
M("TAI_force_students_serving", PNG, REW, "Project National Glory, internal control line", "Placeholder manpower 114514 set to 50000 (flagged for review).")
M("TAI_political_education", PNG, REW, "Project National Glory, internal control line", "Reward unchanged.")
M("TAI_early_economy_control_apply", PNG, REW, "Project National Glory, economic control line", "Reward unchanged.")
M("TAI_total_economy_control_apply", PNG, REW, "Project National Glory, economic control line", "Reward unchanged.")
M("TAI_government_control_labor_union", PNG, REW, "Project National Glory, economic control line", "Reward unchanged.")
M("TAI_enforced_labor_work", PNG, REW, "Project National Glory, economic control line", "AI weight 0 unless the Project National Glory AI option is chosen.")
M("TAI_threat_from_mainland", MT, INT, "TAI_as_root", "The mainland threat is the premise of Across the Strait; 50 political power not duplicated.")
M("TAI_1992_consensus", MT, INT, "TAI_as_uphold_1992", "tai_92 opinion modifier added in both directions.")
M("TAI_toward_communism", MT, REW, "Across the Strait: Red Infiltration path, after TAI_as_uphold_1992", "Keeps TAI_red_rising.")
M("TAI_obscurantism", MT, REW, "Across the Strait: Red Infiltration path", "Party effect unchanged.")
M("TAI_communist_infiltrate_government", MT, REW, "Across the Strait: Red Infiltration path", "Party effect unchanged.")
M("TAI_destory_democracy", MT, REW, "Across the Strait: Red Infiltration path", "ID kept; display name corrected. Civil-war capitals corrected to states the rebels hold.")
M("TAI_back_to_one_china", MT, REW, "Across the Strait: Red Infiltration path", "Fires roc_dev.20, which opens OBT's staged talks and referendum instead of an instant annexation.")
M("TAI_resist_to_mainland_invasions", MT, INT, "TAI_bt_root", "Same theme; its -50 political power is dropped.")
M("TAI_status_quo", MT, INT, "TAI_as_status_quo_dividend", "Conservatism (KMT) popularity +3; the original raised index 5 (anarchist communism) by 20 despite its conservatism tooltip.")
M("TAI_strengthen_national_unity", MT, INT, "TAI_bt_nsc", "Stability and war support +5% each (AUG +10%, scaled; see balance notes).")
M("TAI_steady_democratic_society", MT, INT, "TAI_df_political_dna", "TAI_post_kmt spirit added beside OBT's consolidated-democracy spirit.")
M("TAI_protect_from_mainland_influences", MT, INT, "TAI_df_influence_transparency", "TAI_aia spirit added when completed after 2019.")
M("TAI_second_repbulic_constitution", MT, REW, "Kuomintang branch, alternative to TAI_su_kmt_roc_on_taiwan", "Removes mainland cores and claims; the missing china.59 is replaced by Cross-Strait Tension.")
M("TAI_toward_fully_independence", MT, INT, "TAI_su_dpp_taiwan_centered", "TAI_taiwan_indep spirit and tai_resist opinion added.")
M("TAI_combine_local_political_powers", MT, INT, "TAI_su_tsu_coalition", "Liberalism (DPP) popularity +5 (AUG +20, scaled).")
M("TAI_defeat_kmt_in_elections", MT, INT, "TAI_su_dpp_new_generation", "TAI_purge_kmt spirit added (weekly stability penalty corrected from -0.5% to -0.1%).")
M("TAI_legislate_new_constitution_of_taiwan_republic", MT, INT, "TAI_su_tsu_new_constitution", "Liberalism popularity +5. The original civil-war trigger used state IDs from an older map and is held for AUG to confirm.")
M("TAI_new_taiwan_republic", MT, REW, "DPP branch alt-history capstone (after DPP or TSU capstone)", "The removed declare_independence_taiwan decision is replaced by Washington Warns (blue_tiger.27) and Cross-Strait Tension.")
M("TAI_strengthen_relationships_with_usa", MT, INT, "TAI_pl_washington", "Declaration-of-friendship opinion added in both directions.")
M("TAI_usa_institute_taiwan", MT, INT, "TAI_pl_capitol_hill", "tai_ait opinion added and roc_dev.23 (was taiwan.23) fired.")
M("TAI_seventh_fleet_pass_thought_strait", MT, INT, "Decision TAI_seventh_fleet_pass_thought_strait (Cross-Strait category)", "Fires roc_dev.21; raises Cross-Strait Tension and U.S. support.")
M("TAI_usa_garrisoning_taiwan", MT, REW, "Pacific Lifeline alt-history capstone", "Requires U.S. support above 79 and the Seventh Fleet invitation; mutual access only.")
M("TAI_ask_to_join_nato", MT, OPT, "Pacific Lifeline, hidden unless the NATO Request game rule is on", "Kept as written behind an off-by-default rule.")

assert len(MAPPING) == 92, len(MAPPING)
assert len({m[0] for m in MAPPING}) == 92


def integrate(S):
    F, branch, BR = S.F, S.branch, S.BRANCHES
    A = {f["id"]: f for b in BR for f in b["focuses"]}

    def B(key):
        return next(b for b in BR if b["key"] == key)

    def add(b, fid, icon, cost, pre=(), excl=(), avail=(), eff=(), ai=1, aimods=(), allow=(), filt=None):
        F(b, fid, name(fid), icon, cost * 7, desc(fid), pre=pre, excl=excl, avail=avail, eff=eff, ai=ai, filt=filt)
        f = b["focuses"][-1]
        if aimods:
            f["aimods"] = list(aimods)
        if allow:
            f["allow"] = list(allow)
        A[fid] = f
        return f

    def merge(fid, *toks, replace=None):
        eff = A[fid]["eff"]
        if replace:
            for old, new in replace:
                i = eff.index(old)
                if new is None:
                    eff.pop(i)
                else:
                    eff[i] = new
        eff.extend(toks)

    # ------------------------------------------------ Silicon Island
    ss, na, bt, as_, pl = B("ss"), B("na"), B("bt"), B("as"), B("pl")
    ECO, IND, NAVY = ["FOCUS_FILTER_ECONOMY"], ["FOCUS_FILTER_INDUSTRY"], ["FOCUS_FILTER_NAVY"]
    add(ss, "TAI_develop_rural_district", "industry_civilian", 10, pre=["TAI_ss_trading_economy"],
        eff=[money(-5)] + [random_build("industrial_complex", 2, 2)] * 4, ai=3, filt=IND)
    add(ss, "TAI_oil_production_of_gaoxiong", "oil_production", 10, pre=["TAI_ss_energy_review"], avail=["date>2001.6.1"],
        eff=["idea:TAI_cpc", money(-5), state_build(599, "synthetic_refinery", 2, 2)], ai=3, filt=IND)
    add(ss, "TAI_expand_industrial_in_taipei", "industry_democratic", 8, pre=["TAI_oil_production_of_gaoxiong"],
        eff=[money(-3), state_build(598, "industrial_complex", 2, 2)], ai=3, filt=IND)
    add(ss, "TAI_maanshan_nuclear_power_military_expansion", "nuclear_energy", 5, pre=["TAI_ss_energy_review"],
        excl=["TAI_su_gpt_nuclear_free"], eff=[money(-10), state_build(599, "nuclear_reactor", 1, 1)], ai=1, filt=IND)

    # ------------------------------------------------ National Army: defense-industry line
    add(na, "TAI_expand_205th_arsenal", "industry_military", 10, pre=["TAI_na_csist"],
        eff=[money(-3), "raw:598 = { add_extra_state_shared_building_slots = 2 }", "raw:add_offsite_building = { type = arms_factory level = 2 }"], ai=3,
        filt=["FOCUS_FILTER_INDUSTRY"])
    add(na, "TAI_indigenous_defence_warships", "navy2", 10, pre=["TAI_expand_205th_arsenal"],
        eff=[money(-5), "idea:TAI_idw"], ai=3, filt=NAVY)
    add(na, "TAI_expansion_naval_producing_ability", "navy", 10, pre=["TAI_indigenous_defence_warships"],
        eff=[money(-15)] + [random_build("dockyard", 1, 1)] * 3, ai=2, filt=NAVY)

    # ------------------------------------------------ Operation Blue Tiger: wartime economy
    add(bt, "TAI_expand_industrial_for_war", "industry_democratic3", 10, pre=["TAI_bt_adaptation_office"], avail=["raw:has_war = yes"],
        eff=[money(-10), "raw:add_offsite_building = { type = industrial_complex level = 3 }", "raw:add_offsite_building = { type = arms_factory level = 2 }"],
        ai=5, filt=IND)

    # ------------------------------------------------ Across the Strait: Red Infiltration (alt-history)
    red = dict(ai=0, aimods=[UNITE_AI])
    add(as_, "TAI_toward_communism", "communism4", 15, pre=["TAI_as_uphold_1992"], eff=["idea:TAI_red_rising"], **red)
    add(as_, "TAI_obscurantism", "communist_propaganda", 10, pre=["TAI_toward_communism"],
        eff=["raw:custom_effect_tooltip = TAI_communism_increase_10_tt", party(5, 0.1)], **red)
    add(as_, "TAI_communist_infiltrate_government", "communism12", 10, pre=["TAI_obscurantism"],
        eff=["raw:custom_effect_tooltip = TAI_communism_increase_40_tt", party(5, 0.4)], **red)
    add(as_, "TAI_destory_democracy", "communism8", 2, pre=["TAI_communist_infiltrate_government"], eff=[
        "raw:custom_effect_tooltip = TAI_communist_upring_tt\nhidden_effect = {\n"
        "\tset_politics = { ruling_party = communism elections_allowed = no }\n"
        "\tif = { limit = { communism < 0.3 communism > 0.1 } start_civil_war = { ruling_party = communism ideology = democratic size = 0.8 capital = 598 states = { 598 599 600 430 1109 } } }\n"
        "\tif = { limit = { communism < 0.5 communism > 0.3 } start_civil_war = { ruling_party = communism ideology = democratic size = 0.6 capital = 598 states = { 598 599 600 1015 } } }\n"
        "\tif = { limit = { communism < 0.7 communism > 0.5 } start_civil_war = { ruling_party = communism ideology = democratic size = 0.4 capital = 430 states = { 430 1015 1109 } } }\n"
        "\tif = { limit = { communism < 0.9 communism > 0.7 } start_civil_war = { ruling_party = communism ideology = democratic size = 0.2 capital = 598 states = { 598 599 } } }\n"
        "\tif = { limit = { communism > 0.9 } start_civil_war = { ruling_party = communism ideology = democratic size = 0.1 capital = 1158 states = { 1158 } } }\n"
        "}"], **red)
    add(as_, "TAI_back_to_one_china", "peoples_republic_of_china", 1, pre=["TAI_destory_democracy"],
        eff=["raw:custom_effect_tooltip = TAI_back_to_chi_tt", "raw:country_event = { id = roc_dev.20 days = 1 }", "pp:100"], **red)

    # ------------------------------------------------ Kuomintang: Second Republic (alt-history)
    km, dpp = B("kmt"), B("dpp")
    add(km, "TAI_second_repbulic_constitution", "legislative_yuan", 8, pre=["TAI_su_kmt_consent"], excl=["TAI_su_kmt_roc_on_taiwan"],
        avail=["kmt", "raw:has_war = no"], ai=0, aimods=[SPLIT_AI],
        eff=["pp:50", "raw:custom_effect_tooltip = TAI_second_constitution_tt", REMOVE_MAINLAND_CLAIMS, "chi:tension:10", "var:identity:5"])

    # ------------------------------------------------ DPP: Republic of Taiwan (alt-history)
    add(dpp, "TAI_new_taiwan_republic", "ind_taiwan", 5, pre=[("TAI_su_dpp_own_path", "TAI_su_tsu_taiwan_consensus")],
        avail=["dpp", "raw:has_war = no", "raw:custom_trigger_tooltip = { tooltip = ROC_identity_above_69_tt check_variable = { TAI_taiwanese_identity > 69 } }"],
        ai=0, aimods=[SPLIT_AI],
        eff=["raw:custom_effect_tooltip = TAI_taiwan_republic_tt", "raw:set_cosmetic_tag = TAI_TAIWAN_democratic", REMOVE_MAINLAND_CLAIMS,
             if_exists("CHI", "transfer_state = 430\ntransfer_state = 491\ntransfer_state = 1015\ntransfer_state = 1109"),
             "var:identity:10", "chi:tension:25", "var:usconf:-15", "raw:country_event = { id = blue_tiger.27 days = 3 }"])

    # ------------------------------------------------ Pacific Lifeline: U.S. commitment and NATO
    add(pl, "TAI_usa_garrisoning_taiwan", "american_shield", 10, pre=["TAI_pl_us_crisis_comms"],
        avail=["raw:has_country_flag = ROC_seventh_fleet_invited",
               "raw:custom_trigger_tooltip = { tooltip = ROC_us_support_above_79_tt CHI = { check_variable = { CHI_taiwan_us_support > 79 } } }"],
        ai=1, aimods=[NOT_HISTORICAL],
        eff=[if_exists("USA", "give_military_access = ROOT\nROOT = { give_military_access = PREV }"), "chi:tension:10", "var:usconf:10"])
    add(pl, "TAI_ask_to_join_nato", "align_to_nato", 5, pre=["TAI_usa_garrisoning_taiwan"],
        allow=["raw:NOT = { has_game_rule = { rule = TAI_nato_request option = DISABLED } }"],
        avail=["raw:ROC_nato_request_allowed = yes", "raw:threat > 0.5", "raw:has_stability > 0.7", "raw:has_war_support > 0.7", "raw:has_elections = yes",
               "raw:num_of_military_factories > 12", "raw:num_divisions > 50", "raw:has_war = no"],
        ai=0, aimods=["add = 5 ROC_nato_request_allowed = yes " + "NOT = { TAI_ai_historical_path = yes }"],
        eff=["pp:120", "raw:custom_effect_tooltip = TAI_war_with_mainland_tt", "raw:NATO_join_via_event = yes"])

    # ------------------------------------------------ new branch: Island Society
    isl = branch("isl", "Island Society", 0, ["FOCUS_FILTER_INTERNAL_AFFAIRS"])
    WEL = ["FOCUS_FILTER_INTERNAL_AFFAIRS"]
    infra6 = "raw:" + "\n".join(f"{s} = {{ add_building_construction = {{ type = infrastructure level = 1 instant_build = yes }} }}" for s in (598, 599, 600, 1155, 1156, 1157))
    add(isl, "TAI_rebuilt_ruined_district_of_921_earthquake", "infrastructure", 7, ai=10, filt=["FOCUS_FILTER_INDUSTRY", "FOCUS_FILTER_INTERNAL_AFFAIRS"],
        aimods=["factor = 0 has_active_mission = bankruptcy_incoming_collapse"], eff=[
        "raw:if = {\n\tlimit = { has_idea = TAI_921_earthquake }\n\tremove_ideas = TAI_921_earthquake\n\tset_temp_variable = { treasury_change = -20 }\n\tmodify_treasury_effect = yes\n}", infra6])
    add(isl, "TAI_labour_reform", "union_negotiations", 5, pre=["TAI_rebuilt_ruined_district_of_921_earthquake"], eff=["pp:150"], ai=3)
    add(isl, "TAI_one_fixed_day_off_and_one_flexible_rest_day", "dangerous_laws", 8, pre=["TAI_labour_reform"], avail=["date>2016.12.1"],
        eff=["idea:TAI_labour_standards_law"], ai=3)
    add(isl, "TAI_pension_reform", "demand_territory", 10, pre=["TAI_one_fixed_day_off_and_one_flexible_rest_day"], avail=["date>2017.6.1"],
        eff=["idea:TAI_military_public_educational_pension_reform"], ai=3)
    add(isl, "TAI_act_748", "national_unity", 10, pre=["TAI_pension_reform"], avail=["date>2019.5.17"],
        eff=["pp:150", "stab:0.05", "raw:country_event = { id = roc_dev.22 days = 1 }"], ai=3)
    add(isl, "TAI_social_walfare", "consumer_goods", 5, pre=["TAI_rebuilt_ruined_district_of_921_earthquake"], eff=["pp:150"], ai=3)
    add(isl, "TAI_long_term_care", "consumer_goods", 10, pre=["TAI_social_walfare"], avail=["date>2007.1.1"],
        eff=["pp:100", "idea:TAI_long_care_2"], ai=3)
    add(isl, "TAI_sustainable_development", "sustainable_development", 10, pre=[("TAI_long_term_care", "TAI_su_gpt_eco_reform")],
        eff=["idea:TAI_sustainable_development_strategy", "stab:0.1"], ai=2)
    add(isl, "TAI_affordable_housing", "construction3", 8, pre=["TAI_sustainable_development"], avail=["date>2016.5.20"],
        eff=["idea:TAI_affordable_housing_plan", "ws:0.1"], ai=3)
    add(isl, "TAI_welfare_state", "consumer_goods", 10, pre=["TAI_affordable_housing"], eff=["pp:150", "idea:TAI_walfare_state_goal"], ai=3)

    # ------------------------------------------------ new branch: Southern Policy
    sp = branch("sp", "Southern Policy", 0, ["FOCUS_FILTER_FOREIGN_POLICY"])
    SEA = ["VIE", "IND", "MAY", "PHI", "SIA"]
    add(sp, "TAI_southern_policy", "race_relations2", 7, pre=["TAI_as_go_south"], eff=["pp:50"], ai=2)
    add(sp, "TAI_in_peaceful_way", "improve_relations", 5, pre=["TAI_southern_policy"], excl=["TAI_road_to_war"], eff=["pp:25"], ai=5)
    add(sp, "TAI_establish_unoffical_diplomatic_relationships", "intelligence_exchange2", 10, pre=["TAI_in_peaceful_way"],
        eff=[opinion_in(SEA, "declaration_of_friendship")], ai=3)
    add(sp, "TAI_south_east_nations_sign_regional_security_treaty", "chinese_glory", 10, pre=["TAI_establish_unoffical_diplomatic_relationships"],
        avail=["raw:has_stability > 0.6", "raw:custom_trigger_tooltip = { tooltip = ROC_us_support_above_59_tt CHI = { check_variable = { CHI_taiwan_us_support > 59 } } }"],
        ai=1, aimods=[NOT_HISTORICAL],
        eff=["raw:" + "\n".join(f"if = {{\n\tlimit = {{ country_exists = {t} }}\n\tgive_guarantee = {t}\n\t{t} = {{ give_guarantee = ROOT }}\n}}" for t in SEA)])
    add(sp, "TAI_nra_garrisoning_south_east_nations", "entente", 3, pre=["TAI_south_east_nations_sign_regional_security_treaty"],
        ai=1, aimods=[NOT_HISTORICAL],
        eff=["raw:" + "\n".join(f"if = {{\n\tlimit = {{ country_exists = {t} }}\n\t{t} = {{ give_military_access = ROOT }}\n}}" for t in SEA)])
    SEXP = ["raw:NOT = { has_game_rule = { rule = TAI_southern_expansion option = DISABLED } }"]
    war_ai = dict(ai=0, aimods=["add = 10 ROC_southern_expansion_allowed = yes has_global_flag = TAI_PNG_FOCUS_PATH"])
    add(sp, "TAI_road_to_war", "ultimatum2", 5, pre=["TAI_southern_policy"], excl=["TAI_in_peaceful_way"], allow=SEXP,
        avail=["raw:ROC_southern_expansion_allowed = yes"], eff=[opinion_in(SEA, "declaration_of_hostility")], **war_ai)
    chain = [("philippine", ["PHI"], 24), ("malaysia", ["MAY", "SIN", "BRU"], 25), ("vietnam", ["VIE", "CBD", "LAO"], 26),
             ("thailand", ["SIA"], 27), ("indonesia", ["IND"], 28)]
    prev = ("TAI_road_to_war",)
    for key, tags, ev in chain:
        icon = "attack_" + ("philippines" if key == "philippine" else key)
        w, a = f"TAI_war_with_{key}", f"TAI_ask_{key}_to_surrender"
        add(sp, w, icon, 5, pre=[prev], excl=[a], avail=["raw:ROC_southern_expansion_allowed = yes"], eff=[wargoal(tags)], ai=10)["war_with"] = tags
        add(sp, a, icon, 5, pre=[prev], avail=["raw:ROC_southern_expansion_allowed = yes"], eff=["raw:custom_effect_tooltip = TT_IF_THEY_ACCEPT", ultimatum(tags[0], ev)], ai=10)
        prev = (w, a)

    # ------------------------------------------------ new branch: Project National Glory (alt-history)
    png = branch("png", "Project National Glory", 0, ["FOCUS_FILTER_POLITICAL"])
    DEMO_CAPS = ["TAI_su_kmt_roc_on_taiwan", "TAI_su_pfp_third_force", "TAI_su_dpp_own_path", "TAI_su_tsu_taiwan_consensus", "TAI_su_gpt_conscience", "TAI_df_political_dna"]
    if "TAI_su_dpp_pragmatic_sovereignty" in A:  # OBT's Status Quo capstone (identity/identity_spec.py)
        DEMO_CAPS.append("TAI_su_dpp_pragmatic_sovereignty")
    g = dict(ai=10)
    # Exclusive with the democratic capstones. Written as completed-focus checks on both sides instead of
    # mutually_exclusive, so the tree does not draw six exclusion lines across it; only one focus can be in
    # progress at a time, so the same combinations are blocked for players and the AI.
    add(png, "TAI_restart_project_national_glory", "whampoa_military_academy", 3,
        avail=[f"raw:NOT = {{ has_completed_focus = {c} }}" for c in DEMO_CAPS] + ["raw:TAI_reclamation_allowed = yes", "raw:country_exists = CHI", "raw:CHI = { has_government = communism }", "raw:has_government = democratic", "raw:has_war = no"],
        ai=0, aimods=[PNG_AI], eff=["idea:TAI_old_kmt_rise_up", "pp:150", "stab:-0.1", "ws:0.05"])
    add(png, "TAI_follow_chiang_teach", "chiang_kai_shek", 7, pre=["TAI_restart_project_national_glory"],
        avail=["raw:democratic > 0.42", "raw:has_government = democratic", "raw:has_war = no"], eff=[
            "rmidea:TAI_post_kmt",
            "raw:if = {\n\tlimit = { is_guaranteed_by = USA }\n\tUSA = { diplomatic_relation = { country = ROOT relation = guarantee active = no } }\n}",
            "raw:set_politics = { ruling_party = nationalist elections_allowed = no }\nstart_politics_input = yes\nadd_to_array = { ruling_party = 21 }\nadd_to_variable = { var = party_pop_array^21 value = 0.8 }\nstartup_politics = yes",
            "raw:kill_country_leader = yes\ncreate_country_leader = { name = \"John Chiang\" picture = \"John_Chiang.dds\" ideology = Nat_Fascism }",
            "idea:TAI_martial_law", "flag:TAI_citizen_resist",
            "raw:set_party_name = { ideology = democratic long_name = TAI_liberalism_party_tdra_long name = TAI_liberalism_party_tdra }",
            "var:usconf:-20", "chi:ussupport:-15", "chi:tension:10"], **g)
    add(png, "TAI_operation_plan", "army_logistics", 5, pre=["TAI_follow_chiang_teach"], eff=["pp:125"], **g)
    add(png, "TAI_infiltrate_coast", "war2_green", 10, pre=["TAI_operation_plan"], eff=["idea:encryption_bonus"], **g)
    add(png, "TAI_mobilized_reserve_troops", "army_reform", 10, pre=["TAI_infiltrate_coast"], eff=[
        "raw:if = { limit = { NOT = { has_idea = TAI_afrc } } add_ideas = TAI_afrc }",
        "raw:custom_effect_tooltip = ROC_reserve_readiness_20_tt\nhidden_effect = {\n\tOBT_reserve_init = yes\n\tadd_to_variable = { OBT_reserve_readiness = 20 }\n\tclamp_variable = { var = OBT_reserve_readiness min = 0 max = 100 }\n}",
        "raw:custom_effect_tooltip = ROC_png_mobilization_tt"], **g)
    add(png, "TAI_army_first_special_force", "special_forces", 10, pre=["TAI_mobilized_reserve_troops"],
        eff=["idea:TAI_1st_special_force", "flag:TAI_army_resist", "flag:TAI_army_1sf"], **g)
    add(png, "TAI_internal_society_control", "fascism", 10, pre=["TAI_follow_chiang_teach"], eff=["pp:150", "ws:0.05"], **g)
    add(png, "TAI_reorganize_garrison_command", "taiwan_garrison_command", 10, pre=["TAI_internal_society_control"],
        eff=["idea:TAI_gastapo", "flag:TAI_public_fear"], **g)
    add(png, "TAI_force_students_serving", "entente", 5, pre=["TAI_reorganize_garrison_command"],
        eff=["raw:add_manpower = 50000", "stab:-0.05", "flag:TAI_student_resist"], **g)
    add(png, "TAI_political_education", "propaganda", 10, pre=["TAI_force_students_serving"], eff=["idea:TAI_political_edu", "stab:0.1"], **g)
    add(png, "TAI_early_economy_control_apply", "consumer_goods", 5, pre=["TAI_follow_chiang_teach"],
        eff=["idea:TAI_early_economy_control", "flag:TAI_public_resist"], **g)
    add(png, "TAI_total_economy_control_apply", "consumer_goods", 10, pre=["TAI_early_economy_control_apply"],
        eff=["rmidea:TAI_early_economy_control", "idea:TAI_total_economy_control"], **g)
    add(png, "TAI_government_control_labor_union", "local_management", 10, pre=["TAI_total_economy_control_apply"],
        eff=["idea:TAI_government_controlled_union", "flag:TAI_labor_resist"], **g)
    add(png, "TAI_enforced_labor_work", "production2", 10, pre=["TAI_government_control_labor_union"], eff=["idea:TAI_enforced_labor"],
        ai=0, aimods=[PNG_AI])
    add(png, "TAI_launch_our_plan", "attack_china", 5, pre=["TAI_army_first_special_force", "TAI_political_education", "TAI_enforced_labor_work"],
        avail=["raw:has_war = no"], eff=[
            "raw:unlock_decision_category_tooltip = TAI_png_decisions_category",
            "raw:custom_effect_tooltip = TAI_png_tt",
            "raw:if = {\n\tlimit = {\n\t\thas_country_flag = TAI_army_resist\n\t\tOR = {\n"
            "\t\t\tAND = { has_country_flag = TAI_public_fear has_country_flag = TAI_labor_resist }\n"
            "\t\t\tAND = { has_country_flag = TAI_public_resist has_country_flag = TAI_student_resist }\n"
            "\t\t\tAND = { has_country_flag = TAI_labor_resist has_country_flag = TAI_student_resist }\n"
            "\t\t}\n\t}\n\tcountry_event = { id = roc_dev.18 days = 30 }\n}"], **g)

    # ------------------------------------------------ rewards folded into existing OBT focuses
    merge("TAI_ss_root", "raw:add_tech_bonus = { name = TAI_industry_bonus bonus = 0.65 uses = 3 category = CAT_industry }",
          "raw:unlock_decision_category_tooltip = TAI_economy_decisions_category")
    merge("TAI_ss_central_park", money(-3), state_build(1155, "industrial_complex", 2, 2), state_build(1156, "industrial_complex", 2, 2),
          replace=[("build:one_random_industrial_complex", None), ("build:one_random_industrial_complex", None)])
    merge("TAI_ss_high_speed_rail", "idea:TAI_highspeed_train", money(-15), infra6,
          replace=[("build:one_random_infrastructure", None), ("build:one_random_infrastructure", None)])
    merge("TAI_ss_renewables", "idea:TAI_renewable_energy")
    merge("TAI_na_idf_upgrade", "raw:if = { limit = { NOT = { has_idea = fighter_production_bonus } } add_ideas = fighter_production_bonus }",
          replace=[("air_xp:30", "air_xp:40")])
    merge("TAI_na_manpower_question", "idea:TAI_national_mob_law")
    merge("TAI_na_reserve_audit", replace=[("army_xp:25", "army_xp:60")])
    merge("TAI_na_reserve_reform", "idea:TAI_afrc",
          "raw:custom_effect_tooltip = ROC_reserve_readiness_15_tt\nhidden_effect = {\n\tOBT_reserve_init = yes\n\tadd_to_variable = { OBT_reserve_readiness = 15 }\n\tclamp_variable = { var = OBT_reserve_readiness min = 0 max = 100 }\n}")
    merge("TAI_na_territorial_defense", "idea:TAI_expand_soldiers")
    merge("TAI_as_go_south", opinion_both(SEA, "mutual_trade_agreement"))
    merge("TAI_as_uphold_1992", opinion_both(["CHI"], "tai_92"))
    merge("TAI_as_status_quo_dividend", party(1, 0.03))
    merge("TAI_bt_nsc", "stab:0.05", "ws:0.05")
    merge("TAI_df_political_dna", "raw:if = { limit = { NOT = { has_idea = TAI_post_kmt } } add_ideas = TAI_post_kmt }")
    merge("TAI_df_influence_transparency", "raw:if = {\n\tlimit = { date > 2019.12.31 }\n\tadd_ideas = TAI_aia\n}")
    merge("TAI_su_dpp_taiwan_centered", "idea:TAI_taiwan_indep", opinion_both(["CHI"], "tai_resist"), "chi:tension:3")
    merge("TAI_su_tsu_coalition", party(2, 0.05))
    merge("TAI_su_dpp_new_generation", "idea:TAI_purge_kmt")
    merge("TAI_su_tsu_new_constitution", party(2, 0.05))
    merge("TAI_pl_washington", opinion_both(["USA"], "declaration_of_friendship"))
    merge("TAI_pl_capitol_hill", opinion_both(["USA"], "tai_ait"), "raw:country_event = { id = roc_dev.23 days = 7 }")

    # AI staffing guards for factories built directly (OBT's build: macros add these automatically)
    STAFF = {"industrial_complex": "can_staff_an_industrial_complex", "arms_factory": "can_staff_an_arms_industry", "dockyard": "can_staff_an_dockyard"}
    for fid, kinds in (("TAI_develop_rural_district", ["industrial_complex"]), ("TAI_expand_industrial_in_taipei", ["industrial_complex"]),
                       ("TAI_ss_central_park", ["industrial_complex"]), ("TAI_expand_205th_arsenal", ["arms_factory"]),
                       ("TAI_expansion_naval_producing_ability", ["dockyard"]), ("TAI_expand_industrial_for_war", ["industrial_complex", "arms_factory"])):
        A[fid].setdefault("aimods", []).extend(f"factor = 0 {STAFF[k]} = no" for k in kinds)

    # ------------------------------------------------ checks
    for fid, grp, cls, dest, note in MAPPING:
        in_tree = fid in A
        if cls in (RET, REW, OPT) or fid in ("TAI_expand_205th_arsenal", "TAI_sustainable_development"):
            assert in_tree, f"{fid} should be in the tree"
        else:
            assert not in_tree, f"{fid} was merged and must not be in the tree"
    for c in DEMO_CAPS:
        A[c]["avail"].append("raw:NOT = { has_completed_focus = TAI_restart_project_national_glory }")

    # Layout: Southern Policy and Project National Glory sit under Across the Strait, in the Pacific Lifeline
    # column and beside the Kuomintang; Island Society sits under Democratic Fortress with the domestic branches.
    assert S.TIERS == [["pl", "su", "ss"], ["kmt", "pfp", "dpp", "tsu", "gpt"], ["as", "df", "na", "bt"]], S.TIERS
    S.TIERS = [["pl", "su", "ss"], ["kmt", "pfp", "dpp", "tsu", "gpt"], [["as", ("sp", "png")], "bt", "na", ["df", "isl"]]]
    S.TIER_GAP = 3
    S.CONTINUOUS_POS = (2000, 3800)  # pixels (96 x 130 per cell): the empty area under Operation Blue Tiger
    return S.TIERS


def roc_focus_ids():
    return [m[0] for m in MAPPING]
