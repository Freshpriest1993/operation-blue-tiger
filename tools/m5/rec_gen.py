#!/usr/bin/env python3
"""Generate Operation Blue Tiger milestone-5 Return to the Mainland events and localisation."""
import os
import sys

OUT = sys.argv[1]
NS = "reclamation"
R = "TAI_bop_restoration"
S = "TAI_bop_self_determination"


def bop(v):
    side = R if v < 0 else S
    return f"add_power_balance_value = {{\n\tid = TAI_reclamation_bop\n\tvalue = {v}\n\ttooltip_side = {side}\n}}"


def var(v, amt):
    return f"add_to_variable = {{ {v} = {amt} tooltip = {v}_tt }}\nclamp_variable = {{ var = {v} min = 0 max = 100 }}"


def ifchi(body):
    return "if = {\n\tlimit = { country_exists = CHI }\n\tCHI = {\n" + "\n".join("\t\t" + l for l in body.split("\n")) + "\n\t}\n}"


TAI_TRIG = "original_tag = TAI"
EVENTS = []


def E(n, title, desc, pic, options, trigger=TAI_TRIG, once=False):
    EVENTS.append(dict(n=n, title=title, desc=desc, pic=pic, options=options, trigger=trigger, once=once))


def O(text, eff="", ai=50, trig=None):
    return dict(text=text, eff=eff, ai=ai, trig=trig)


AH = "Alternate history. "

E(1, "A Pact for National Reclamation",
  AH + "Since 1991 the Republic of China has renounced force against the mainland. Now the cabinet asks the nation to accept a war to restore the Republic on both sides of the Strait. Party leaders, generals and civic groups gather in Taipei to set the terms. Many on the island will fight only if they are promised a say in what comes after.",
  "GFX_TAI_roc", [
      O("Promise a referendum on Taiwan's future after the war.",
        "set_country_flag = TAI_pledge_referendum\nadd_political_power = -50\nadd_timed_idea = { idea = TAI_reclamation_referendum_pledge days = 730 }\n" + bop(0.15) + "\n" + ifchi("add_war_support = 0.05"), 30),
      O("Guarantee Taiwan's autonomy within the restored Republic.",
        "set_country_flag = TAI_pledge_autonomy\nadd_political_power = -25\nadd_timed_idea = { idea = TAI_reclamation_autonomy_pledge days = 730 }\n" + bop(0.05) + "\n" + ifchi("add_war_support = 0.02"), 50),
      O("Offer no concessions. The Republic is one.",
        "set_country_flag = TAI_pledge_none\nadd_timed_idea = { idea = TAI_reclamation_no_concessions days = 730 }\n" + bop(-0.10), 20),
  ])

E(2, "Across the Strait",
  AH + "The landings have been thrown back and the island holds. The general staff now proposes what no government in Taipei has seriously planned for half a century: to carry the war to the mainland itself.",
  "GFX_TAI_tank_bridge", [
      O("For the Republic.", "add_war_support = 0.05\n" + var("TAI_us_confidence", -5)),
  ])

E(3, "Taipei Carries the War to the Mainland",
  AH + "Having repelled a Chinese invasion, the Republic of China has announced it will pursue the war onto the mainland. Our commitment covers Taiwan's defense. It was never meant to cover this.",
  "GFX_USA_event_congress", [
      O("Stand by Taipei, but no further guarantees.",
        "TAI = {\n\t" + var("TAI_us_confidence", 5).replace("\n", "\n\t") + "\n}", 60),
      O("Urge restraint publicly.",
        "TAI = {\n\t" + var("TAI_us_confidence", -10).replace("\n", "\n\t") + "\n}", 40),
  ], trigger="original_tag = USA")

E(4, "Taipei Strikes First",
  AH + "The Republic of China has attacked the mainland while Beijing is in crisis. No American administration promised to support a Taiwanese war of choice, and Congress is demanding answers.",
  "GFX_USA_event_congress", [
      O("Condemn the attack and suspend assistance.",
        "TAI = {\n\t" + var("TAI_us_confidence", -20).replace("\n", "\n\t") + "\n\tif = {\n\t\tlimit = { has_idea = TAI_american_assistance }\n\t\tremove_ideas = TAI_american_assistance\n\t}\n}", 70),
      O("Stay quiet and watch.",
        "TAI = {\n\t" + var("TAI_us_confidence", -5).replace("\n", "\n\t") + "\n}", 30),
  ], trigger="original_tag = USA")

