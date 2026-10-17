#!/usr/bin/env python3
"""Generate the Operation Blue Tiger milestone-5 mainland Republic of China focus tree."""
import os
import sys

OUT = sys.argv[1]
AH = "Alternate history. "


def reform():
    return "if = {\n\tlimit = { has_country_flag = ROC_provisional_administration }\n\tadd_to_variable = { ROC_admin_reforms = 1 }\n\tROC_update_administration = yes\n}"


def build(state, typ, lvl, slots=0):
    inner = []
    if slots:
        inner.append(f"\tadd_extra_state_shared_building_slots = {slots}")
    inner += ["\tadd_building_construction = {", f"\t\ttype = {typ}", f"\t\tlevel = {lvl}", "\t\tinstant_build = yes", "\t}"]
    return "if = {\n\tlimit = { " + str(state) + " = { is_owned_and_controlled_by = ROOT } }\n\t" + str(state) + " = {\n" + "\n".join("\t" + l for l in inner) + "\n\t}\n}"


def money(n):
    return f"set_temp_variable = {{ treasury_change = {n} }}\nmodify_treasury_effect = yes"


def party(i, v):
    return f"add_to_variable = {{ party_pop_array^{i} = {v} }}\nrecalculate_party = yes"


def opinion(tag, mod="recent_actions_positive"):
    return f"if = {{\n\tlimit = {{ country_exists = {tag} }}\n\tadd_opinion_modifier = {{ target = {tag} modifier = {mod} }}\n\t{tag} = {{ add_opinion_modifier = {{ target = ROOT modifier = {mod} }} }}\n}}"


F = []


def f(fid, icon, x, y, name, desc, reward, pre=(), mutex=(), filt="FOCUS_FILTER_POLITICAL", cost=10, ai=10, available=None):
    F.append(dict(id="ROC_m_" + fid, icon=icon, x=x, y=y, name=name, desc=AH + desc, reward=reward,
                  pre=[["ROC_m_" + p for p in g] for g in pre], mutex=["ROC_m_" + m for m in mutex], filt=filt, cost=cost, ai=ai, available=available))


f("provisional_government", "Focus_Parliament_Constitution", 10, 0, "The Provisional Government",
  "A government of the Republic sits on the mainland for the first time since 1949. Before it can rule it must exist: a cabinet, a budget and a chain of command that reaches beyond the capital.",
  "add_political_power = 100\nadd_stability = 0.05", cost=5)

f("temporary_provisions", "Generic_Ripping_Papers", 2, 1, "End the Emergency Decrees",
  "The provisional decrees that carried the Republic through the war were meant to be temporary. Ending them early tells the country that the Republic means to govern by law.",
  "add_stability = 0.03\nadd_political_power = 50", pre=[["provisional_government"]])
f("national_assembly", "MNT_democracy", 1, 2, "Convene a National Assembly",
  "Delegates from every province meet to draft the Republic's postwar constitution.",
  "add_political_power = 75\nadd_stability = 0.02", pre=[["temporary_provisions"]])
f("three_principles", "Generic_Conservatism", 3, 2, "Revive the Three Principles",
  "Nationalism, democracy and the people's livelihood: Sun Yat-sen's program was written for this country before it was carried to Taiwan.",
  "add_ideas = ROC_three_principles_revived", pre=[["temporary_provisions"]])
f("amnesty", "Generic_Secret_Meeting", 0, 3, "Amnesty for Party Members",
  "Tens of millions belonged to the old ruling party. An amnesty keeps the county offices staffed and the trains running, at the price of leaving yesterday's officials in place.",
  "add_stability = 0.05\nadd_war_support = -0.03\n" + reform(), pre=[["national_assembly"]], mutex=["lustration"])
f("lustration", "anti_corruption", 2, 3, "Lustration of the Cadres",
  "Senior officials of the old regime are barred from public office. The purge is popular with the victims of the old order and leaves many offices empty.",
  "add_stability = -0.05\nadd_political_power = 100\ndecrease_corruption = yes", pre=[["national_assembly"]], mutex=["amnesty"])
