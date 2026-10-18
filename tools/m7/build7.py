#!/usr/bin/env python3
"""Generate the Operation Blue Tiger Cross-Strait Tension meter (milestone 7) source files.

Usage: python3 build7.py <out_dir>
Writes effects, triggers, dynamic modifiers, decisions, events, GUI, scripted GUI,
scripted localisation and localisation into out_dir for apply7.py / refresh7.sh.
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
STAGES = ["calm", "friction", "coercion", "crisis", "brink"]
NAMES = ["Calm", "Friction", "Coercion", "Crisis", "Brink"]
COL = ["G", "Y", "O", "R", "R"]
LO = [0, 20, 40, 60, 80]

CHI_MOD = {
    "stability_factor": (0.02, 0, -0.01, -0.03, -0.05),
    "political_power_gain": (0.05, 0.01, -0.02, -0.05, -0.10),
    "trade_opinion_factor": (0.05, -0.02, -0.05, -0.10, -0.15),
    "industrial_capacity_factory": (0.02, 0, 0, 0, 0),
    "consumer_goods_factor": (0, 0, 0, 0.02, 0.04),
    "army_org_factor": (0, 0, 0.02, 0.03, 0.05),
    "experience_gain_army_factor": (0, 0, 0.05, 0.10, 0.15),
    "experience_gain_navy_factor": (0, 0, 0.05, 0.10, 0.15),
}
TAI_MOD = {
    "stability_factor": (0.02, 0, 0, -0.02, -0.04),
    "political_power_gain": (0.05, 0, -0.02, -0.04, -0.06),
    "trade_opinion_factor": (0.05, -0.02, -0.03, -0.06, -0.10),
    "industrial_capacity_factory": (0.02, 0, 0, 0, 0),
    "consumer_goods_factor": (0, 0, 0, 0.02, 0.04),
    "war_support_factor": (0, 0.02, 0.03, 0.05, 0.08),
    "army_defence_factor": (0, 0, 0.02, 0.04, 0.05),
    "conscription_factor": (0, 0, 0.02, 0.04, 0.06),
    "static_anti_air_damage_factor": (0, 0, 0.05, 0.10, 0.15),
}
VARNAME = {"stability_factor": "stab", "political_power_gain": "pp", "trade_opinion_factor": "trade",
           "industrial_capacity_factory": "factory", "consumer_goods_factor": "cg", "army_org_factor": "org",
           "experience_gain_army_factor": "armyxp", "experience_gain_navy_factor": "navyxp",
           "war_support_factor": "ws", "army_defence_factor": "def", "conscription_factor": "consc",
           "static_anti_air_damage_factor": "aa"}
LABEL = {"stability_factor": "stability", "political_power_gain": "political power", "trade_opinion_factor": "trade opinion",
         "industrial_capacity_factory": "factory output", "consumer_goods_factor": "consumer goods",
         "army_org_factor": "army organization", "experience_gain_army_factor": "army experience gain",
         "experience_gain_navy_factor": "navy experience gain", "war_support_factor": "war support",
         "army_defence_factor": "army defense", "conscription_factor": "recruitable population",
         "static_anti_air_damage_factor": "anti-air damage"}
BAD_WHEN_UP = {"consumer_goods_factor"}


def w(name, text, bom=False):
    with open(os.path.join(OUT, name), "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(text)


def ind(s, t):
    return "\n".join((t + l) if l else l for l in s.split("\n"))


def fmt_effects(mods, s):
    parts = []
    for k, vals in mods.items():
        v = vals[s]
        if not v:
            continue
        good = (v < 0) if k in BAD_WHEN_UP else (v > 0)
        c = "G" if good else "R"
        parts.append(f"§{c}{v * 100:+.0f}%§! {LABEL[k]}")
    return ", ".join(parts) if parts else "no effect"


# ---------------------------------------------------------------- dynamic modifiers
dm = []
for tag, mods in (("CHI", CHI_MOD), ("TAI", TAI_MOD)):
    dm.append(f"OBT_strait_stage_{tag} = {{")
    dm.append("\ticon = GFX_idea_political_drain" if tag == "CHI" else "\ticon = GFX_idea_national_unity")
    dm.append("")
    for k in mods:
        dm.append(f"\t{k} = OBT_ss_{VARNAME[k]}")
    dm.append("}")
    dm.append("")
w("dynmod.txt", "\n".join(dm).rstrip("\n") + "\n")

# ---------------------------------------------------------------- triggers (live value)
T = []
for s, name in enumerate(STAGES):
    lo, hi = LO[s] - 1, (LO[s + 1] - 1 if s < 4 else None)
    cond = [f"check_variable = {{ CHI_taiwan_strait_tension > {lo} }}"] if s else []
    if hi is not None:
        cond.append(f"NOT = {{ check_variable = {{ CHI_taiwan_strait_tension > {hi} }} }}")
    T.append(f"\nOBT_strait_live_{name} = {{\n\tcountry_exists = CHI\n\tCHI = {{\n" + "\n".join("\t\t" + c for c in cond) + "\n\t}\n}\n")
for s, name in enumerate(STAGES[1:], 1):
    T.append(f"""
OBT_strait_at_least_{name} = {{
	custom_trigger_tooltip = {{
		tooltip = OBT_strait_at_least_{name}_tt
		country_exists = CHI
		CHI = {{ check_variable = {{ CHI_taiwan_strait_tension > {LO[s] - 1} }} }}
	}}
}}
""")
for s, name in ((2, "coercion"), (3, "crisis")):
    T.append(f"""