E(5, "The Mainland Falls",
  AH + "Resistance across the mainland has collapsed. The flag of the Republic flies again over cities it left in 1949. Now come the provinces, the ministries and hundreds of millions of people who were never asked.",
  "GFX_TAI_roc", [
      O("Restore the Republic's authority.",
        "if = {\n\tlimit = { country_exists = CHI }\n\tannex_country = { target = CHI transfer_troops = no }\n}\nclr_country_flag = TAI_reclamation_war\nROC_init_administration = yes\nadd_political_power = 100\ncountry_event = { id = reclamation.6 days = 45 }", 100),
  ], once=True)

E(6, "The Postwar Settlement",
  AH + "The war is won. The promises made in Taipei before it began now fall due, and the island is watching to see whether they will be kept.",
  "GFX_politics_negotiations", [
      O("Honor the referendum pledge.",
        "country_event = { id = reclamation.7 days = 30 }", 60, "has_country_flag = TAI_pledge_referendum"),
      O("Negotiate continued association.",
        "country_event = { id = reclamation.11 days = 7 }", 60, "has_country_flag = TAI_pledge_autonomy"),
      O("Repudiate the pledge.",
        "country_event = { id = reclamation.12 days = 1 }", 10, "OR = { has_country_flag = TAI_pledge_referendum has_country_flag = TAI_pledge_autonomy }"),
      O("Rule the whole Republic from Taipei.",
        "add_stability = -0.05\nremove_power_balance = { id = TAI_reclamation_bop }\ncountry_event = { id = reclamation.16 days = 60 }", 100, "has_country_flag = TAI_pledge_none"),
  ], once=True)

E(7, "The Referendum",
  AH + "Voters across Taiwan, Penghu, Kinmen and Matsu are asked one question: should Taiwan form its own state, or remain part of the restored Republic?",
  "GFX_election_day", [
      O("Count the votes.",
        "random_list = {\n\t50 = {\n\t\tmodifier = {\n\t\t\tadd = 25\n\t\t\tpower_balance_value = { id = TAI_reclamation_bop value > 0.2 }\n\t\t}\n\t\tmodifier = {\n\t\t\tadd = 25\n\t\t\tpower_balance_value = { id = TAI_reclamation_bop value > 0.6 }\n\t\t}\n\t\tmodifier = {\n\t\t\tadd = 15\n\t\t\tcheck_variable = { TAI_taiwanese_identity > 60 }\n\t\t}\n\t\tcountry_event = { id = reclamation.8 days = 3 }\n\t}\n\t50 = {\n\t\tmodifier = {\n\t\t\tadd = 25\n\t\t\tpower_balance_value = { id = TAI_reclamation_bop value < -0.2 }\n\t\t}\n\t\tmodifier = {\n\t\t\tadd = 25\n\t\t\tpower_balance_value = { id = TAI_reclamation_bop value < -0.6 }\n\t\t}\n\t\tcountry_event = { id = reclamation.10 days = 3 }\n\t}\n}", 100),
  ], once=True)

E(8, "Taiwan Chooses Its Own Path",
  AH + "A majority has voted for a separate Taiwanese state. The government will keep its word: the island becomes its own country, and the Republic on the mainland continues under a provisional government of its own. Taipei must decide where it will stand.",
  "GFX_TAI_taiwan", [
      O("Keep the promise.",
        "TAI_split_successor_states = yes\nTAI_renounce_mainland_claims = yes\nset_cosmetic_tag = TAI_TAIWAN\nadd_ideas = TAI_cross_strait_partnership\nCHI = { add_ideas = TAI_cross_strait_partnership }\nadd_stability = 0.05\n" + var("TAI_us_confidence", 10) + "\nif = {\n\tlimit = { has_idea = TAI_reclamation_referendum_pledge }\n\tremove_ideas = TAI_reclamation_referendum_pledge\n}\ncountry_event = { id = reclamation.9 days = 1 }", 100),
  ], once=True)