f("local_self_government", "Generic_Major_City", 1, 4, "Local Self-Government",
  "County and city elections give local communities a stake in the Republic and take some of the burden off the provisional administration.",
  "add_stability = 0.03\n" + reform(), pre=[["amnesty", "lustration"]])
f("first_elections", "Election", 1, 5, "The First Free National Elections",
  "For the first time, the whole country votes for its government.",
  "add_political_power = 100\nadd_stability = 0.05\n" + party(1, 0.03), pre=[["local_self_government"]])
f("constitutional_court", "MEX_Defend_the_constitution", 3, 5, "A Constitutional Court",
  "Judges independent of the party and the army will decide what the new constitution means.",
  "add_stability = 0.03\ndecrease_corruption = yes", pre=[["three_principles"]])
f("republic_endures", "Generic_Liberalism", 2, 6, "The Republic Endures",
  "A free government has survived its first years on the mainland.",
  "add_political_power = 150\nadd_stability = 0.05", pre=[["first_elections"], ["constitutional_court"]])

f("restore_ministries", "Generic_Command_Power", 7, 1, "Restore the Ministries",
  "The ministries are staffed again, partly by officials from Taipei and partly by former mainland civil servants willing to serve.",
  "add_political_power = 50\n" + reform(), pre=[["provisional_government"]], filt="FOCUS_FILTER_STABILITY")
f("reconstruction_program", "Generic_Public_Works", 7, 2, "The Reconstruction Program",
  "War damage, abandoned projects and neglected provinces: a national program sets priorities for all of them.",
  "add_ideas = ROC_reconstruction_program", pre=[["restore_ministries"]], filt="FOCUS_FILTER_INDUSTRY")
f("rebuild_railways", "Generic_Railroads", 6, 3, "Rebuild the Trunk Railways",
  "The trunk lines between Beijing, Wuhan, Shanghai and Guangzhou carry the country. Bridges and junctions destroyed in the war come first.",
  build(570, "infrastructure", 1) + "\n" + build(547, "infrastructure", 1) + "\n" + build(534, "infrastructure", 1), pre=[["reconstruction_program"]], filt="FOCUS_FILTER_INDUSTRY")
f("power_grid", "Efficient_Oil_Production_Focus_Icon_V2", 8, 3, "Restore the Power Grid",
  "Factories cannot reopen until the power stations and transmission lines do.",
  build(540, "industrial_complex", 1, 1) + "\n" + build(541, "industrial_complex", 1, 1), pre=[["reconstruction_program"]], filt="FOCUS_FILTER_INDUSTRY")
f("return_the_displaced", "Generic_Red_Cross", 7, 4, "Return the Displaced",
  "Millions fled the fighting. Bringing them home is the first test of whether the Republic can care for its people.",
  "add_stability = 0.05\nadd_manpower = 20000", pre=[["rebuild_railways", "power_grid"]], filt="FOCUS_FILTER_STABILITY")
f("provincial_governors", "Generic_Imperial_China_Diplomacy", 7, 5, "Appoint Provincial Governors",
  "Civilian governors replace the military administrators who have run the provinces since the war.",
  "add_political_power = 50\n" + reform(), pre=[["return_the_displaced"]], filt="FOCUS_FILTER_STABILITY")

f("new_yuan", "generic_banks", 12, 1, "The New Yuan",
  "A new currency, backed by reserves from Taipei and foreign credit, replaces the old renminbi.",
  "add_stability = 0.02\n" + money(5), pre=[["provisional_government"]], filt="FOCUS_FILTER_INDUSTRY")
f("reopen_coast", "ExpandTrade", 11, 2, "Reopen the Coastal Markets",
  "The ports of Shanghai, Tianjin and Guangzhou reopen to world trade under the Republic's flag.",
  "add_ideas = ROC_open_coast", pre=[["new_yuan"]], filt="FOCUS_FILTER_INDUSTRY")