OBT_strait_at_most_{name} = {{
	custom_trigger_tooltip = {{
		tooltip = OBT_strait_at_most_{name}_tt
		country_exists = CHI
		CHI = {{ NOT = {{ check_variable = {{ CHI_taiwan_strait_tension > {LO[s + 1] - 1} }} }} }}
	}}
}}
""")
w("triggers.txt", "".join(T))

# ---------------------------------------------------------------- effects
TRACK = [("trust", "CHI", "CHI_TAI_trust"), ("ussupport", "CHI", "CHI_taiwan_us_support"),
         ("burden", "TAI", "TAI_blockade_burden"), ("ptn", "TAI", "TAI_pressure_to_negotiate"),
         ("usconf", "TAI", "TAI_us_confidence"), ("identity", "TAI", "TAI_taiwanese_identity")]
snap = ["", "OBT_strait_snapshot = {", "\tif = {", "\t\tlimit = {", "\t\t\tcountry_exists = CHI", "\t\t\tcountry_exists = TAI", "\t\t}"]
for key, tag, var in TRACK:
    snap += [f"\t\tset_variable = {{ global.OBT_d_{key} = {tag}.{var} }}",
             f"\t\tsubtract_from_variable = {{ global.OBT_d_{key} = global.OBT_prev_{key} }}",
             f"\t\tset_variable = {{ global.OBT_prev_{key} = {tag}.{var} }}"]
snap += ["\t}", "}", ""]
init = ["", "OBT_strait_init_snapshot = {", "\tif = {", "\t\tlimit = {", "\t\t\tcountry_exists = CHI", "\t\t\tcountry_exists = TAI", "\t\t}"]
for key, tag, var in TRACK:
    init += [f"\t\tset_variable = {{ global.OBT_prev_{key} = {tag}.{var} }}", f"\t\tset_variable = {{ global.OBT_d_{key} = 0 }}"]
init += ["\t}", "}", ""]
E = ["""
OBT_strait_update = {
	if = {
		limit = {
			country_exists = CHI
			country_exists = TAI
		}
		set_variable = { global.OBT_strait_fill = CHI.CHI_taiwan_strait_tension }
		clamp_variable = { var = global.OBT_strait_fill min = 0 max = 100 }
		if = {
			limit = { check_variable = { global.OBT_strait_fill > 79 } }
			set_temp_variable = { OBT_new_stage = 4 }
		}
		else_if = {
			limit = { check_variable = { global.OBT_strait_fill > 59 } }
			set_temp_variable = { OBT_new_stage = 3 }
		}
		else_if = {
			limit = { check_variable = { global.OBT_strait_fill > 39 } }
			set_temp_variable = { OBT_new_stage = 2 }
		}
		else_if = {
			limit = { check_variable = { global.OBT_strait_fill > 19 } }
			set_temp_variable = { OBT_new_stage = 1 }
		}
		else = {
			set_temp_variable = { OBT_new_stage = 0 }
		}
		if = {
			limit = {
				NOT = { has_global_flag = OBT_strait_initialized }
			}
			set_global_flag = OBT_strait_initialized
			set_variable = { global.OBT_strait_stage = OBT_new_stage }
			CHI = { OBT_strait_apply_stage = yes }
			TAI = { OBT_strait_apply_stage = yes }
			OBT_strait_init_snapshot = yes
		}
		else_if = {
			limit = {
				NOT = { check_variable = { global.OBT_strait_stage = OBT_new_stage } }
			}
			set_temp_variable = { OBT_old_stage = global.OBT_strait_stage }
			set_variable = { global.OBT_strait_stage = OBT_new_stage }
			CHI = { OBT_strait_apply_stage = yes }
			TAI = { OBT_strait_apply_stage = yes }
			if = {
				limit = {
					OR = {
						NOT = { has_global_flag = OBT_strait_event_cooldown }
						has_global_flag = { flag = OBT_strait_event_cooldown days > 179 }
					}
					NOT = { CHI = { has_war_with = TAI } }
				}
				clr_global_flag = OBT_strait_event_cooldown
				set_global_flag = OBT_strait_event_cooldown
				if = {
					limit = { check_variable = { OBT_new_stage > OBT_old_stage } }
					CHI = { country_event = { id = obt_strait.1 days = 1 } }
					TAI = { country_event = { id = obt_strait.3 days = 1 } }
				}
				else = {
					CHI = { country_event = { id = obt_strait.2 days = 1 } }
					TAI = { country_event = { id = obt_strait.4 days = 1 } }
				}
			}
		}
	}
}
"""]
E.append("\n".join(snap))
E.append("\n".join(init))
apply = ["OBT_strait_apply_stage = {"]
for tag, mods in (("CHI", CHI_MOD), ("TAI", TAI_MOD)):
    apply += ["\tif = {", f"\t\tlimit = {{ original_tag = {tag} }}"]
    apply += [f"\t\tset_variable = {{ OBT_ss_{VARNAME[k]} = 0 }}" for k in mods]
    for s in range(5):
        lines = [f"\t\t\tset_variable = {{ OBT_ss_{VARNAME[k]} = {vals[s]} }}" for k, vals in mods.items() if vals[s]]
        if lines:
            apply += ["\t\tif = {", f"\t\t\tlimit = {{ check_variable = {{ global.OBT_strait_stage = {s} }} }}"] + lines + ["\t\t}"]
    apply += ["\t\tif = {", f"\t\t\tlimit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = OBT_strait_stage_{tag} }} }} }}",
              f"\t\t\tadd_dynamic_modifier = {{ modifier = OBT_strait_stage_{tag} }}", "\t\t}", "\t}"]
apply.append("}")
E.append("\n" + "\n".join(apply) + "\n")
w("effects.txt", "".join(E))


# ---------------------------------------------------------------- shared effect snippets
def tension(n):
    return (f"if = {{\n\tlimit = {{ country_exists = CHI }}\n\tCHI = {{\n\t\tadd_to_variable = {{ CHI_taiwan_strait_tension = {n} tooltip = CHI_taiwan_strait_tension_tt }}\n"
            f"\t\tclamp_variable = {{ var = CHI_taiwan_strait_tension min = 0 max = 100 }}\n\t}}\n}}\nOBT_strait_update = yes")


def var(owner, v, n):
    body = f"add_to_variable = {{ {v} = {n} tooltip = {v}_tt }}\nclamp_variable = {{ var = {v} min = 0 max = 100 }}"
    if owner == "self":
        return body
    return f"if = {{\n\tlimit = {{ country_exists = {owner} }}\n\t{owner} = {{\n" + "\n".join("\t\t" + l for l in body.split("\n")) + "\n\t}\n}"


def money(n):
    return f"set_temp_variable = {{ treasury_change = {n} }}\nmodify_treasury_effect = yes"


# ---------------------------------------------------------------- decisions
LOC = {}


def D(did, icon, visible, available, cost, summary, effects, ai, extra="", reenable=None, remove=None, modifier=None):
    LOC[f"{did}_tt"] = summary
    out = [f"\t{did} = {{", f"\t\ticon = {icon}", ""]
    if visible:
        out += ["\t\tvisible = {", ind(visible, "\t\t\t"), "\t\t}", ""]
    if available:
        out += ["\t\tavailable = {", ind(available, "\t\t\t"), "\t\t}", ""]
    out.append(f"\t\tcost = {cost}")
    if reenable:
        out.append(f"\t\tdays_re_enable = {reenable}")
    if remove:
        out.append(f"\t\tdays_remove = {remove}")
    if extra:
        out.append(extra)
    out.append("")
    if modifier:
        out += ["\t\tmodifier = {", ind(modifier, "\t\t\t"), "\t\t}", ""]
    out += ["\t\tcomplete_effect = {", f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision {did}"',
            f"\t\t\tcustom_effect_tooltip = {did}_tt", ind(effects, "\t\t\t"), "\t\t}", ""]
    out += ["\t\tai_will_do = {", ind(ai, "\t\t\t"), "\t\t}", "\t}", ""]
    return "\n".join(out)


NOWAR = "country_exists = TAI\nNOT = { has_war_with = TAI }"
NOWAR_T = "country_exists = CHI\nNOT = { has_war_with = CHI }"
FW = "has_completed_focus = CHI_SAR_one_china_framework"
BT = "has_completed_focus = TAI_bt_root"


def mod(f, trig):
    return f"modifier = {{\n\tfactor = {f}\n\t{trig}\n}}"


LOWSTAB_CHI = "modifier = {\n\tfactor = 3\n\thas_stability < 0.45\n}"
chi = [
    D("OBT_CHI_crisis_hotline", "generic_political_discourse", NOWAR, "OBT_strait_at_least_coercion = yes", 50,
      "§GLowers§! Cross-Strait Tension by §G10§! and raises trust with Taipei.",
      tension(-10) + "\n" + var("self", "CHI_TAI_trust", 3),
      "base = 2\n" + mod(4, "OBT_strait_at_least_crisis = yes") + "\n" + LOWSTAB_CHI + "\n" + mod(3, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH") + "\n" + mod(0.25, "has_global_flag = CHI_HEGEMON_FOCUS_PATH"), reenable=180),
    D("OBT_CHI_quiet_channel", "generic_research", NOWAR, "", 25,
      "§GLowers§! Cross-Strait Tension by §G5§! and raises trust with Taipei.",
      tension(-5) + "\n" + var("self", "CHI_TAI_trust", 2),
      "base = 1\nmodifier = {\n\tfactor = 3\n\tOBT_strait_at_least_coercion = yes\n\thas_stability < 0.5\n}\n" + mod(2, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH"), reenable=120),
    D("OBT_CHI_stern_warning", "generic_operation", NOWAR, "OBT_strait_at_most_crisis = yes", 25,
      "§RRaises§! Cross-Strait Tension by §R6§!. Washington's support for Taiwan grows, and so does Taiwanese identity.",
      tension(6) + "\n" + var("self", "CHI_taiwan_us_support", 2) + "\n" + var("TAI", "TAI_taiwanese_identity", 1),
      "base = 1\n" + mod(3, "has_global_flag = CHI_HEGEMON_FOCUS_PATH") + "\n" + mod(0, "has_stability < 0.4") + "\n" + mod(0.2, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH"), reenable=90),
    D("OBT_CHI_patrol_surge", "generic_naval", FW + "\n" + NOWAR, "OBT_strait_at_most_crisis = yes", 50,
      "§RRaises§! Cross-Strait Tension by §R10§!. Trains our navy, costs money and raises U.S. support for Taiwan.",
      tension(10) + "\n" + money(-3) + "\nnavy_experience = 10\n" + var("self", "CHI_taiwan_us_support", 3),
      "base = 1\n" + mod(3, "has_global_flag = CHI_HEGEMON_FOCUS_PATH") + "\n" + mod(0, "has_stability < 0.45") + "\n" + mod(0, "has_active_mission = bankruptcy_incoming_collapse") + "\n" + mod(0.2, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH"), reenable=120),
    D("OBT_CHI_economic_incentives", "generic_factory", FW + "\n" + NOWAR, "", 50,
      "§GLowers§! Cross-Strait Tension by §G6§!. Costs money, builds trust and deepens Taiwan's dependence on the mainland.",
      tension(-6) + "\n" + money(-5) + "\n" + var("self", "CHI_TAI_trust", 5) + "\n" + var("TAI", "TAI_mainland_dependence", 3),
      "base = 2\n" + mod(3, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH") + "\n" + mod(0, "has_active_mission = bankruptcy_incoming_collapse") + "\n" + mod(0.5, "has_global_flag = CHI_HEGEMON_FOCUS_PATH"), reenable=180),
    D("OBT_CHI_prepare_contingency", "generic_intelligence_operation", FW + "\n" + NOWAR + "\nOBT_strait_at_least_brink = yes",
      "NOT = { has_wargoal_against = TAI }\nhas_war_support > 0.5", 150,
      "Gives a §Ywar goal§! against Taiwan. It does §Rnot§! declare war. Costs stability and raises U.S. support for Taiwan.",
      "create_wargoal = {\n\ttype = annex_everything\n\ttarget = TAI\n}\nadd_stability = -0.05\n" + var("self", "CHI_taiwan_us_support", 8) + "\nTAI = { add_war_support = 0.05 }",
      "base = 0\nmodifier = {\n\tadd = 5\n\thas_global_flag = CHI_HEGEMON_FOCUS_PATH\n\thas_stability > 0.5\n}", reenable=365, extra="\t\twar_with_on_complete = TAI"),
]
LOWSTAB_TAI = "modifier = {\n\tfactor = 3\n\thas_stability < 0.4\n}"
tai = [
    D("OBT_TAI_crisis_hotline", "generic_political_discourse", NOWAR_T, "OBT_strait_at_least_coercion = yes", 50,
      "§GLowers§! Cross-Strait Tension by §G8§!. Washington's confidence in Taipei rises.",
      tension(-8) + "\n" + var("self", "TAI_us_confidence", 3),
      "base = 2\n" + mod(4, "OBT_strait_at_least_crisis = yes") + "\n" + LOWSTAB_TAI + "\n" + mod(2, "has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH"), reenable=180),
    D("OBT_TAI_reaffirm_status_quo", "generic_research", NOWAR_T, "", 25,
      "§GLowers§! Cross-Strait Tension by §G5§!. Frustrates the identity-minded base.",
      tension(-5) + "\n" + var("self", "TAI_taiwanese_identity", -2),
      "base = 1\n" + mod(3, "OBT_strait_at_least_crisis = yes") + "\n" + mod(2, "has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH") + "\n" + mod(0.3, "has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH"), reenable=120),
    D("OBT_TAI_cross_strait_trade_talks", "generic_factory", NOWAR_T, "OBT_strait_at_most_coercion = yes", 50,
      "§GLowers§! Cross-Strait Tension by §G6§!. Builds trust, at the price of deeper dependence on the mainland.",
      tension(-6) + "\n" + var("self", "TAI_mainland_dependence", 4) + "\n" + var("CHI", "CHI_TAI_trust", 4) + "\n" + var("self", "TAI_taiwanese_identity", -1),
      "base = 1\n" + mod(4, "has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH") + "\n" + mod(0, "has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH"), reenable=180),
    D("OBT_TAI_raise_readiness", "generic_operation", NOWAR_T, "OBT_strait_at_least_coercion = yes", 50,
      "§RRaises§! Cross-Strait Tension by §R3§!. Costs money; better organization and defense for 120 days.",
      tension(3) + "\n" + money(-3),
      "base = 1\n" + mod(4, "OBT_strait_at_least_crisis = yes") + "\n" + mod(0, "has_active_mission = bankruptcy_incoming_collapse"), reenable=180, remove=120,
      modifier="army_org_factor = 0.05\narmy_defence_factor = 0.03"),
    D("OBT_TAI_civil_defense_drill", "generic_welfare", BT + "\n" + NOWAR_T, "", 50,
      "§RRaises§! Cross-Strait Tension by §R2§!. Costs money; raises stability, war support and national coordination.",
      tension(2) + "\n" + money(-2) + "\nadd_stability = 0.02\nadd_war_support = 0.03\n" + var("self", "TAI_national_coordination", 3),
      "base = 2\n" + mod(3, "OBT_strait_at_least_coercion = yes") + "\n" + mod(0, "has_active_mission = bankruptcy_incoming_collapse"), reenable=180),
    D("OBT_TAI_brief_washington", "generic_research", NOWAR_T, "OBT_strait_at_least_friction = yes", 50,
      "§RRaises§! Cross-Strait Tension by §R3§!. U.S. support for Taiwan grows.",
      tension(3) + "\n" + var("CHI", "CHI_taiwan_us_support", 4),
      "base = 1\n" + mod(3, "OBT_strait_at_least_crisis = yes") + "\n" + mod(0.3, "has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH"), reenable=180),
]
w("TAI_strait_decisions.txt", "OBT_cross_strait_category = {\n" + "\n".join(tai).rstrip("\n") + "\n}\n\nCHI_SAR_decisions_category = {\n" + "\n".join(chi).rstrip("\n") + "\n}\n")

# ---------------------------------------------------------------- events
EV, EVLOC = [], []


def tl(n):
    return tension(n).split("\n")


def vl(owner, v, n):
    return var(owner, v, n).split("\n")


def event(n, tag, title, descs, pic, opts):
    eid = f"obt_strait.{n}"
    out = ["country_event = {", f"\tid = {eid}", f"\ttitle = {eid}.t"]
    EVLOC.append(f' {eid}.t: "{title}"')
    for s, text in descs:
        out.append(f"\tdesc = {{ text = {eid}.d{s} trigger = {{ check_variable = {{ global.OBT_strait_stage = {s} }} }} }}")
        EVLOC.append(f' {eid}.d{s}: "{text}"')
    out += [f"\tpicture = {pic}", "\tis_triggered_only = yes", "", "\ttrigger = {", f"\t\toriginal_tag = {tag}", "\t}", ""]
    for i, (text, eff, ai) in enumerate(opts):
        key = f"{eid}.{'abc'[i]}"
        out += ["\toption = {", f"\t\tname = {key}", f'\t\tlog = "[GetDateText]: [This.GetName]: {key} executed"']
        out += ["\t\t" + l for l in eff]
        out += ["\t\tai_chance = {"] + ["\t\t\t" + l for l in ai] + ["\t\t}", "\t}", ""]
        EVLOC.append(f' {key}: "{text}"')
    out[-1] = "}"
    EV.append("\n".join(out) + "\n")


def m(f, t):
    return ["modifier = {", f"\tfactor = {f}", f"\t{t}", "}"]


HEG, PEACE, LOW = m(3, "has_global_flag = CHI_HEGEMON_FOCUS_PATH"), m(3, "has_global_flag = CHI_PEACEFUL_RISE_FOCUS_PATH"), m(3, "has_stability < 0.45")
FORT, ACC = m(3, "has_global_flag = TAI_ISLAND_FORTRESS_FOCUS_PATH"), m(3, "has_global_flag = TAI_ACCOMMODATION_FOCUS_PATH")
event(1, "CHI", "Tension Rises in the Strait",
      [(1, "Relations with Taipei have cooled into open friction. Our diplomats and theirs trade sharper words, and the business community is starting to notice."),
       (2, "Our pressure on Taipei is now unmistakable. Every exercise and every statement is read in Taipei, Tokyo and Washington as coercion."),
       (3, "The Strait has entered a crisis. Foreign navies are watching, markets are nervous, and the cost to our own economy is rising."),
       (4, "The Strait stands at the brink. One miscalculation could start a war that no one in Beijing has formally decided to fight.")],
      "GFX_CHI_event_navy_ship",
      [("Press the advantage.", tl(3) + ["navy_experience = 5"] + vl("self", "CHI_taiwan_us_support", 2), ["base = 30"] + HEG),
       ("Hold our position.", vl("self", "CHI_TAI_trust", -1), ["base = 40"]),
       ("Signal restraint.", tl(-5) + ["add_political_power = -25"], ["base = 30"] + PEACE + LOW)])
event(2, "CHI", "The Strait Cools",
      [(0, "Cross-Strait relations are calm. Trade flows, tourists cross and the generals on both sides are quiet."),
       (1, "The worst of the confrontation has passed. Relations remain cool, but the danger of a clash has eased."),
       (2, "The crisis has eased into steady pressure. We have room to choose our next step."),
       (3, "We have stepped back from the brink, though the Strait remains in crisis.")],
      "GFX_politics_talks",
      [("Bank the calm.", vl("self", "CHI_TAI_trust", 3), ["base = 50"] + PEACE),
       ("Remind Taipei of our resolve.", tl(3) + vl("self", "CHI_TAI_trust", -2), ["base = 50"] + HEG)])
event(3, "TAI", "Pressure Across the Strait",
      [(1, "Beijing's tone has hardened and cross-Strait relations have slipped into friction. The public is uneasy but calm."),
       (2, "Beijing is now openly coercing us: exercises near our waters, warnings to our partners, pressure on our businesses."),
       (3, "The Strait is in crisis. Shipping insurers are raising rates, and Washington is asking what we intend to do."),
       (4, "The Strait stands at the brink. Our forces are on alert, and the world is watching both capitals.")],
      "GFX_CHI_event_missiles_taiwan",
      [("Stand firm.", tl(2) + vl("self", "TAI_taiwanese_identity", 2), ["base = 35"] + FORT),
       ("Call for calm and dialogue.", tl(-4) + vl("self", "TAI_us_confidence", 2) + vl("self", "TAI_taiwanese_identity", -1), ["base = 35"] + ACC + LOW),
       ("Consult Washington.", vl("CHI", "CHI_taiwan_us_support", 2) + ["add_political_power = -25"], ["base = 30"])])
event(4, "TAI", "The Strait Eases",
      [(0, "Relations with the mainland are calm. Ferries run full, investors are confident and the coast guard has a quiet season."),
       (1, "The confrontation has eased into friction. The pressure has not gone away, but the danger has passed for now."),
       (2, "Beijing's pressure continues, but the crisis atmosphere has lifted."),
       (3, "We have stepped back from the brink, though the Strait remains in crisis.")],
      "GFX_negotiations",
      [("Reopen the channels.", vl("CHI", "CHI_TAI_trust", 3) + vl("self", "TAI_mainland_dependence", 2), ["base = 50"] + ACC),
       ("Stay vigilant.", vl("self", "TAI_national_coordination", 2), ["base = 50"] + FORT)])
w("Taiwan_Strait_Meter.txt", "add_namespace = obt_strait\n\n" + "\n".join(EV))
w("events_loc.yml", "\n".join(EVLOC) + "\n")

# ---------------------------------------------------------------- GUI
BX, BW = 8, 404


def text(name, x, y, key, font="hoi_16mbs", wd=90, fmt="left", tt=None):
    s = ["\t\tinstantTextBoxType = {", f'\t\t\tname = "{name}"', f"\t\t\tposition = {{ x = {x} y = {y} }}",
         f'\t\t\tfont = "{font}"', f'\t\t\ttext = "{key}"', f"\t\t\tmaxWidth = {wd}", "\t\t\tmaxHeight = 20", f"\t\t\tformat = {fmt}"]
    if tt:
        s.append(f'\t\t\tpdx_tooltip = "{tt}"')
    s.append("\t\t}")
    return "\n".join(s)


def window(tag, inds):
    L = ["\tcontainerWindowType = {", f'\t\tname = "OBT_{tag}_strait_meter_window"', "\t\tsize = { width = 440 height = 170 }", "\t\tposition = { x = 0 y = 0 }", ""]
    L.append(text(f"OBT_{tag}_strait_title", BX, 0, "OBT_strait_meter_title", "hoi_20bs", 430, "left", "OBT_strait_meter_tt"))
    L += ["\t\ticonType = {", '\t\t\tname = "OBT_strait_bar"', '\t\t\tquadTextureSprite = "GFX_OBT_strait_tension_bar"',
          f"\t\t\tposition = {{ x = {BX} y = 31 }}", '\t\t\tpdx_tooltip = "OBT_strait_meter_tt"', "\t\t}",
          "\t\ticonType = {", '\t\t\tname = "OBT_strait_bar_frame"', '\t\t\tspriteType = "GFX_OBT_strait_frame"',
          "\t\t\tposition = { x = 0 y = 24 }", "\t\t\talwaystransparent = yes", "\t\t}"]
    for i, st in enumerate(STAGES):
        L.append(text(f"OBT_{tag}_strait_label_{st}", BX + round(BW * i / 5), 78, f"OBT_strait_label_{st}", "hoi_16mbs", round(BW / 5), "center", f"OBT_strait_stage_{st}_tt"))
    L.append(text(f"OBT_{tag}_strait_stage_line", BX, 98, "OBT_strait_stage_line", "hoi_16mbs", 425, "left", "OBT_strait_stage_info_tt"))
    for i, (key, tt) in enumerate(inds):
        L.append(text(f"OBT_{tag}_strait_ind_{i}", BX + (i % 2) * 215, 124 + (i // 2) * 22, key, "hoi_16mbs", 210, "left", tt))
    L.append("\t}")
    return "\n".join(L)


chi_ind = [("OBT_ind_chi_trust", "OBT_ind_chi_trust_tt"), ("OBT_ind_us_support", "OBT_ind_us_support_tt"),
           ("OBT_ind_chi_burden", "OBT_ind_chi_burden_tt"), ("OBT_ind_chi_ptn", "OBT_ind_chi_ptn_tt")]
tai_ind = [("OBT_ind_tai_ptn", "OBT_ind_ptn_tt"), ("OBT_ind_tai_burden", "OBT_ind_burden_tt"),
           ("OBT_ind_us_confidence", "OBT_ind_us_confidence_tt"), ("OBT_ind_identity", "OBT_ind_identity_tt")]
w("OBT_strait_meter.gui", "guiTypes = {\n" + window("CHI", chi_ind) + "\n\n" + window("TAI", tai_ind) + "\n}\n")
sg = ["scripted_gui = {"]
for tag in ("CHI", "TAI"):
    sg += [f"\tOBT_{tag}_strait_meter = {{", f'\t\twindow_name = "OBT_{tag}_strait_meter_window"', "\t\tcontext_type = decision_category",
           "\t\tdirty = CHI.CHI_taiwan_strait_tension", "", "\t\tproperties = {", "\t\t\tOBT_strait_bar = { frame = CHI.CHI_taiwan_strait_tension }", "\t\t}", "\t}", ""]
sg[-1] = "}"
w("99_OBT_strait_scripted_guis.txt", "\n".join(sg) + "\n")

# ---------------------------------------------------------------- scripted localisation
SL = []


def defined(name, entries, default):
    SL.append("defined_text = {")
    SL.append(f"\tname = {name}")
    for trig, key in entries:
        SL.append(f"\ttext = {{ trigger = {{ {trig} }} localization_key = {key} }}")
    SL.append(f"\ttext = {{ localization_key = {default} }}")
    SL.append("}")
    SL.append("")


live = [f"OBT_strait_live_{s} = yes" for s in STAGES]
defined("OBT_strait_stage_name", [(live[i], f"OBT_strait_stage_{STAGES[i]}_colored") for i in range(4)], "OBT_strait_stage_brink_colored")
for i, st in enumerate(STAGES):
    defined(f"OBT_strait_label_{st}_text", [(live[i], f"OBT_strait_label_{st}_on")], f"OBT_strait_label_{st}_off")
defined("OBT_strait_stage_line_text", [(live[i], f"OBT_strait_line_{STAGES[i]}") for i in range(4)], "OBT_strait_line_brink")
defined("OBT_strait_stage_info_text", [(live[i], f"OBT_strait_info_{STAGES[i]}") for i in range(4)], "OBT_strait_info_brink")
defined("OBT_strait_active_effects", [(f"check_variable = {{ global.OBT_strait_stage = {i} }}", f"OBT_strait_effects_{STAGES[i]}") for i in range(4)], "OBT_strait_effects_brink")
w("99_OBT_strait_scripted_localisation.txt", "\n".join(SL))

# ---------------------------------------------------------------- localisation
L = []
add = lambda k, v: L.append(f' {k}: "{v}"')
add("OBT_cross_strait_category", "Cross-Strait Relations")
add("OBT_cross_strait_category_desc", "Beijing's pressure and Taipei's response move one shared measure, §YCross-Strait Tension§!. Higher stages harden the island's resolve but cost it trade and political capital; calm pays both sides. Pressure is not control: no stage forces war, annexation or capitulation.")
add("OBT_strait_meter_title", "CROSS-STRAIT TENSION: §Y[?CHI.CHI_taiwan_strait_tension|0]§!/100 · [OBT_strait_stage_name]")
legend = "   ".join(f"§{COL[i]}{NAMES[i]}§! {LO[i]}-{(LO[i + 1] - 1) if i < 4 else 100}" for i in range(5))
add("OBT_strait_meter_tt", "§YCross-Strait Tension§! is shared by Beijing and Taipei. It rises with coercion, blockades and provocations, and falls with dialogue, trade and restraint.\\n\\n" + legend + "\\n\\n§YModifiers now in force§! (updated at the start of each month):\\n[OBT_strait_active_effects]\\n\\nNo stage starts a war, annexes Taiwan or forces it to capitulate.")
for i, st in enumerate(STAGES):
    up = st.upper()
    add(f"OBT_strait_stage_{st}", NAMES[i])
    add(f"OBT_strait_stage_{st}_colored", f"§{COL[i]}{up}{' (!)' if i == 4 else ''}§!")
    add(f"OBT_strait_label_{st}", f"[OBT_strait_label_{st}_text]")
    add(f"OBT_strait_label_{st}_on", f"§{COL[i]}{up}§!")
    add(f"OBT_strait_label_{st}_off", f"§g{NAMES[i]}§!")
    rng = f"{LO[i]}-{(LO[i + 1] - 1) if i < 4 else 100}"
    add(f"OBT_strait_stage_{st}_tt", f"§{COL[i]}{NAMES[i]}§! ({rng})\\n$OBT_strait_effects_{st}$")
    eff = f"§YChina§!: {fmt_effects(CHI_MOD, i)}\\n§YTaiwan§!: {fmt_effects(TAI_MOD, i)}"
    add(f"OBT_strait_effects_{st}", eff)
LINES = ["Rises to §YFriction§! at §Y20§!.",
         "Rises to §OCoercion§! at §Y40§! · falls to §GCalm§! below §Y20§!.",
         "Rises to §RCrisis§! at §Y60§! · falls to §YFriction§! below §Y40§!.",
         "Rises to §RBrink§! at §Y80§! · falls to §OCoercion§! below §Y60§!.",
         "The highest stage · falls to §RCrisis§! below §Y80§!."]
UNLOCK = ["No crisis decisions are needed. Trade talks and quiet diplomacy keep the peace.",
          "Taiwan can brief Washington. Trade talks remain open.",
          "Crisis hotlines open for both sides. Taiwan can raise readiness. Trade talks remain open.",
          "Taiwan can declare a §YBlue Tiger Emergency§! without a blockade. Trade talks close; warnings and patrol surges remain possible.",
          "Beijing can §Yprepare a contingency war goal§!; war still needs a declaration. Warnings and patrol surges are exhausted."]
for i, st in enumerate(STAGES):
    add(f"OBT_strait_line_{st}", f"§YStage:§! [OBT_strait_stage_name]   {LINES[i]}")
    add(f"OBT_strait_info_{st}", f"§{COL[i]}{NAMES[i]}§!\\n\\n§YEffects§!\\n$OBT_strait_effects_{st}$\\n\\n§YDecisions§!\\n{UNLOCK[i]}\\n\\n§YMoving the meter§!\\nCoercion, blockades, warnings, patrol surges and readiness raise tension. Hotlines, quiet channels, trade talks, incentives and reaffirming the status quo lower it.")
add("OBT_strait_stage_line", "[OBT_strait_stage_line_text]")
add("OBT_strait_stage_info_tt", "[OBT_strait_stage_info_text]")
add("OBT_strait_at_least_friction_tt", "Cross-Strait Tension is at least §YFriction§! (20)")
add("OBT_strait_at_least_coercion_tt", "Cross-Strait Tension is at least §OCoercion§! (40)")
add("OBT_strait_at_least_crisis_tt", "Cross-Strait Tension is at least §RCrisis§! (60)")
add("OBT_strait_at_least_brink_tt", "Cross-Strait Tension is at §RBrink§! (80)")
add("OBT_strait_at_most_coercion_tt", "Cross-Strait Tension is below §RCrisis§! (60)")
add("OBT_strait_at_most_crisis_tt", "Cross-Strait Tension is below §RBrink§! (80)")
add("OBT_ind_chi_trust", "Cross-Strait Trust: §Y[?CHI.CHI_TAI_trust|0]§! ([?global.OBT_d_trust|+=0])")
add("OBT_ind_us_support", "U.S. Support for Taiwan: §Y[?CHI.CHI_taiwan_us_support|0]§! ([?global.OBT_d_ussupport|-=0])")
add("OBT_ind_chi_burden", "Taiwan Blockade Burden: §Y[?TAI.TAI_blockade_burden|0]§! ([?global.OBT_d_burden|0])")
add("OBT_ind_chi_ptn", "Taipei's Will to Negotiate: §Y[?TAI.TAI_pressure_to_negotiate|0]§! ([?global.OBT_d_ptn|+=0])")
add("OBT_ind_tai_ptn", "Pressure to Negotiate: §Y[?TAI.TAI_pressure_to_negotiate|0]§! ([?global.OBT_d_ptn|-=0])")
add("OBT_ind_tai_burden", "Blockade Burden: §Y[?TAI.TAI_blockade_burden|0]§! ([?global.OBT_d_burden|-=0])")
add("OBT_ind_us_confidence", "U.S. Confidence in Taipei: §Y[?TAI.TAI_us_confidence|0]§! ([?global.OBT_d_usconf|+=0])")
add("OBT_ind_identity", "Taiwan-Centered Identity: §Y[?TAI.TAI_taiwanese_identity|0]§! ([?global.OBT_d_identity|0])")
TREND = "\\n\\nThe number in brackets is the change over the last month."
add("OBT_ind_chi_trust_tt", "§YCross-Strait Trust§!: how far Beijing and Taipei trust each other.\\n§GRises§! with hotlines, quiet channels, incentives and trade talks.\\n§RFalls§! with pressure and broken talks." + TREND)
add("OBT_ind_us_support_tt", "§YU.S. Support for Taiwan§! is Washington's commitment to deterring Beijing.\\n§RRises§! when China escalates or Taipei briefs Washington.\\nIt is §Ynot§! the same as U.S. Confidence in Taipei." + TREND)
add("OBT_ind_us_confidence_tt", "§YU.S. Confidence in Taipei§! is Washington's trust in Taiwan's government.\\n§GRises§! with restraint, hotlines and keeping promises.\\n§RFalls§! with provocations and first strikes.\\nIt is §Ynot§! the same as U.S. Support for Taiwan." + TREND)
add("OBT_ind_chi_burden_tt", "§YTaiwan Blockade Burden§!: how hard a blockade is hitting Taiwan's economy after its preparations. Above 40 it pushes Taipei toward talks." + TREND)
add("OBT_ind_burden_tt", "§YBlockade Burden§!: how hard a blockade is hitting our economy after reserves, rationing and shipping guarantees are counted.\\n§RRises§! with blockades. §GFalls§! with preparations and when the blockade lifts." + TREND)
add("OBT_ind_chi_ptn_tt", "§YTaipei's Will to Negotiate§! (our estimate of Taiwan's Pressure to Negotiate). Above 70, with a real blockade burden, Taipei may seek staged talks. It can leave them at every stage; it never capitulates automatically." + TREND)
add("OBT_ind_ptn_tt", "§YPressure to Negotiate§!: how strongly the public wants talks with Beijing.\\n§RRises§! under blockade. §GFalls§! with stability, preparations and American support.\\nA high value can open staged talks, which we can leave at every stage; it never forces capitulation." + TREND)
add("OBT_ind_identity_tt", "§YTaiwan-Centered Identity§!: how strongly the public identifies with Taiwan rather than China. Beijing's coercion tends to raise it; reaffirming the status quo and trade talks lower it." + TREND)
add("OBT_strait_stage_CHI", "Cross-Strait Tension")
add("OBT_strait_stage_TAI", "Cross-Strait Tension")
DEC = {
    "OBT_CHI_crisis_hotline": ("Open the Crisis Hotline", "A direct line between the two capitals lets officials talk before an incident becomes a war."),
    "OBT_CHI_quiet_channel": ("Quiet Channel to Taipei", "Intermediaries carry private messages across the Strait without either side losing face."),
    "OBT_CHI_stern_warning": ("Issue a Stern Warning", "A public warning to the authorities in Taipei. It will please nationalists at home and alarm Washington."),
    "OBT_CHI_patrol_surge": ("Surge Coast Guard Patrols", "More ships, closer to Taiwan's waters, more often. It trains our crews and costs us abroad."),
    "OBT_CHI_economic_incentives": ("Offer Economic Incentives", "Preferential terms for Taiwanese farmers, firms and investors make the mainland harder to refuse."),
    "OBT_CHI_prepare_contingency": ("Prepare a Taiwan Contingency", "Draw up the political and military case for war. It gives us a war goal; it does not declare war, and every capital will see it."),
    "OBT_TAI_crisis_hotline": ("Use the Crisis Hotline", "Call Beijing directly to stop an incident from escalating. Washington welcomes the restraint."),
    "OBT_TAI_reaffirm_status_quo": ("Reaffirm the Status Quo", "A public statement that Taiwan seeks neither independence nor unification today. It calms the Strait and frustrates our own base."),
    "OBT_TAI_cross_strait_trade_talks": ("Reopen Cross-Strait Trade Talks", "Talks on trade and investment lower the temperature, at the price of deeper dependence on the mainland."),
    "OBT_TAI_raise_readiness": ("Raise Readiness", "Cancel leave, disperse aircraft and man the coastal defenses. Beijing will call it a provocation."),
    "OBT_TAI_civil_defense_drill": ("Nationwide Civil Defense Drill", "Air-raid sirens, shelters and supply points across the island: a rehearsal for the day we hope never comes."),
    "OBT_TAI_brief_washington": ("Brief Washington", "Share our intelligence on Beijing's pressure with the United States to strengthen its commitment to deterrence."),
}
for k, (n, d) in DEC.items():
    add(k, n)
    add(k + "_desc", d)
for k, v in LOC.items():
    add(k, v)
for line in L:
    assert "—" not in line, line
w("loc_main.yml", "\n".join(L) + "\n")
print("built", len(L), "loc keys,", len(chi) + len(tai), "decisions")