E(9, "Two Republics",
  AH + "There are now two governments where there was one: Taiwan, and the Republic of China on the mainland. Which will you lead?",
  "GFX_TAI_roc", [
      O("Remain with Taiwan.", "add_political_power = 25", 100),
      O("Lead the Republic on the mainland.", "CHI = { change_tag_from = ROOT }", 0, "is_ai = no\ncountry_exists = CHI"),
  ], once=True)

E(10, "Taiwan Votes to Remain",
  AH + "A majority has voted to keep Taiwan within the restored Republic. The government now owes the island the terms of that association.",
  "GFX_election_rally", [
      O("Draft the terms.", "add_stability = 0.03\ncountry_event = { id = reclamation.11 days = 7 }", 100),
  ], once=True)

E(11, "Terms of Association",
  AH + "Negotiators from the island and the new provincial administrations have two models on the table: one Republic with a chartered autonomy for Taiwan, or a federal union in which Taiwan governs itself under the Republic's protection.",
  "GFX_negotiations", [
      O("One Republic, with an autonomous Taiwan.",
        "add_ideas = TAI_taiwan_autonomy_charter\nremove_power_balance = { id = TAI_reclamation_bop }\nset_country_flag = TAI_reclamation_concluded\nif = {\n\tlimit = { has_idea = TAI_reclamation_autonomy_pledge }\n\tremove_ideas = TAI_reclamation_autonomy_pledge\n}", 70),
      O("A federal union under the mainland government.",
        "TAI_split_successor_states = yes\nset_cosmetic_tag = TAI_TAIWAN\nadd_ideas = TAI_taiwan_autonomy_charter\nCHI = { puppet = TAI }\nif = {\n\tlimit = { has_idea = TAI_reclamation_autonomy_pledge }\n\tremove_ideas = TAI_reclamation_autonomy_pledge\n}\ncountry_event = { id = reclamation.9 days = 1 }", 30),
  ], once=True)

E(12, "The Pact Is Broken",
  AH + "The government has set aside the promise it made before the war. On the island, the people who were asked to fight for the Republic in exchange for a voice now say they were deceived.",
  "GFX_FRA_political_scandal", [
      O("The Republic cannot be divided.",
        "if = {\n\tlimit = { power_balance_value = { id = TAI_reclamation_bop value > 0.2 } }\n\tadd_ideas = TAI_broken_reclamation_pact_severe\n}\nelse = {\n\tadd_ideas = TAI_broken_reclamation_pact\n}\n" + var("TAI_us_confidence", -10) + "\n" + var("TAI_taiwanese_identity", 10) + "\nremove_power_balance = { id = TAI_reclamation_bop }\ncountry_event = { id = reclamation.13 days = 30 }\ncountry_event = { id = reclamation.14 days = 150 }", 100),
  ], once=True)

E(13, "Protests in Taipei",
  AH + "Hundreds of thousands have filled Ketagalan Boulevard demanding the promised referendum. Opposition legislators have joined them, and the police ask for instructions.",
  "GFX_election_protests", [
      O("Open talks with the protest leaders.",
        "add_political_power = -50\nadd_stability = 0.02", 60),
      O("Clear the streets.",
        "add_timed_idea = { idea = TAI_island_crackdown days = 180 }\n" + var("TAI_us_confidence", -10) + "\n" + var("TAI_taiwanese_identity", 5), 40),
  ], once=True)

E(14, "A General Strike on the Island",
  AH + "Dockworkers in Kaohsiung and engineers in Hsinchu have walked out together. Shipping is stopped and the foundries are idle until the government honors its pledge.",
  "GFX_TAI_sunflower", [
      O("Concede ground to the strikers.",
        "add_political_power = -75\nif = {\n\tlimit = { has_idea = TAI_broken_reclamation_pact_severe }\n\tswap_ideas = {\n\t\tremove_idea = TAI_broken_reclamation_pact_severe\n\t\tadd_idea = TAI_broken_reclamation_pact\n\t}\n}", 60),
      O("Break the strike.",
        "add_stability = -0.05\n" + var("TAI_us_confidence", -10) + "\n" + var("TAI_taiwanese_identity", 5), 40),
  ], trigger="original_tag = TAI\nOR = {\n\thas_idea = TAI_broken_reclamation_pact\n\thas_idea = TAI_broken_reclamation_pact_severe\n}", once=True)