f("land_to_the_tiller", "agriculture", 13, 2, "Land to the Tiller",
  "On Taiwan, land reform built a class of farmer-owners who backed the Republic. The provisional government offers the same bargain on the mainland.",
  "add_stability = 0.05\n" + party(1, 0.02), pre=[["new_yuan"]], filt="FOCUS_FILTER_STABILITY")
f("taiwanese_capital", "Trade_with_the_east", 11, 3, "Invite Taiwanese Capital",
  "Taiwanese firms know the mainland's factories better than anyone. They are invited back on generous terms.",
  build(538, "industrial_complex", 1, 1) + "\n" + build(537, "industrial_complex", 1, 1) + "\n" + opinion("TAI", "improve_trade"), pre=[["reopen_coast"]], filt="FOCUS_FILTER_INDUSTRY")
f("state_enterprises", "economic_prosperity2", 13, 3, "Restructure the State Enterprises",
  "The giant state enterprises are broken up, sold or put on commercial footing. Layoffs follow.",
  money(10) + "\nadd_stability = -0.03", pre=[["land_to_the_tiller"]], filt="FOCUS_FILTER_INDUSTRY")
f("industrial_heartland", "BLR_Hi_Tech_Park", 12, 4, "Rebuild the Industrial Heartland",
  "The northeast and the Yangtze valley are rebuilt as the Republic's industrial base.",
  build(552, "industrial_complex", 1, 1) + "\n" + build(570, "industrial_complex", 1, 1) + "\n" + build(586, "industrial_complex", 1, 1), pre=[["taiwanese_capital", "state_enterprises"]], filt="FOCUS_FILTER_INDUSTRY")
f("second_miracle", "Generic_Major_City", 12, 5, "A Second Economic Miracle",
  "What Taiwan did in the 1960s, the mainland now tries at fifty times the scale.",
  "add_political_power = 50\nadd_stability = 0.03\n" + build(540, "industrial_complex", 1, 1) + "\n" + build(547, "industrial_complex", 1, 1), pre=[["industrial_heartland"]], filt="FOCUS_FILTER_INDUSTRY")

f("national_army", "Generic_Soldiers_Defense", 17, 1, "One National Army",
  "Units from Taiwan and new mainland formations are combined under a single command loyal to the constitution, not a party.",
  "add_ideas = ROC_national_army", pre=[["provisional_government"]], filt="FOCUS_FILTER_MILITARY")
f("integrate_pla", "Generic_Infantry_Training", 16, 2, "Integrate the PLA Remnants",
  "Former PLA officers and men who swear loyalty to the Republic keep their posts. The army gains experience and inherits old loyalties.",
  "add_manpower = 50000\narmy_experience = 20\nadd_stability = -0.05", pre=[["national_army"]], mutex=["disband_pla"], filt="FOCUS_FILTER_MILITARY")
f("disband_pla", "Generic_Volunteer_Corps", 18, 2, "Disband the PLA",
  "The old army is demobilized and a new one is recruited from volunteers. It is smaller, untested and politically reliable.",
  "add_stability = 0.03\nadd_war_support = 0.05", pre=[["national_army"]], mutex=["integrate_pla"], filt="FOCUS_FILTER_MILITARY", cost=15)
f("seat_at_un", "USA_diplomatic_corps", 17, 3, "Reclaim the Security Council Seat",
  "The Republic of China held a permanent seat on the Security Council until 1971. Its diplomats argue that it never lost the right to it.",
  "add_political_power = 100\nadd_stability = 0.02", pre=[["integrate_pla", "disband_pla"]], filt="FOCUS_FILTER_POLITICAL")
f("friends_in_washington", "american_government", 16, 4, "Friends in Washington",
  "Washington supported Taiwan for half a century. The Republic on the mainland asks it to extend that friendship.",
  opinion("USA"), pre=[["seat_at_un"]], filt="FOCUS_FILTER_POLITICAL")
f("compact_with_taipei", "accept_treaty", 18, 4, "A Compact with Taipei",
  "Two governments descended from one republic agree to keep the peace, trade freely and settle disputes by negotiation.",
  "if = {\n\tlimit = {\n\t\tcountry_exists = TAI\n\t\tNOT = { has_idea = TAI_cross_strait_partnership }\n\t}\n\tadd_ideas = TAI_cross_strait_partnership\n}\n" + opinion("TAI", "improve_trade"), pre=[["seat_at_un"]], filt="FOCUS_FILTER_POLITICAL",
  available="country_exists = TAI")
f("settle_borders", "Generic_Imperial_China_Diplomacy", 17, 5, "Settle the Borders",
  "Moscow and New Delhi want to know whether the Republic will honor the border agreements of the People's Republic. It will, for a price.",
  "add_political_power = 50\nadd_stability = 0.03\n" + opinion("SOV") + "\n" + opinion("RAJ"), pre=[["friends_in_washington", "compact_with_taipei"]], filt="FOCUS_FILTER_POLITICAL")
f("free_china_among_nations", "align_to_america", 17, 6, "A Free China Among Nations",
  "The Republic takes its place in the world as a great power and a democracy.",
  "add_political_power = 100\nadd_war_support = 0.05\narmy_experience = 25", pre=[["settle_borders"]], filt="FOCUS_FILTER_POLITICAL")

f("free_china", "TAI_civilwar_legacy", 10, 7, "Free China",
  "The civil war that divided the Chinese nation in 1949 is over. The Republic Sun Yat-sen founded governs the mainland again, by consent.",
  "add_political_power = 150\nadd_stability = 0.10", pre=[["republic_endures"], ["provincial_governors"], ["second_miracle"], ["free_china_among_nations"]], cost=15)

ids = {x["id"] for x in F}
for x in F:
    for g in x["pre"]:
        for p in g:
            assert p in ids, p
    for m in x["mutex"]:
        assert m in ids, m
pos = {(x["x"], x["y"]) for x in F}
assert len(pos) == len(F), "overlap"


def ind(s, t):
    return [t + l if l else l for l in s.split("\n")]


out = ["focus_tree = {", "\tid = roc_mainland_focus", "", "\tcountry = {", "\t\tfactor = 0", "\t}", "", "\tcontinuous_focus_position = { x = 50 y = 1200 }", ""]
loc = []
for x in F:
    out += ["\tfocus = {", f"\t\tid = {x['id']}", f"\t\ticon = {x['icon']}", f"\t\tx = {x['x'] * 2}", f"\t\ty = {x['y']}", f"\t\tcost = {x['cost']}"]
    for g in x["pre"]:
        out.append("\t\tprerequisite = { " + " ".join(f"focus = {p}" for p in g) + " }")
    if x["mutex"]:
        out.append("\t\tmutually_exclusive = { " + " ".join(f"focus = {m}" for m in x["mutex"]) + " }")
    out.append(f"\t\tsearch_filters = {{ {x['filt']} }}")
    if x["available"]:
        out += ["\t\tavailable = {"] + ind(x["available"], "\t\t\t") + ["\t\t}"]
    out += ["\t\tcompletion_reward = {", f'\t\t\tlog = "[GetDateText]: [Root.GetName]: Focus {x["id"]}"'] + ind(x["reward"], "\t\t\t") + ["\t\t}"]
    out += ["\t\tai_will_do = {", f"\t\t\tbase = {x['ai']}"]
    if "industrial_complex" in x["reward"]:
        out += ["\t\t\tmodifier = {", "\t\t\t\tfactor = 0", "\t\t\t\tcan_staff_an_industrial_complex = no", "\t\t\t}"]
    out += ["\t\t}", "\t}", ""]
    loc += [f' {x["id"]}: "{x["name"]}"', f' {x["id"]}_desc: "{x["desc"]}"']
out[-1] = "}"
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "05_roc_mainland.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(out) + "\n")
with open(os.path.join(OUT, "focus_loc.yml"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(loc) + "\n")
print(len(F), "focuses")