E(16, "Voices on the Island",
  AH + "No promise was made before the war, and none is owed. Still, many on Taiwan now ask whether the island they defended has become one province among thirty.",
  "GFX_election_protests", [
      O("Promise local self-government.",
        "add_ideas = TAI_taiwan_autonomy_charter\nadd_political_power = -50", 60),
      O("Nothing has changed. Taiwan is the Republic.",
        "add_stability = -0.03\n" + var("TAI_taiwanese_identity", 5), 40),
  ], once=True)

E(18, "The Crusade Falters",
  AH + "The war has ended without the mainland in our hands. The generals blame the politicians, the politicians blame Washington, and the island counts the cost of a gamble that failed.",
  "GFX_CHI_event_missiles_taiwan", [
      O("Return to the defense of Taiwan.",
        "add_stability = -0.05\nadd_political_power = -50\n" + bop(0.20) + "\n" + var("TAI_taiwanese_identity", 10), 100),
  ])

E(19, "A Republic on the Mainland",
  AH + "A provisional government of the Republic of China now sits on the mainland, separate from Taipei. It inherits a vast country, a broken party-state and an army that fought against it months ago. Its first decision is where to govern from.",
  "GFX_CHI_event_national_congress_started", [
      O("Return to Nanjing, the Republic's old capital.",
        "if = {\n\tlimit = { 536 = { is_owned_and_controlled_by = ROOT } }\n\tset_capital = { state = 536 }\n}", 50),
      O("Govern from Beijing.",
        "if = {\n\tlimit = { 547 = { is_owned_and_controlled_by = ROOT } }\n\tset_capital = { state = 547 }\n}", 50),
  ], trigger="original_tag = CHI", once=True)

E(20, "The Republic Restored",
  AH + "Civil administration now reaches every region under the Republic's flag. The provisional decrees lapse and the ordinary laws of the Republic take their place.",
  "GFX_TAI_roc", [
      O("A new beginning.",
        "ROC_end_administration = yes\nadd_ideas = ROC_republic_restored\nadd_stability = 0.05", 100),
  ], trigger="has_country_flag = ROC_provisional_administration", once=True)


def ind(text, t):
    return [t + l if l else l for l in text.split("\n")]


ev = ["add_namespace = " + NS, ""]
loc = []
for e in EVENTS:
    eid = f"{NS}.{e['n']}"
    ev += ["country_event = {", f"\tid = {eid}", f"\ttitle = {eid}.t", f"\tdesc = {eid}.d", f"\tpicture = {e['pic']}", "\tis_triggered_only = yes"]
    if e["once"]:
        ev.append("\tfire_only_once = yes")
    ev += ["", "\ttrigger = {"] + ind(e["trigger"], "\t\t") + ["\t}", ""]
    loc += [f' {eid}.t: "{e["title"]}"', f' {eid}.d: "{e["desc"]}"']
    for i, o in enumerate(e["options"]):
        key = f"{eid}.{'abcefgh'[i]}"
        ev += ["\toption = {", f"\t\tname = {key}"]
        if o["trig"]:
            ev += ["\t\ttrigger = {"] + ind(o["trig"], "\t\t\t") + ["\t\t}"]
        ev.append(f'\t\tlog = "[GetDateText]: [This.GetName]: {key} executed"')
        if o["eff"]:
            ev += ind(o["eff"], "\t\t")
        ev += ["\t\tai_chance = {", f"\t\t\tbase = {o['ai']}", "\t\t}", "\t}", ""]
        loc.append(f' {key}: "{o["text"]}"')
    ev[-1] = "}"
    ev.append("")
for line in loc:
    assert "—" not in line, line
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "Taiwan_Reclamation.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(ev).rstrip("\n") + "\n")
with open(os.path.join(OUT, "events_loc.yml"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(loc) + "\n")
print(len(EVENTS), "events")
