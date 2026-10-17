# Operation Blue Tiger: Taiwan focus tree specification (milestone 1).
# Effects mini-language (expanded by gen.py):
#   pp:N  stab:X  ws:X  money:N (billions, negative = cost)  corr:-1 (decrease corruption one level)
#   var:<key>:N   chi:<trust|tension|ussupport>:N
#   idea:ID  rmidea:ID  timed:ID:DAYS  posture:N
#   tech:CAT:BONUS:USES  xp:army|navy|air:N  build:<scripted building effect>
#   party:INDEX:DELTA  opinion:TAG:MODIFIER  flag:NAME  raw:<script>
# Availability tokens:
#   transfer  dpp  kmt  pfp  blue  ly  date>YYYY.M.D  noflag:NAME  flag:NAME  raw:<trigger>

BRANCHES = []

def branch(key, name, x, filters):
    b = {"key": key, "name": name, "x": x, "filters": filters, "focuses": []}
    BRANCHES.append(b)
    return b

def F(b, fid, name, icon, days, desc, pre=(), excl=(), avail=(), eff=(), ai=1, filt=None, track=""):
    b["focuses"].append({
        "id": fid, "name": name, "icon": icon, "days": days, "desc": desc,
        "pre": list(pre), "excl": list(excl), "avail": list(avail), "eff": list(eff),
        "ai": ai, "filt": filt, "track": track,
    })

POL = ["FOCUS_FILTER_POLITICAL"]

# ---------------------------------------------------------------- Branch 1
su = branch("su", "The 2000 Succession", 0, POL)
T = "trunk"
F(su, "TAI_su_millennium_election", "The Millennium Election", "Election", 35,
  "President Lee Teng-hui is barred from a third term, and the Kuomintang has split over his succession. Three serious candidates now compete for the first presidency of the new century.",
  eff=["pp:50"], ai=10, track=T)
F(su, "TAI_su_heal_kmt_split", "Heal the KMT Split", "Generic_Secret_Meeting", 35,
  "James Soong left the Kuomintang to run on his own after Lee chose Lien Chan. Bringing his supporters back could unite the Pan-Blue vote, at the cost of reopening old quarrels.",
  pre=["TAI_su_millennium_election"], excl=["TAI_su_voters_decide"], avail=["raw:date < 2000.3.18"],
  eff=["party:1:0.04", "party:14:-0.04", "stab:-0.02"], track=T)
F(su, "TAI_su_voters_decide", "Let the Voters Decide", "Election_graphics", 35,
  "We will not manipulate a divided field. The election will be decided at the ballot box, whoever the winner turns out to be.",
  pre=["TAI_su_millennium_election"], eff=["stab:0.03", "pp:25"], ai=3, track=T)
F(su, "TAI_su_lee_legacy", "Lee Teng-hui's Legacy", "TAI_civilwar_legacy", 35,
  "Lee dismantled the emergency constitution, opened direct presidential elections and described cross-Strait ties as a special state-to-state relationship. His successor inherits both the reforms and Beijing's anger.",
  pre=["TAI_su_millennium_election"], eff=["var:identity:5", "chi:tension:3", "pp:25"], track=T)
F(su, "TAI_su_peaceful_transfer", "The Peaceful Transfer of Power", "MNT_democracy", 70,
  "Whoever won, the presidency must change hands under the constitution. A smooth handover proves that our democracy can survive a change of ruling party.",
  pre=[("TAI_su_heal_kmt_split", "TAI_su_voters_decide")], avail=["transfer"],
  eff=["stab:0.05", "var:milconf:-5", "pp:50"], ai=5, track=T)
F(su, "TAI_su_form_cabinet", "Form the Cabinet", "Generic_Command_Power", 35,
  "The new president appoints a premier who must work with the Legislative Yuan. A cross-party appointment buys cooperation and reassures the officer corps.",
  pre=["TAI_su_peaceful_transfer"], eff=["var:milconf:5", "pp:25"], ai=5, track=T)
F(su, "TAI_su_minority_government", "A Government Without a Majority", "Generic_Factionalism", 35,
  "We hold the presidency but not the Legislative Yuan. Budgets, procurement and reform will all have to be negotiated with the opposition.",
  pre=["TAI_su_form_cabinet"], excl=["TAI_su_unified_government"], avail=["raw:TAI_government_has_ly_majority = no"],
  eff=["idea:TAI_divided_government", "pp:50"], ai=5, track=T)
F(su, "TAI_su_unified_government", "A Unified Government", "Generic_Conservatism", 35,
  "Our party controls both the presidency and the Legislative Yuan. We can legislate quickly, but critics will call it a return of the old order.",
  pre=["TAI_su_form_cabinet"], avail=["raw:TAI_government_has_ly_majority = yes"],
  eff=["pp:75", "stab:-0.02"], ai=5, track=T)
F(su, "TAI_su_fourth_nuclear", "The Fourth Nuclear Plant Question", "Eu_nuclear_power", 70,
  "The Lungmen plant is already budgeted and under construction. Halting it would honor environmental pledges and provoke a constitutional fight with the legislature; finishing it secures power supply.",
  pre=[("TAI_su_minority_government", "TAI_su_unified_government")],
  eff=["raw:add_tech_bonus = { name = TAI_su_fourth_nuclear bonus = 0.5 uses = 1 category = CAT_nuclear_reactors }", "stab:-0.02"], track=T)
F(su, "TAI_su_2001_recession", "Weather the 2001 Recession", "GENERIC_austerity_measures", 70,
  "The technology downturn has pushed our export economy into its first contraction in decades. Targeted relief and job programmes can keep the slump from becoming a political crisis.",
  pre=["TAI_su_peaceful_transfer"], avail=["date>2001.1.1"],
  eff=["money:-3", "stab:0.04", "raw:add_timed_idea = { idea = TAI_recession_relief days = 365 }"], ai=3, track=T)
F(su, "TAI_su_ly_2001", "The 2001 Legislative Election", "Election", 35,
  "The People First Party and the Taiwan Solidarity Union now contest seats beside the KMT and DPP. A strong campaign can change the balance in the Legislative Yuan.",
  pre=[("TAI_su_minority_government", "TAI_su_unified_government")], avail=["date>2001.6.1"],
  eff=["raw:TAI_campaign_for_ruling_camp = yes", "pp:25"], track=T)
F(su, "TAI_su_second_mandate", "Seek a Second Mandate", "Election_graphics", 70,
  "The next presidential election will judge four years of divided government. We must run on our record and hold our coalition together.",
  pre=["TAI_su_ly_2001"], avail=["date>2003.6.1"],
  eff=["raw:TAI_campaign_for_ruling_camp = yes", "stab:0.02"], track=T)
F(su, "TAI_su_heal_divided_island", "Healing a Divided Island", "Generic_Liberty_Calling", 70,
  "A bitterly contested election has left many citizens doubting the result. Transparent recounts, court review and restraint on both sides can restore faith in the system.",
  pre=["TAI_su_second_mandate"], avail=["date>2004.3.21"], eff=["stab:0.05", "var:ptn:-3"], track=T)
F(su, "TAI_su_second_test", "Democracy's Second Test", "MNT_democracy", 70,
  "The new single-member districts and a weary electorate may hand power to the opposition. Accepting defeat gracefully would show that alternation in power is now routine.",
  pre=["TAI_su_heal_divided_island"], avail=["date>2007.6.1"], eff=["stab:0.04", "pp:50"], track=T)

D = "dpp"
F(su, "TAI_su_dpp_four_noes", "Four Noes and One Without", "Generic_Ripping_Papers", 35,
  "Provided Beijing does not intend to use force, we will not declare independence, change the national title, write state-to-state relations into the constitution, or hold an independence referendum, and we will keep the National Unification Council.",
  pre=["TAI_su_form_cabinet"], avail=["dpp"], eff=["chi:tension:-8", "var:usconf:10", "chi:trust:5"], ai=5, track=D)
F(su, "TAI_su_dpp_cautious_revolutionary", "The Cautious Revolutionary", "Generic_Liberalism", 70,
  "We came to office promising change but without a majority. A former KMT defense minister as premier and steady administration can win time for deeper reform.",
  pre=["TAI_su_dpp_four_noes"], avail=["dpp"], eff=["stab:0.03", "var:milconf:5", "pp:50"], ai=3, track=D)
F(su, "TAI_su_dpp_taiwan_centered", "A Taiwan-Centered State", "TAI_civilwar_legacy", 70,
  "Schools, museums and public life can reflect the island's own history and languages. Identity grows stronger, and Beijing watches every step.",
  pre=["TAI_su_dpp_cautious_revolutionary"], avail=["dpp"], eff=["var:identity:8", "chi:tension:4", "chi:trust:-4"], track=D)
F(su, "TAI_su_dpp_referendum_act", "The Referendum Act", "Generic_Tear_Paper", 70,
  "Frustrated by legislative deadlock, we can give citizens a direct vote on public questions. Washington will judge each referendum by what it asks.",
  pre=["TAI_su_dpp_taiwan_centered"], avail=["dpp", "ly", "date>2003.1.1"], eff=["var:identity:3", "var:usconf:-5", "stab:0.02"], track=D)
F(su, "TAI_su_dpp_status_quo", "Reaffirm the Status Quo", "accept_treaty", 70,
  "We can promise Washington that referendums will not be used to change the island's status. Deep-Green activists will call it a betrayal.",
  pre=["TAI_su_dpp_referendum_act"], excl=["TAI_su_dpp_name_rectification"], avail=["dpp"],
  eff=["var:usconf:10", "chi:tension:-5", "stab:-0.03"], ai=3, track=D)
F(su, "TAI_su_dpp_name_rectification", "Name Rectification", "Generic_Ripping_Papers", 70,
  "State enterprises and government bodies still carry \"China\" in their names. Renaming them asserts a separate identity and alarms both Beijing and Washington.",
  pre=["TAI_su_dpp_referendum_act"], avail=["dpp"], eff=["var:identity:10", "chi:tension:10", "var:usconf:-10"], track=D)
F(su, "TAI_su_dpp_council_ceases", "The Council Ceases to Function", "Generic_Tear_Paper", 70,
  "Our earlier pledge depended on Beijing renouncing force. With more missiles aimed at us, we can declare that the National Unification Council ceases to function without formally abolishing it.",
  pre=["TAI_su_dpp_name_rectification"], avail=["dpp", "raw:custom_trigger_tooltip = { tooltip = TAI_strait_tension_above_49_tt CHI = { check_variable = { CHI_taiwan_strait_tension > 49 } } }"],
  eff=["var:identity:5", "chi:tension:12", "var:usconf:-10"], track=D)
F(su, "TAI_su_dpp_un_bid", "Join the UN as Taiwan", "Afghan_on_the_world_stage", 70,
  "A membership application under the name Taiwan would rally our supporters and draw a public rebuke from Washington, which opposes unilateral changes to the status quo.",
  pre=["TAI_su_dpp_council_ceases"], avail=["dpp", "date>2007.1.1"], eff=["var:identity:10", "var:usconf:-15", "chi:tension:10"], ai=0, track=D)
F(su, "TAI_su_dpp_clean_party", "A Clean Green Party", "BLR_Democratic_clean", 70,
  "We rose to power promising to end black-gold politics. Internal audits and open finances must apply to our own officials too.",
  pre=["TAI_su_dpp_cautious_revolutionary"], avail=["dpp"], eff=["corr:-1", "stab:0.02"], ai=3, track=D)

K = "kmt"
F(su, "TAI_su_kmt_rebuild", "Rebuild the Kuomintang", "Generic_Conservatism", 70,
  "The 2000 split taught the party that it can no longer take power for granted. Reform must start inside the KMT itself.",
  pre=["TAI_su_form_cabinet"], avail=["kmt"], eff=["stab:0.03", "pp:50"], ai=5, track=K)
F(su, "TAI_su_kmt_party_assets", "Settle the Party Assets", "generic_banks", 70,
  "The KMT's business empire was built while party and state were one. Selling or surrendering contested assets removes a constant source of scandal.",
  pre=["TAI_su_kmt_rebuild"], avail=["kmt"], eff=["corr:-1", "stab:0.03"], track=K)
F(su, "TAI_su_kmt_technocrats", "A Government of Technocrats", "Generic_Command_Power", 70,
  "Experienced ministers and planners can deliver results that rallies cannot. Competence is our best answer to the charge of being the old regime.",
  pre=["TAI_su_kmt_rebuild"], avail=["kmt"], eff=["var:reform:10", "raw:add_timed_idea = { idea = TAI_technocratic_cabinet days = 730 }"], ai=3, track=K)
F(su, "TAI_su_kmt_pan_blue", "The Pan-Blue Coalition", "Generic_Secret_Meeting", 35,
  "Cooperation with the People First Party and the New Party turns a divided camp into a working majority.",
  pre=["TAI_su_kmt_rebuild"], avail=["kmt"], eff=["party:1:0.02", "party:14:0.01", "pp:25"], ai=3, track=K)
F(su, "TAI_su_kmt_new_taiwanese", "We Are All New Taiwanese", "Generic_Liberty_Calling", 70,
  "Lee Teng-hui's idea of the New Taiwanese welcomes every community that has made the island its home. It lets the KMT speak to rising local identity without abandoning the ROC.",
  pre=["TAI_su_kmt_pan_blue"], avail=["kmt"], eff=["var:identity:4", "stab:0.03"], track=K)
F(su, "TAI_su_kmt_roc_framework", "Preserve the ROC Framework", "Focus_Parliament_Constitution", 70,
  "We defend the Republic of China constitution as the common ground of the status quo. Beijing finds this easier to work with than formal independence.",
  pre=["TAI_su_kmt_new_taiwanese"], avail=["kmt"], eff=["chi:tension:-5", "chi:trust:5"], track=K)
F(su, "TAI_su_kmt_peace_framework", "Toward a Peace Framework", "NKO_korea_peace", 70,
  "Regular talks and economic ties can lower the risk of war. Every agreement also deepens our dependence on the mainland market.",
  pre=["TAI_su_kmt_roc_framework"], avail=["kmt"], eff=["chi:trust:10", "chi:tension:-5", "var:dep:5"], track=K)
F(su, "TAI_su_kmt_consent", "No Unification Without Consent", "MNT_democracy", 70,
  "Whatever is negotiated across the Strait, no change to our status can take effect without the consent of the people of Taiwan.",
  pre=["TAI_su_kmt_peace_framework"], avail=["kmt"], eff=["var:ptn:-10", "stab:0.03"], ai=3, track=K)
F(su, "TAI_su_kmt_us_ties", "Keep Washington Close", "align_to_america", 70,
  "Better relations with Beijing must not look like drifting away from the United States. Quiet consultation keeps both doors open.",
  pre=["TAI_su_kmt_technocrats"], avail=["kmt"], eff=["var:usconf:8", "chi:ussupport:3"], ai=3, track=K)

P = "pfp"
F(su, "TAI_su_pfp_people_first", "The People First Government", "Generic_Liberty_Calling", 35,
  "James Soong's new party now governs. It must prove it is more than one man's following.",
  pre=["TAI_su_form_cabinet"], avail=["pfp"], eff=["pp:75", "party:14:0.02"], ai=5, track=P)
F(su, "TAI_su_pfp_provincial_network", "Mobilize the Provincial Network", "Generic_Major_City", 70,
  "As provincial governor, Soong built ties with township leaders across the island. Those contacts can carry the new government's programme.",
  pre=["TAI_su_pfp_people_first"], avail=["pfp"], eff=["var:coord:5", "party:14:0.02", "stab:0.02"], track=P)
F(su, "TAI_su_pfp_court_kmt_caucus", "Court the KMT Caucus", "Generic_Secret_Meeting", 70,
  "Many KMT legislators share our outlook if not our party card. Committee posts and shared priorities can win their votes.",
  pre=["TAI_su_pfp_provincial_network"], avail=["pfp"], eff=["party:1:0.02", "party:14:0.02", "stab:-0.02"], track=P)
F(su, "TAI_su_pfp_reunite_blue", "Reunite the Pan-Blue Camp", "Generic_Conservatism", 70,
  "A joint ticket with the KMT would end the split that elected the DPP. It requires sharing power with old rivals.",
  pre=["TAI_su_pfp_court_kmt_caucus"], avail=["pfp"], eff=["rmidea:TAI_divided_government", "pp:50"], track=P)
F(su, "TAI_su_pfp_clean_sweep", "The Clean Sweep", "anti_corruption", 70,
  "We can prosecute vote buying and factional graft even where our own allies benefit. Local factions will resist.",
  pre=["TAI_su_pfp_people_first"], avail=["pfp"], eff=["corr:-1", "stab:-0.02"], track=P)
F(su, "TAI_su_pfp_every_township", "Build Every Township", "Generic_Public_Works", 70,
  "Roads, drainage and schools in neglected townships turn goodwill into votes and better lives.",
  pre=["TAI_su_pfp_provincial_network"], avail=["pfp"], eff=["build:one_random_infrastructure", "build:one_random_infrastructure", "stab:0.02"], track=P)
F(su, "TAI_su_pfp_pragmatic_strait", "A Pragmatic Strait", "Generic_Imperial_China_Diplomacy", 70,
  "We favour practical dealings with Beijing over symbolic confrontation, while keeping the ROC's sovereignty claims intact.",
  pre=["TAI_su_pfp_people_first"], avail=["pfp"], eff=["chi:trust:8", "chi:tension:-5"], track=P)
F(su, "TAI_su_pfp_peace_mechanism", "A Cross-Strait Peace Mechanism", "NKO_korea_peace", 70,
  "A standing channel for crisis talks could prevent accidents at sea and in the air from becoming wars.",
  pre=["TAI_su_pfp_pragmatic_strait"], avail=["pfp"], eff=["chi:trust:5", "chi:tension:-5", "var:dep:5"], track=P)
F(su, "TAI_su_pfp_washington", "Reassure Washington", "align_to_america", 70,
  "Washington must understand that dialogue with Beijing does not mean abandoning our security partnership.",
  pre=["TAI_su_pfp_pragmatic_strait"], avail=["pfp"], eff=["var:usconf:8"], track=P)

# ---------------------------------------------------------------- Branch 2
df = branch("df", "Democratic Fortress", 0, ["FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INTERNAL_AFFAIRS"])
COR = ["FOCUS_FILTER_CORRUPTION", "FOCUS_FILTER_INTERNAL_AFFAIRS"]
F(df, "TAI_df_root", "Consolidate the State, Not the Party", "Strengthening_Russian_Democracy", 70,
  "Taiwan's democracy is young, and many institutions still bear the habits of one-party rule. Our task is to strengthen the state that every future government will inherit.",
  pre=["TAI_su_peaceful_transfer"], eff=["stab:0.03", "var:coord:5"], ai=3, track="rule")
F(df, "TAI_df_justice_minister", "A Reformist Justice Minister", "MEX_Purge_corrupt_judges", 35,
  "An incorruptible minister can promote younger prosecutors and protect them from political pressure, even when they investigate the ruling party.",
  pre=["TAI_df_root"], eff=["var:reform:5", "corr:-1"], filt=COR, track="rule")
F(df, "TAI_df_unshackle_prosecutors", "Unshackle the Prosecutors", "Generic_Policeman", 70,
  "Allowing prosecutors to pursue cases beyond their home district turns rivalry between offices into a race to expose corruption.",
  pre=["TAI_df_justice_minister"], eff=["corr:-1", "stab:-0.02"], filt=COR, track="rule")
F(df, "TAI_df_professional_judiciary", "Professionalize the Judiciary", "MEX_Defend_the_constitution", 70,
  "Better training, evaluation and discipline for judges will slowly build public trust in the courts.",
  pre=["TAI_df_unshackle_prosecutors"], eff=["stab:0.03"], filt=COR, track="rule")
F(df, "TAI_df_grand_justices", "Strengthen the Grand Justices", "Focus_Parliament_Constitution", 70,
  "A respected constitutional court can settle disputes between the president and the legislature before they paralyse government.",
  pre=["TAI_df_professional_judiciary"], eff=["stab:0.03", "pp:25"], track="rule")
F(df, "TAI_df_special_division", "A Special Investigation Division", "Generic_Espionage02", 70,
  "A dedicated unit for high-level corruption delivers fast results, but its power can be turned against political rivals.",
  pre=["TAI_df_grand_justices"], excl=["TAI_df_ordinary_prosecutors"], eff=["corr:-1", "stab:-0.03"], filt=COR, track="rule")
F(df, "TAI_df_ordinary_prosecutors", "Trust the Ordinary Prosecutors", "Generic_Policeman", 70,
  "Leaving high-level cases with regular prosecutors is slower but harder to politicise.",
  pre=["TAI_df_grand_justices"], eff=["stab:0.04"], filt=COR, ai=3, track="rule")

F(df, "TAI_df_black_gold", "Clean Up Black Gold", "BLR_Anti_Corruption", 70,
  "Organized crime figures have sat in our legislature, and local factions have traded votes for public money. Breaking this system is a matter of national security.",
  pre=["TAI_df_root"], eff=["corr:-1", "stab:-0.02"], filt=COR, track="clean")
F(df, "TAI_df_vote_buying", "End the Vote-Buying Economy", "anti_corruption", 70,
  "Prosecuting vote brokers and the candidates who pay them will cost some incumbents their seats.",
  pre=["TAI_df_black_gold"], eff=["corr:-1", "party:1:-0.01"], filt=COR, track="clean")
F(df, "TAI_df_sunshine_laws", "Sunshine Laws", "MEX_War_on_corruption", 70,
  "Asset disclosure and political donation rules let voters and journalists follow the money.",
  pre=["TAI_df_vote_buying"], avail=["ly"], eff=["corr:-1", "stab:0.02"], filt=COR, track="clean")
F(df, "TAI_df_state_enterprises", "Experts, Not Loyalists", "Generic_Command_Power", 70,
  "State enterprises should be run by managers chosen for skill rather than political loyalty.",
  pre=["TAI_df_black_gold"], eff=["raw:add_timed_idea = { idea = TAI_professional_state_enterprises days = 1095 }"], track="clean")
F(df, "TAI_df_farmers_associations", "Reform the Farmers' Associations", "agriculture", 70,
  "County farmers' associations have long channelled credit and patronage to local factions. Reform weakens those networks and angers rural power brokers.",
  pre=["TAI_df_state_enterprises"], eff=["corr:-1", "stab:-0.02"], filt=COR, track="clean")
F(df, "TAI_df_special_funds_audit", "Audit the Special Funds", "generic_banks", 70,
  "Discretionary funds at the top of government invite abuse. Independent audits protect officeholders from temptation and from false accusations alike.",
  pre=["TAI_df_sunshine_laws"], eff=["corr:-1", "stab:0.03"], filt=COR, track="clean")

F(df, "TAI_df_settle_executive", "Settle the Executive Question", "Focus_Parliament_Constitution", 70,
  "The constitution is ambiguous about who directs the cabinet when the president lacks a majority. A clear presidential reading ends a recurring crisis.",
  pre=["TAI_df_root"], eff=["stab:0.03", "pp:50"], track="inst")
F(df, "TAI_df_legislative_reform", "Reform the Legislative Yuan", "EU_reform", 70,
  "Clear committee rules and procedures can make the legislature a place for bargaining rather than brawling.",
  pre=["TAI_df_settle_executive"], avail=["ly"], eff=["rmidea:TAI_divided_government", "pp:50"], track="inst")
F(df, "TAI_df_end_sntv", "End the SNTV System", "Election", 70,
  "Multi-member districts reward factional candidates and extreme positions. Single-member districts with a party list will reshape every campaign.",
  pre=["TAI_df_legislative_reform"], avail=["ly", "date>2004.1.1"], eff=["corr:-1", "stab:0.02"], track="inst")
F(df, "TAI_df_national_assembly", "The National Assembly Votes Itself Out", "EU_constitution", 70,
  "Abolishing the National Assembly moves constitutional ratification to the voters and halves the size of the legislature.",
  pre=["TAI_df_end_sntv"], avail=["date>2005.1.1"], eff=["stab:0.05", "pp:50"], track="inst")
F(df, "TAI_df_control_yuan", "Protect the Control Yuan", "Generic_Policeman", 35,
  "If nominations stall, the Control Yuan can sit empty for years. A confirmation compromise keeps the watchdog working.",
  pre=["TAI_df_settle_executive"], eff=["corr:-1"], filt=COR, track="inst")
F(df, "TAI_df_civil_service", "A Neutral Civil Service", "Generic_Command_Power", 70,
  "Officials who serve whichever party governs are the backbone of a stable democracy.",
  pre=["TAI_df_control_yuan"], eff=["var:coord:5", "var:reform:5"], track="inst")
F(df, "TAI_df_local_government", "Empower Local Government", "Generic_Major_City", 70,
  "Capable county and city governments can keep services running when Taipei is under pressure.",
  pre=["TAI_df_civil_service"], eff=["var:coord:5", "stab:0.02"], track="inst")

F(df, "TAI_df_civil_commissions", "Open the Commissions to Civil Society", "Generic_Workers_Democracy", 35,
  "Human rights, environmental and women's groups can sit on government commissions alongside business and officials.",
  pre=["TAI_df_root"], eff=["stab:0.03"], track="civil")
F(df, "TAI_df_party_tv_exit", "Get the Parties Out of Television", "SER_mil_in_tv", 70,
  "Parties, the government and the military should not own broadcasters. Their exit from the airwaves strengthens media independence.",
  pre=["TAI_df_civil_commissions"], eff=["stab:0.02"], track="civil")
F(df, "TAI_df_public_broadcasting", "Expand Public Broadcasting", "SOV_tv_propaganda", 70,
  "A well-funded public broadcaster offers a trusted source of news in a sensational media market.",
  pre=["TAI_df_party_tv_exit"], eff=["money:-1", "var:ptn:-3"], track="civil")
F(df, "TAI_df_every_community", "Voices of Every Community", "Generic_Liberty_Calling", 70,
  "Hakka and indigenous broadcasting gives every community a voice in national life.",
  pre=["TAI_df_party_tv_exit"], eff=["var:identity:3", "stab:0.02"], track="civil")
F(df, "TAI_df_martial_law_past", "Confront the Martial-Law Past", "Generic_Ripping_Papers", 70,
  "Opening archives and compensating victims of the White Terror acknowledges a painful history. Some officers see it as an attack on the armed forces.",
  pre=["TAI_df_every_community"], eff=["stab:0.03", "var:milconf:-5"], track="civil")

F(df, "TAI_df_rapid_facts", "Rapid Factual Communication", "Socialist_Radio", 70,
  "When rumours spread faster than facts, the government must publish verified information quickly and plainly.",
  pre=["TAI_df_public_broadcasting"], eff=["var:ptn:-3", "stab:0.02"], track="info")
F(df, "TAI_df_media_literacy", "Media Literacy for All", "Generic_Infantry_Training", 70,
  "Teaching citizens to check sources makes disinformation less effective without restricting speech.",
  pre=["TAI_df_rapid_facts"], eff=["var:ptn:-5"], track="info")
F(df, "TAI_df_influence_transparency", "Foreign Influence Transparency", "Generic_Espionage04", 70,
  "Disclosure rules expose covert foreign funding of media and politics while leaving open debate untouched.",
  pre=["TAI_df_media_literacy"], excl=["TAI_df_counter_disinfo"], eff=["var:ptn:-5", "stab:0.02"], ai=3, track="info")
F(df, "TAI_df_counter_disinfo", "Counter-Disinformation Center", "Generic_Intelligence_Gathering", 70,
  "A government center can rebut false stories within hours. Critics fear it may decide what counts as truth.",
  pre=["TAI_df_media_literacy"], eff=["var:ptn:-8", "stab:-0.02"], track="info")

F(df, "TAI_df_political_dna", "Democracy in the Political DNA", "MNT_democracy", 105,
  "Clean elections, independent courts and a free press have become habits that no party can easily undo. Our democracy is now a source of national strength.",
  pre=["TAI_df_national_assembly", "TAI_df_special_funds_audit", ("TAI_df_influence_transparency", "TAI_df_counter_disinfo")],
  eff=["rmidea:TAI_young_democracy", "idea:TAI_consolidated_democracy", "var:ptn:-10"], ai=5, track="info")

# ---------------------------------------------------------------- Branch 3
na = branch("na", "The National Army", 0, ["FOCUS_FILTER_MILITARY_LAWS"])
ARMY = ["FOCUS_FILTER_MILITARY_LAWS", "FOCUS_FILTER_ARMY"]
NAVY = ["FOCUS_FILTER_NAVY"]
AIR = ["FOCUS_FILTER_AIRCRAFT"]
EQ = ["FOCUS_FILTER_EQUIPMENT"]
MAN = ["FOCUS_FILTER_MANPOWER"]
F(na, "TAI_na_rebuild_shield", "Rebuild the Shield", "Generic_Soldiers_Defense", 70,
  "The 1995-96 missile crisis showed that our defense was built for an invasion that might never come first. A national defense review must ask what we are defending against.",
  eff=["army_xp:15", "pp:25"], ai=5, track="civmil")
F(na, "TAI_na_nationalize", "Nationalize the Armed Forces", "Generic_Command_Power", 70,
  "Our officers must serve the constitution rather than any party. The change unsettles commanders raised under the old system.",
  pre=["TAI_na_rebuild_shield", "TAI_su_peaceful_transfer"], eff=["raw:TAI_reduce_party_army_legacy = yes", "var:milconf:-5", "stab:0.02"], ai=5, track="civmil")
F(na, "TAI_na_defense_act", "Implement the National Defense Act", "Homeland_Defense_Act", 70,
  "The National Defense Act unifies command under a civilian minister and makes political neutrality law.",
  pre=["TAI_na_nationalize"], eff=["raw:TAI_reduce_party_army_legacy = yes", "var:milconf:10", "var:reform:5"], ai=5, track="civmil")
F(na, "TAI_na_reassure_commanders", "Reassure the Commanders", "Generic_Morale_Bonus_Focus", 35,
  "Respecting professional judgment and seniority calms the officer corps, though it slows reforms they dislike.",
  pre=["TAI_na_rebuild_shield"], eff=["var:milconf:10", "var:reform:-5"], ai=3, track="civmil")
F(na, "TAI_na_officer_corps", "Professional Officer Corps", "Generic_Pilots", 70,
  "Promotion by merit, joint education and modern staff training build leaders for a changing force.",
  pre=["TAI_na_defense_act"], eff=["raw:add_timed_idea = { idea = TAI_professional_officer_corps days = 1825 }"], track="civmil")
F(na, "TAI_na_political_warfare", "Reform the Political Warfare Department", "Generic_Ripping_Papers", 70,
  "Political officers once taught loyalty to the party. Their new role is morale, welfare and constitutional education.",
  pre=["TAI_na_officer_corps"], eff=["stab:0.02", "var:milconf:5"], track="civmil")
F(na, "TAI_na_joint_command", "Joint Command Reform", "Generic_Command_Power", 105,
  "The army, navy and air force must plan and fight as one force rather than three rival services.",
  pre=["TAI_na_officer_corps"], eff=["raw:TAI_remove_did_joint_penalty = yes", "army_xp:20", "navy_xp:10", "air_xp:10"], track="civmil")

F(na, "TAI_na_reassess_did", "Reassess Defense-in-Depth", "Dutch_Defense_Doctrine1", 70,
  "General Hau Pei-tsun's Decisive Campaign at the Water's Edge aimed to defeat a landing on our beaches. Missiles can now hurt us long before any landing.",
  pre=["TAI_na_rebuild_shield"], eff=["army_xp:10", "pp:25"], ai=5, track="doct")
F(na, "TAI_na_missile_crisis_lessons", "Lessons of the Missile Crisis", "air_defense", 35,
  "The 1996 missile tests closed ports and frightened markets without a single soldier landing. Our next investments must answer that kind of pressure.",
  pre=["TAI_na_reassess_did"], eff=["tech:CAT_surface_to_air_missiles:0.5:1", "var:reform:5"], ai=5, track="doct")
F(na, "TAI_na_outside_territory", "Decisive Campaign Outside the Territory", "TAI_air_forces", 70,
  "We will engage invasion forces at their bases and in the Strait rather than wait for the beaches. After the election, the explicit preemptive option is dropped; the emphasis on air, naval and strike power remains.",
  pre=["TAI_na_missile_crisis_lessons"], eff=["posture:2", "chi:tension:4", "var:milconf:-5"], ai=3, track="doct")
F(na, "TAI_na_effective_deterrence", "Effective Deterrence, Resolute Defense", "american_shield", 70,
  "Putting deterrence first in our defense doctrine signals that active countermeasures now carry real weight.",
  pre=["TAI_na_outside_territory"], eff=["navy_xp:15", "air_xp:15"], track="doct")
F(na, "TAI_na_air_sea_interdiction", "Air-Sea Interdiction", "TAI_navy_forces", 105,
  "Anti-ship aircraft, missile boats and coordinated strikes can attack an invasion fleet while it crosses the Strait.",
  pre=["TAI_na_effective_deterrence"], eff=["tech:CAT_naval_anti_ship_missiles:0.5:2", "navy_xp:15"], filt=NAVY, track="doct")
F(na, "TAI_na_hf2e", "The HF-2E Program", "Generic_MLRS", 105,
  "A domestically built land-attack cruise missile could threaten the bases an invasion would need. Beijing calls it offensive, some legislators oppose its cost, and Washington worries about escalation.",
  pre=["TAI_na_effective_deterrence"], avail=["ly"], eff=["tech:CAT_cruise_missiles:0.75:2", "chi:tension:8", "var:usconf:-5"], filt=EQ, track="doct")
F(na, "TAI_na_hf2e_extended", "Extended-Range Countermeasures", "Generic_MLRS", 140,
  "Longer-range variants increase the number of targets we can hold at risk, and the political cost of building them.",
  pre=["TAI_na_hf2e"], eff=["tech:CAT_ground_launched_cruise_missiles:0.75:2", "chi:tension:8"], filt=EQ, ai=0, track="doct")
F(na, "TAI_na_info_warfare", "Information and Electronic Warfare Command", "Generic_Espionage04", 70,
  "Cyber defense and electronic warfare protect command networks that every other defense depends on.",
  pre=["TAI_na_effective_deterrence"], eff=["tech:CAT_encryption:0.5:2", "var:reform:5"], filt=EQ, track="doct")
F(na, "TAI_na_layered_air_defense", "Layered Air and Missile Defense", "air_defense2", 105,
  "Patriot batteries, indigenous Tien Kung missiles and early-warning radar together reduce the damage a missile salvo can do.",
  pre=["TAI_na_missile_crisis_lessons"], eff=["tech:CAT_surface_to_air_missiles:0.75:2", "build:one_anti_air", "build:one_radar_station"], filt=EQ, track="doct")
F(na, "TAI_na_harden_island", "Harden the Island", "SIN_long_island_costal_defence", 70,
  "Hardened shelters, buried command posts and spare runways help our forces survive the first strike.",
  pre=["TAI_na_missile_crisis_lessons"], eff=["build:one_air_base", "raw:add_timed_idea = { idea = TAI_hardened_shelters days = 1825 }", "army_xp:10"], filt=ARMY, track="doct")
F(na, "TAI_na_repair_runways", "Repair the Runways", "Generic_Transport_Aircraft", 70,
  "Rapid runway repair teams can return damaged airbases to service within hours.",
  pre=["TAI_na_harden_island"], eff=["air_xp:15", "raw:add_timed_idea = { idea = TAI_runway_repair_teams days = 1825 }"], filt=AIR, track="doct")
F(na, "TAI_na_mine_approaches", "Mine the Approaches", "Naval_Robots", 70,
  "Sea mines and fast minelayers make every landing beach a gamble for an invader.",
  pre=["TAI_na_harden_island"], eff=["navy_xp:15", "raw:add_timed_idea = { idea = TAI_mined_approaches days = 1825 }"], filt=NAVY, track="doct")
F(na, "TAI_na_rapid_redeploy", "Rapid Internal Redeployment", "Generic_Train", 70,
  "Road and rail plans let reserves move quickly to wherever an enemy lands.",
  pre=["TAI_na_repair_runways"], eff=["build:one_random_infrastructure", "army_xp:10"], filt=ARMY, track="doct")
F(na, "TAI_na_hard_roc", "Hard ROC", "SIN_total_defense", 105,
  "Su Chi's Hard ROC concept emphasises survival, denial and recovery rather than distant strikes. Programmes already built remain in service.",
  pre=["TAI_na_mine_approaches"], avail=[("raw:date > 2008.1.1", "kmt")], eff=["posture:3", "chi:tension:-3"], track="doct")
F(na, "TAI_na_mobile_fires", "Mobile Coastal Fires", "Generic_MLRS", 105,
  "Truck-mounted anti-ship missiles that hide and move are harder to destroy than fixed batteries.",
  pre=[("TAI_na_mine_approaches", "TAI_na_air_sea_interdiction")], eff=["tech:CAT_naval_anti_ship_missiles:0.5:2", "army_xp:10"], filt=EQ, track="doct")
F(na, "TAI_na_disperse", "Disperse and Survive", "Generic_Underground_Factories", 70,
  "Forces spread across many small sites cannot all be destroyed in one strike.",
  pre=["TAI_na_mobile_fires"], eff=["raw:add_timed_idea = { idea = TAI_dispersed_forces days = 1825 }"], filt=ARMY, track="doct")
F(na, "TAI_na_unmanned", "Unmanned Systems", "Drones", 105,
  "Cheap drones and unmanned boats can watch and strike across the Strait without risking crews.",
  pre=["TAI_na_disperse"], avail=["date>2012.1.1"], eff=["tech:CAT_air_drones:0.75:2", "tech:CAT_land_drones:0.5:1"], filt=EQ, track="doct")
F(na, "TAI_na_odc", "Overall Defense Concept", "Generic_Submarine_Drone", 105,
  "Admiral Lee Hsi-min's concept invests in many small, mobile, survivable systems that deny a stronger enemy control of the littoral.",
  pre=["TAI_na_unmanned"], avail=["date>2017.1.1"], eff=["posture:4", "var:usconf:5"], track="doct")
F(na, "TAI_na_hybrid", "Hybrid Resilience", "Generic_Soldiers_Defense", 105,
  "We keep enough fighters and ships to contest gray-zone pressure in peacetime while building survivable forces for invasion denial.",
  pre=[("TAI_na_air_sea_interdiction", "TAI_na_hard_roc", "TAI_na_odc"), "TAI_na_joint_command"], eff=["posture:5", "army_xp:15"], track="doct")
F(na, "TAI_na_whole_of_society", "Whole-of-Society Defense", "Generic_Volunteer_Corps", 105,
  "Civil defense, reserves and infrastructure operators train together so the whole island can keep functioning under attack.",
  pre=["TAI_na_hybrid", "TAI_na_territorial_defense"], eff=["idea:TAI_whole_of_society_defense", "ws:0.05"], track="doct")
F(na, "TAI_na_fortress_taiwan", "Fortress Taiwan", "american_shield", 140,
  "Every layer of our defense now reinforces the others. Holding it at readiness is expensive and politically demanding.",
  pre=["TAI_na_whole_of_society"], eff=["idea:TAI_fortress_taiwan", "chi:tension:5"], track="doct")

F(na, "TAI_na_manpower_question", "The Manpower Question", "NKO_reserve", 35,
  "We must choose between a smaller professional force, a large conscript army, or a balance of the two.",
  pre=["TAI_na_rebuild_shield"], eff=["pp:25"], filt=MAN, ai=5, track="man")
F(na, "TAI_na_volunteer_reserve_split", "Volunteer / Reserve Split", "Generic_Infantry_Training", 70,
  "Volunteers will staff the first-line force while conscripts fill the reserves.",
  pre=["TAI_na_manpower_question"], excl=["TAI_na_professional_force", "TAI_na_extended_conscription"], eff=["idea:TAI_volunteer_reserve_split"], filt=MAN, ai=5, track="man")
F(na, "TAI_na_professional_force", "Professional First-Line Force", "Generic_Pilots", 70,
  "Long-service volunteers are better trained and harder to replace. Recruiting them costs money every year.",
  pre=["TAI_na_manpower_question"], excl=["TAI_na_extended_conscription"], eff=["idea:TAI_professional_force"], filt=MAN, track="man")
F(na, "TAI_na_extended_conscription", "Retain Extended Conscription", "FRA_Reform_Military_Mass_Mobilization_Conscription", 70,
  "Long conscription keeps a deep pool of trained men at the cost of popularity and lost civilian work.",
  pre=["TAI_na_manpower_question"], eff=["idea:TAI_extended_conscription"], filt=MAN, track="man")
F(na, "TAI_na_reserve_audit", "Reserve Readiness Audit", "Generic_Intelligence_Gathering", 35,
  "Our reserve rolls list millions of names, but how many could actually fight? An honest audit is the first step.",
  pre=[("TAI_na_volunteer_reserve_split", "TAI_na_professional_force", "TAI_na_extended_conscription")], eff=["army_xp:10", "var:reform:5"], filt=MAN, track="man")
F(na, "TAI_na_reserve_reform", "Reserve Reform", "NKO_reserve", 105,
  "Regular refresher training and modern equipment turn a paper reserve into a real one.",
  pre=["TAI_na_reserve_audit"], eff=["rmidea:TAI_uneven_reserves", "money:-2"], filt=MAN, track="man")
F(na, "TAI_na_nco_initiative", "NCO and Junior Leader Initiative", "Generic_Soldier_Aiming", 70,
  "Sergeants and lieutenants trusted to act on their own judgment make a force far harder to paralyse.",
  pre=[("TAI_na_volunteer_reserve_split", "TAI_na_professional_force", "TAI_na_extended_conscription")], eff=["raw:add_timed_idea = { idea = TAI_junior_leader_initiative days = 1825 }"], filt=ARMY, track="man")
F(na, "TAI_na_territorial_defense", "Territorial Defense Brigades", "Generic_Volunteer_Corps", 105,
  "Local brigades of reservists can defend their own towns and free regular units to counterattack.",
  pre=["TAI_na_reserve_reform"], eff=["army_xp:20", "ws:0.03"], filt=MAN, track="man")

F(na, "TAI_na_us_links", "Secure U.S. Defense Links", "align_to_america", 70,
  "The Taiwan Relations Act lets Washington sell us defensive arms. It does not oblige the United States to fight for us.",
  pre=["TAI_na_rebuild_shield"], eff=["chi:ussupport:3", "var:usconf:3"], ai=5, track="proc")
F(na, "TAI_na_2001_package", "The 2001 Arms Package", "american_arms_focus", 35,
  "Washington has offered Kidd-class destroyers, P-3 patrol aircraft and diesel submarines it does not build itself. An offer is not a delivery.",
  pre=["TAI_na_us_links"], avail=["date>2001.4.1"], eff=["chi:tension:5", "pp:25"], track="proc")
F(na, "TAI_na_special_budget", "Special Defense Budget", "generic_banks", 70,
  "Major purchases need a special budget, and the opposition can delay, trim or block it.",
  pre=["TAI_na_2001_package"], avail=["ly"], eff=["money:-5", "var:usconf:5"], filt=["FOCUS_FILTER_MILITARY_LAWS", "FOCUS_FILTER_EXPENDITURE"], track="proc")
F(na, "TAI_na_kidd_destroyers", "Accept the Kidd-Class Destroyers", "TAI_navy_forces", 105,
  "Four large destroyers bring area air defense to sea, along with crews to train and maintenance bills to pay.",
  pre=["TAI_na_special_budget"], eff=["tech:CAT_destroyers:0.5:2", "navy_xp:20", "money:-3"], filt=NAVY, track="proc")
F(na, "TAI_na_maritime_patrol", "Maritime Patrol Aircraft", "Generic_Transport_Aircraft", 105,
  "Long-range patrol aircraft can track submarines through the Strait and its approaches.",
  pre=["TAI_na_special_budget"], eff=["tech:CAT_heavy_aircraft:0.5:1", "air_xp:15"], filt=AIR, track="proc")
F(na, "TAI_na_submarine_question", "The Submarine Question", "Generic_Submarine1", 70,
  "The United States no longer builds diesel submarines, and European yards fear Beijing. We may have to build our own.",
  pre=["TAI_na_special_budget"], eff=["tech:CAT_submarines:0.5:1"], filt=NAVY, track="proc")
F(na, "TAI_na_indigenous_submarine", "Indigenous Submarine Program", "Generic_Submarine2", 140,
  "A domestic submarine programme will take many years and teach our shipyards skills no one will sell us.",
  pre=["TAI_na_submarine_question", "TAI_na_csist"], avail=["date>2010.1.1"], eff=["tech:CAT_submarines:1:2", "build:one_random_dockyard"], filt=NAVY, track="proc")
F(na, "TAI_na_interoperability", "Interoperability Without Alliance", "alliance_JAP_USA", 70,
  "Shared training standards and logistics with American forces improve readiness without any treaty commitment.",
  pre=["TAI_na_us_links"], eff=["var:reform:5", "army_xp:10", "air_xp:10"], track="proc")
F(na, "TAI_na_absorption", "Solve the Absorption Problem", "Generic_Support_Equipment", 105,
  "New equipment is useless without trained crews, spare parts and maintenance crews. We will fund the pipeline before the next purchase.",
  pre=["TAI_na_interoperability"], eff=["rmidea:TAI_limited_absorption", "var:reform:10"], track="proc")
F(na, "TAI_na_fighter_fleet", "Sustain the Fighter Fleet", "Jet_Fighters", 70,
  "Our F-16s, Mirage 2000-5s and Ching-kuo fighters need upgrades and spares to stay ahead of the PLA Air Force.",
  pre=["TAI_na_absorption"], eff=["tech:CAT_aircraft:0.5:2", "air_xp:20"], filt=AIR, track="proc")
F(na, "TAI_na_idf_upgrade", "Upgrade the Indigenous Fighter", "TAI_air_forces", 105,
  "An improved Ching-kuo with better avionics and weapons keeps our domestic aerospace industry alive.",
  pre=["TAI_na_fighter_fleet", "TAI_na_csist"], eff=["tech:CAT_light_aircraft:0.75:2", "build:one_random_arms_factory"], filt=AIR, track="proc")
F(na, "TAI_na_csist", "Empower the Chungshan Institute", "BLR_Hi_Tech_Park", 70,
  "The Chungshan Institute of Science and Technology designs our missiles, radars and electronics. More funding means fewer dependencies.",
  pre=["TAI_na_rebuild_shield"], eff=["tech:CAT_missiles:0.5:2", "money:-2"], filt=["FOCUS_FILTER_RESEARCH"], track="proc")
F(na, "TAI_na_gray_zone", "Contest the Gray Zone", "JAP_taiwan_naval", 70,
  "Fighters and patrol ships that meet every incursion show that our airspace and waters are watched, even when no shot is fired.",
  pre=["TAI_na_rebuild_shield"], eff=["navy_xp:10", "air_xp:10", "var:ptn:-3"], track="proc")
F(na, "TAI_na_service_rivalry", "End the Service Rivalry", "Generic_Command_Power", 70,
  "A joint budget process stops the army, navy and air force from fighting each other for every dollar.",
  pre=["TAI_na_joint_command", "TAI_na_special_budget"], eff=["var:reform:10", "pp:50"], track="proc")

# ---------------------------------------------------------------- Branch 4
ss = branch("ss", "The Silicon Island", 0, ["FOCUS_FILTER_INDUSTRY"])
RES = ["FOCUS_FILTER_RESEARCH", "FOCUS_FILTER_INDUSTRY"]
TRD = ["FOCUS_FILTER_TRADE"]
ECO = ["FOCUS_FILTER_ECONOMY"]
F(ss, "TAI_ss_root", "The Silicon Island", "BLR_Hi_Tech_Park", 70,
  "TSMC and its rivals already lead the world in contract chipmaking. The question is whether that strength can protect the island as well as enrich it.",
  eff=["tech:CAT_microchips:0.5:1", "pp:25"], filt=RES, ai=5, track="chips")
F(ss, "TAI_ss_deepen_hsinchu", "Deepen Hsinchu Science Park", "BLR_Hi_Tech_Park", 70,
  "More land, power and water for the science park keeps fabs and suppliers clustered together.",
  pre=["TAI_ss_root"], eff=["build:one_random_industrial_complex", "tech:CAT_microchips:0.5:1"], filt=RES, track="chips")
F(ss, "TAI_ss_southern_park", "Expand the Southern Science Park", "Generic_Major_City", 70,
  "The Tainan science park spreads high-technology jobs to the south.",
  pre=["TAI_ss_deepen_hsinchu"], eff=["build:one_random_industrial_complex", "stab:0.02"], filt=RES, track="chips")
F(ss, "TAI_ss_central_park", "Found the Central Taiwan Science Park", "Generic_Major_City", 105,
  "A third science park near Taichung gives the industry room to grow.",
  pre=["TAI_ss_southern_park"], avail=["date>2003.1.1"], eff=["build:one_random_industrial_complex", "build:one_random_industrial_complex"], filt=RES, track="chips")
F(ss, "TAI_ss_twelve_inch", "The 12-Inch Transition", "ASML_world", 105,
  "300-millimetre wafers cut the cost of every chip but require years of new tools and yield work.",
  pre=["TAI_ss_deepen_hsinchu"], eff=["tech:CAT_microchips:0.75:2", "var:chips:5"], filt=RES, track="chips")
F(ss, "TAI_ss_advanced_process", "Advanced Process R&D", "ASML_world", 105,
  "Staying a node ahead of rivals keeps the world's chip designers coming to us.",
  pre=["TAI_ss_twelve_inch"], eff=["tech:CAT_microchips:1:2", "var:chips:5"], filt=RES, track="chips")
F(ss, "TAI_ss_fabless", "Strengthen Fabless Partnerships", "ExpandTrade", 70,
  "American and European design firms rely on our foundries. Long-term contracts make their success ours.",
  pre=["TAI_ss_deepen_hsinchu"], eff=["chi:ussupport:2", "raw:add_opinion_modifier = { target = USA modifier = large_commercial_relations }"], filt=TRD, track="chips")
F(ss, "TAI_ss_itri", "Reinvest in ITRI", "Generic_Command_Power", 70,
  "The Industrial Technology Research Institute spun off TSMC and UMC. New funding can seed the next industries.",
  pre=["TAI_ss_root"], eff=["tech:CAT_information_technology:0.5:2", "tech:CAT_robotics:0.5:1"], filt=RES, track="chips")
F(ss, "TAI_ss_crown_jewels", "Protect the Crown Jewels", "Generic_Espionage02", 70,
  "Our most advanced process knowledge stays at home. Partners may invest, license older technology and train engineers, but the core remains Taiwanese.",
  pre=["TAI_ss_advanced_process"], eff=["var:chips:5", "pp:25"], track="chips")
F(ss, "TAI_ss_supply_chain", "Protect Critical Supply Chains", "maritime_trade", 70,
  "Our fabs depend on Japanese chemicals, Dutch lithography and American tools. Mapping those dependencies is the first step to protecting them.",
  pre=["TAI_ss_advanced_process"], eff=["var:chips:10"], track="chips")
F(ss, "TAI_ss_materials_inventory", "Strategic Materials Inventory", "Generic_Support_Equipment", 70,
  "Stockpiles of wafers, gases and specialty chemicals let the fabs keep running if deliveries stop.",
  pre=["TAI_ss_supply_chain"], eff=["var:chips:10", "money:-2"], filt=["FOCUS_FILTER_INDUSTRY", "FOCUS_FILTER_EXPENDITURE"], track="chips")
F(ss, "TAI_ss_us_compact", "U.S.-Taiwan Semiconductor Compact", "align_to_america", 140,
  "This alternate-history compact ties American capital and customers to our fabs while the leading-edge know-how stays here.",
  pre=["TAI_ss_supply_chain", "TAI_pl_washington"], eff=["chi:ussupport:5", "var:usconf:5", "var:chips:5", "money:5"], filt=TRD, track="chips")
F(ss, "TAI_ss_court_berlin", "Court Berlin", "German_Diplomacy", 70,
  "German precision engineering, specialty materials and optics suppliers are vital links in our supply chain. This alternate-history push deepens those ties.",
  pre=["TAI_ss_supply_chain"], eff=["var:chips:5", "raw:if = { limit = { country_exists = GER } add_opinion_modifier = { target = GER modifier = large_commercial_relations } }"], filt=TRD, track="chips")
F(ss, "TAI_ss_dutch_litho", "Dutch Lithography Partnership", "ASML_world", 70,
  "Lithography machines are made by very few firms. Service agreements and spare parts keep our most valuable tools running.",
  pre=["TAI_ss_court_berlin"], eff=["var:chips:10", "raw:if = { limit = { country_exists = HOL } add_opinion_modifier = { target = HOL modifier = large_commercial_relations } }"], filt=TRD, track="chips")
F(ss, "TAI_ss_japan_materials", "Japanese Materials Alliance", "align_to_japan", 70,
  "Japanese firms supply many of the wafers, photoresists and chemicals our fabs consume.",
  pre=["TAI_ss_supply_chain", "TAI_pl_tokyo"], eff=["var:chips:10"], filt=TRD, track="chips")
F(ss, "TAI_ss_silicon_shield", "The Silicon Shield", "american_shield", 140,
  "The world economy now depends on our foundries, giving many governments a stake in our stability. That interest is not a guarantee: a blockade can still cut the supplies our fabs need.",
  pre=["TAI_ss_us_compact", ("TAI_ss_dutch_litho", "TAI_ss_japan_materials")], eff=["idea:TAI_silicon_shield", "chi:ussupport:5"], ai=5, track="chips")

F(ss, "TAI_ss_trading_economy", "The Island Trading Economy", "maritime_trade", 70,
  "Almost everything we eat, burn and build passes through our ports. Trade is our lifeblood and our weak point.",
  pre=["TAI_ss_root"], eff=["pp:25", "stab:0.02"], filt=ECO, track="eco")
F(ss, "TAI_ss_bad_loans", "Clear the Bad Loans", "generic_banks", 70,
  "Non-performing loans weigh on our banks after years of easy credit. Writing them off now restores confidence.",
  pre=["TAI_ss_trading_economy"], avail=["date>2001.6.1"], eff=["money:-3", "raw:add_timed_idea = { idea = TAI_financial_reform days = 1095 }"], filt=ECO, track="eco")
F(ss, "TAI_ss_bank_consolidation", "Consolidate the Banks", "generic_banks", 70,
  "Too many small banks compete for the same customers. Mergers create institutions able to weather a crisis.",
  pre=["TAI_ss_bad_loans"], avail=["date>2004.1.1"], eff=["stab:0.02", "pp:25"], filt=ECO, track="eco")
F(ss, "TAI_ss_challenge_2008", "Challenge 2008", "economic_prosperity2", 105,
  "A six-year national development plan sets targets for research, digital government and infrastructure.",
  pre=["TAI_ss_trading_economy"], avail=["date>2002.1.1"], eff=["tech:CAT_construction:0.5:2", "pp:25"], filt=ECO, track="eco")
F(ss, "TAI_ss_ten_projects", "Ten New Major Construction Projects", "Generic_Public_Works", 105,
  "Ports, rail and research parks built now will serve the economy for decades.",
  pre=["TAI_ss_challenge_2008"], eff=["build:one_random_industrial_complex", "build:one_random_infrastructure"], filt=["FOCUS_FILTER_INFRASTRUCTURE", "FOCUS_FILTER_EXPENDITURE"], track="eco")
F(ss, "TAI_ss_high_speed_rail", "Finish the High-Speed Rail", "Generic_Railroads", 105,
  "A bullet train from Taipei to Kaohsiung ties the west coast into one economy. It cannot open before its tracks are finished.",
  pre=["TAI_ss_ten_projects"], avail=["date>2006.6.1"], eff=["build:one_random_infrastructure", "build:one_random_infrastructure", "stab:0.02"], filt=["FOCUS_FILTER_INFRASTRUCTURE", "FOCUS_FILTER_EXPENDITURE"], track="eco")
F(ss, "TAI_ss_e_taiwan", "e-Taiwan", "Generic_Digital_Agriculture", 70,
  "Broadband, digital government and online services make the state faster and the economy more productive.",
  pre=["TAI_ss_trading_economy"], eff=["tech:CAT_internet:0.5:2", "build:one_random_network_infrastructure"], filt=RES, track="eco")
F(ss, "TAI_ss_biotech", "Biotech Takeoff", "generic_hospital", 70,
  "Biotechnology diversifies our exports beyond electronics.",
  pre=["TAI_ss_e_taiwan"], eff=["tech:CAT_genetics:0.5:2"], filt=RES, track="eco")
F(ss, "TAI_ss_services", "Services and Tourism", "Tourism_is_our_oil", 70,
  "Finance, design and tourism earn income that does not pass through a single market.",
  pre=["TAI_ss_trading_economy"], eff=["var:dep:-3", "raw:add_timed_idea = { idea = TAI_service_economy days = 1095 }"], filt=ECO, track="eco")
F(ss, "TAI_ss_export_markets", "Diversify Export Markets", "Trade_with_the_east", 70,
  "New customers in Southeast Asia, Europe and the Americas reduce our exposure to any single buyer.",
  pre=["TAI_ss_services"], eff=["var:dep:-5", "raw:add_opinion_modifier = { target = VIE modifier = large_commercial_relations }"], filt=TRD, track="eco")
F(ss, "TAI_ss_fx_facility", "A Defined Reserve Facility", "generic_banks", 70,
  "Our central bank holds large foreign reserves, but they are not a government piggy bank. Clear rules decide when they may defend the currency or pay for emergency imports.",
  pre=["TAI_ss_bad_loans"], eff=["pp:25", "var:ptn:-3"], filt=ECO, track="eco")
F(ss, "TAI_ss_marine_insurance", "National Marine Insurance Pool", "maritime_trade", 70,
  "If private insurers flee during a crisis, a state-backed pool can keep cargo moving. It is a contingent liability, not free money.",
  pre=["TAI_ss_fx_facility"], eff=["var:ptn:-3", "stab:0.02"], filt=TRD, track="eco")

F(ss, "TAI_ss_energy_review", "Energy Security Review", "Efficient_Oil_Production_Focus_Icon_V2", 35,
  "We import nearly all of our energy. A review shows how long we could last if tankers stopped coming.",
  pre=["TAI_ss_root"], eff=["pp:25"], filt=["FOCUS_FILTER_RESOURCE"], track="energy")
F(ss, "TAI_ss_spr", "Strategic Petroleum Reserve", "Efficient_Oil_Production_Focus_Icon_V2", 105,
  "Larger oil stocks buy time in a blockade. Tanks must be built and then filled before they help.",
  pre=["TAI_ss_energy_review"], eff=["money:-3", "raw:add_timed_idea = { idea = TAI_strategic_fuel_reserve days = 3650 }"], filt=["FOCUS_FILTER_RESOURCE", "FOCUS_FILTER_EXPENDITURE"], track="energy")
F(ss, "TAI_ss_lng", "Expand the LNG Terminals", "Federal_Gas_Tax_Fund", 105,
  "More gas terminals diversify the fuels our power plants burn.",
  pre=["TAI_ss_energy_review"], eff=["build:one_random_infrastructure", "tech:CAT_fuel_refining:0.5:1"], filt=["FOCUS_FILTER_POWER_INFRASTRUCTURE"], track="energy")
F(ss, "TAI_ss_coal_stocks", "Coal Stockpiles for the Grid", "Generic_Train", 70,
  "Coal yards at the power stations keep the lights on through short interruptions.",
  pre=["TAI_ss_energy_review"], eff=["var:ptn:-2", "money:-1"], filt=["FOCUS_FILTER_POWER_INFRASTRUCTURE"], track="energy")
F(ss, "TAI_ss_renewables", "Renewable Energy Act", "Generic_Digital_Agriculture", 70,
  "Wind and solar power give us a small share of energy that no blockade can cut.",
  pre=["TAI_ss_lng"], avail=["date>2009.1.1"], eff=["tech:CAT_renewable_energy:0.75:2"], filt=["FOCUS_FILTER_RENEWABLE_ENERGY_INFRASTRUCTURE"], track="energy")
F(ss, "TAI_ss_food_reserve", "National Food Reserve", "agriculture2", 70,
  "Rice reserves and feed stocks protect against both bad harvests and blockade.",
  pre=["TAI_ss_energy_review"], eff=["money:-1", "var:ptn:-3"], filt=["FOCUS_FILTER_RESOURCE"], track="energy")
F(ss, "TAI_ss_wto_farmers", "Protect Farmers After the WTO", "agriculture", 70,
  "Joining the WTO opens our market to cheaper imports. Support for farmers keeps domestic food production alive.",
  pre=["TAI_ss_food_reserve", "TAI_pl_wto"], eff=["money:-1", "stab:0.03"], filt=["FOCUS_FILTER_RESOURCE"], track="energy")
F(ss, "TAI_ss_emergency_shipping", "Emergency Shipping Arrangements", "Generic_Maritime", 70,
  "Reserved charter contracts give us ships to call on when commercial carriers hesitate.",
  pre=["TAI_ss_marine_insurance"], eff=["var:ptn:-3"], filt=TRD, track="energy")
F(ss, "TAI_ss_endurance_target", "A National Endurance Target", "Focus_Rationing", 70,
  "Fuel, food and chip materials each get a stockpile target and a plan to reach it.",
  pre=["TAI_ss_spr", "TAI_ss_food_reserve", "TAI_ss_materials_inventory"], eff=["idea:TAI_strategic_reserves", "var:ptn:-5"], ai=3, track="energy")

# ---------------------------------------------------------------- Branch 5
as_ = branch("as", "Across the Strait", 0, ["FOCUS_FILTER_FOREIGN_POLICY"])
FP = ["FOCUS_FILTER_FOREIGN_POLICY"]
F(as_, "TAI_as_root", "Across the Strait", "Generic_Imperial_China_Diplomacy", 70,
  "Trade and investment across the Strait keep growing even while political relations freeze. We must manage both at once.",
  pre=["TAI_su_peaceful_transfer"], eff=["pp:25"], ai=5, track="econ")
F(as_, "TAI_as_go_slow", "No Haste, Be Patient", "Generic_Soldiers_Defense", 70,
  "Lee Teng-hui's policy limited large investments on the mainland to avoid dependence. Keeping it means slower growth and less exposure.",
  pre=["TAI_as_root"], excl=["TAI_as_active_opening"], eff=["idea:TAI_no_haste", "var:dep:-5"], filt=TRD, track="econ")
F(as_, "TAI_as_active_opening", "Active Opening, Effective Management", "ExpandTrade", 70,
  "Loosening investment limits lets our firms profit from the mainland's growth while the government watches the risks.",
  pre=["TAI_as_root"], eff=["idea:TAI_active_opening", "var:dep:8", "chi:trust:3"], filt=TRD, ai=3, track="econ")
F(as_, "TAI_as_mini_three_links", "The Mini Three Links", "Generic_Maritime", 35,
  "Direct ferries, trade and mail between Kinmen, Matsu and Fujian are a modest first step toward normal links.",
  pre=["TAI_as_root"], avail=["date>2001.1.1"], eff=["chi:trust:3", "var:dep:3", "chi:tension:-2"], filt=TRD, ai=3, track="econ")
F(as_, "TAI_as_taishang", "The Taishang Question", "Generic_Major_City", 70,
  "Hundreds of thousands of our businesspeople now live on the mainland. They bring home profits and also lobby for Beijing's preferences.",
  pre=[("TAI_as_go_slow", "TAI_as_active_opening")], eff=["var:dep:3", "pp:25"], filt=TRD, track="econ")
F(as_, "TAI_as_charter_flights", "Holiday Charter Flights", "Generic_Transport_Aircraft", 35,
  "Charter flights at Lunar New Year let families travel without changing planes in Hong Kong.",
  pre=["TAI_as_mini_three_links"], avail=["date>2003.1.1"], eff=["chi:trust:3", "var:dep:2"], track="econ")
F(as_, "TAI_as_investment_caps", "Sector Investment Caps", "generic_banks", 70,
  "Limiting how much of a firm's capital can go to the mainland caps the damage Beijing can do to any one company.",
  pre=["TAI_as_taishang"], eff=["var:dep:-5", "var:ptn:-3"], filt=TRD, track="econ")
F(as_, "TAI_as_exposure_monitor", "Monitor Mainland Exposure", "Generic_Intelligence_Gathering", 35,
  "Tracking where our trade, investment and supplies depend on the mainland warns us before pressure arrives.",
  pre=["TAI_as_investment_caps"], eff=["var:ptn:-3", "var:coord:3"], track="econ")
F(as_, "TAI_as_tighten_management", "Active Management, Effective Opening", "Generic_Policeman", 70,
  "Reversing the order of the slogan puts risk management ahead of opening.",
  pre=["TAI_as_exposure_monitor"], avail=["date>2006.1.1"], eff=["var:dep:-5", "chi:trust:-3"], filt=TRD, track="econ")
F(as_, "TAI_as_go_south", "Go South", "Trade_with_the_east", 70,
  "Investment in Southeast Asia spreads our factories across many countries instead of one.",
  pre=["TAI_as_root"], eff=["var:dep:-5", "raw:add_opinion_modifier = { target = VIE modifier = large_commercial_relations }", "raw:add_opinion_modifier = { target = PHI modifier = large_commercial_relations }"], filt=TRD, track="econ")
F(as_, "TAI_as_three_links", "The Full Three Links", "Generic_Maritime", 105,
  "Direct shipping, flights and mail would end decades of detours through Hong Kong. The economic gain is large, and so is the new dependence.",
  pre=["TAI_as_charter_flights"], avail=[("blue", "raw:date > 2008.6.1")], eff=["chi:trust:8", "var:dep:10", "raw:add_timed_idea = { idea = TAI_direct_links days = 1825 }"], filt=TRD, track="econ")
F(as_, "TAI_as_mainland_tourists", "Mainland Tourists", "Tourism_is_our_oil", 70,
  "Mainland tour groups bring money to hotels and shops, and Beijing can turn the flow off at will.",
  pre=["TAI_as_three_links"], eff=["var:dep:5", "chi:trust:3"], filt=TRD, track="econ")
F(as_, "TAI_as_economic_framework", "A Cross-Strait Economic Framework", "accept_treaty", 140,
  "A broad trade agreement would cut tariffs and open markets. Beijing would gain its strongest economic lever yet.",
  pre=["TAI_as_mainland_tourists"], avail=[("raw:date > 2009.1.1", "raw:AND = { TAI_kmt_in_power = yes date > 2006.1.1 }")], eff=["var:dep:12", "chi:trust:10", "raw:add_timed_idea = { idea = TAI_cross_strait_framework days = 3650 }"], filt=TRD, track="econ")

F(as_, "TAI_as_restore_1992_spirit", "Restore the Spirit of the 1992 Talks", "Generic_Secret_Meeting", 70,
  "In 1992 the two sides agreed to set sovereignty aside and solve practical problems. We can return to that method without endorsing any one-China formula.",
  pre=["TAI_as_root"], excl=["TAI_as_uphold_1992"], avail=["dpp"], eff=["chi:trust:5", "chi:tension:-3"], ai=3, track="pol")
F(as_, "TAI_as_uphold_1992", "Uphold the 1992 Consensus", "Generic_Imperial_China_Diplomacy", 70,
  "One China, respective interpretations: both sides affirm one China and each defines it differently. Beijing welcomes the formula; critics say it concedes too much.",
  pre=["TAI_as_root"], avail=["blue"], eff=["chi:trust:12", "chi:tension:-5", "var:identity:-3"], ai=3, track="pol")
F(as_, "TAI_as_sef_arats", "Revive the SEF-ARATS Channel", "Generic_Secret_Meeting", 70,
  "The semi-official Straits Exchange Foundation and its mainland counterpart can resume talks on practical issues.",
  pre=[("TAI_as_restore_1992_spirit", "TAI_as_uphold_1992")], avail=["raw:custom_trigger_tooltip = { tooltip = TAI_chi_trust_above_19_tt CHI = { check_variable = { CHI_TAI_trust > 19 } } }"], eff=["chi:trust:5", "chi:tension:-3"], track="pol")
F(as_, "TAI_as_crisis_channel", "A Cross-Strait Crisis Channel", "NKO_korea_peace", 70,
  "A standing line for incidents at sea and in the air lets both sides check facts before anyone escalates.",
  pre=["TAI_as_sef_arats"], eff=["chi:tension:-8"], track="pol")
F(as_, "TAI_as_stabilization", "The Strait Stabilization Initiative", "accept_treaty", 105,
  "This alternate-history initiative offers restraint for restraint: we avoid unilateral constitutional change while Beijing reduces military coercion.",
  pre=["TAI_as_crisis_channel"], eff=["chi:tension:-10", "chi:trust:5", "var:usconf:5"], ai=3, track="pol")
F(as_, "TAI_as_structured_restraint", "Structured Restraint", "Generic_Soldiers_Defense", 70,
  "If Beijing answers our restraint with pressure, our patience becomes evidence for friends abroad.",
  pre=["TAI_as_stabilization"], eff=["chi:ussupport:5", "var:usconf:5"], track="pol")
F(as_, "TAI_as_cbms", "Military Confidence-Building Measures", "NKO_korea_peace", 70,
  "Advance notice of exercises and rules for close encounters lower the risk of accidental war.",
  pre=["TAI_as_structured_restraint"], eff=["chi:tension:-8", "var:milconf:-3"], track="pol")
F(as_, "TAI_as_one_country_each_side", "One Country on Each Side", "TAI_civilwar_legacy", 35,
  "Declaring that there is one country on each side of the Strait thrills our base and alarms Beijing and Washington.",
  pre=["TAI_as_root"], avail=["dpp", "date>2002.8.1"], eff=["var:identity:5", "chi:tension:10", "var:usconf:-5"], ai=0, track="pol")
F(as_, "TAI_as_journey_of_peace", "The Journey of Peace", "Generic_Secret_Meeting", 70,
  "Our party chairman can travel to Beijing to meet its leaders, the first such meeting since the civil war.",
  pre=["TAI_as_uphold_1992"], avail=["date>2005.1.1"], eff=["chi:trust:10", "chi:tension:-5"], track="pol")
F(as_, "TAI_as_red_lines", "Know Beijing's Red Lines", "Generic_Intelligence_Gathering", 35,
  "Understanding what Beijing considers intolerable lets us choose our risks deliberately.",
  pre=["TAI_as_root"], eff=["pp:25", "var:coord:3"], track="pol")
F(as_, "TAI_as_anti_secession", "Answer the Anti-Secession Law", "Generic_Tear_Paper", 70,
  "Beijing's new law authorises non-peaceful means under conditions it alone defines. Our answer can rally citizens or reassure friends.",
  pre=["TAI_as_red_lines"], avail=["date>2005.3.14"], eff=["var:identity:3", "chi:ussupport:3", "stab:0.02"], track="pol")
F(as_, "TAI_as_assent", "The Assent of the People of Taiwan", "MNT_democracy", 70,
  "No settlement across the Strait can take effect without the consent of the people who would live under it.",
  pre=["TAI_as_red_lines"], eff=["var:ptn:-10", "stab:0.02"], ai=3, track="pol")
F(as_, "TAI_as_peace_accord", "A Cross-Strait Peace Accord?", "NKO_korea_peace", 140,
  "A formal peace accord could end the state of hostility. Any agreement would need a referendum, and voters may reject it.",
  pre=["TAI_as_journey_of_peace", "TAI_as_assent"], avail=["blue"], eff=["chi:trust:10", "chi:tension:-10", "var:dep:3"], ai=0, track="pol")
F(as_, "TAI_as_status_quo_dividend", "The Status Quo Dividend", "economic_prosperity2", 70,
  "Calm in the Strait lowers insurance costs and attracts investors.",
  pre=["TAI_as_crisis_channel"], eff=["raw:add_timed_idea = { idea = TAI_status_quo_dividend days = 1095 }"], filt=ECO, track="pol")
F(as_, "TAI_as_managed_ambiguity", "Managed Ambiguity", "Generic_East_Vs_West", 105,
  "We decline to settle the final question while acting decisively to strengthen the state we already govern.",
  pre=["TAI_as_assent", ("TAI_as_structured_restraint", "TAI_as_peace_accord")], eff=["idea:TAI_managed_ambiguity", "var:usconf:5"], ai=5, track="pol")
F(as_, "TAI_as_offshore_line", "Kinmen and Matsu Safety Line", "Generic_Maritime", 35,
  "A direct line between local authorities on the offshore islands and Fujian handles fishing disputes and smuggling.",
  pre=["TAI_as_mini_three_links"], eff=["chi:tension:-3", "stab:0.01"], track="pol")

# ---------------------------------------------------------------- Branch 6
pl = branch("pl", "The Pacific Lifeline", 0, ["FOCUS_FILTER_FOREIGN_POLICY"])
F(pl, "TAI_pl_root", "The Pacific Lifeline", "Afghan_on_the_world_stage", 70,
  "Our friendships abroad are infrastructure for a crisis. They must be built before they are needed.",
  eff=["pp:25"], ai=5, track="us")
F(pl, "TAI_pl_washington", "Consult Washington", "align_to_america", 35,
  "Regular consultation helps Washington see our decisions coming.",
  pre=["TAI_pl_root"], eff=["var:usconf:5"], ai=5, track="us")
F(pl, "TAI_pl_no_surprises", "No Surprises", "USA_diplomatic_corps", 70,
  "We brief Washington before major announcements. It costs some freedom of action and earns trust.",
  pre=["TAI_pl_washington"], eff=["var:usconf:10"], ai=3, track="us")
F(pl, "TAI_pl_capitol_hill", "Friends on Capitol Hill", "american_government", 70,
  "Members of Congress from both parties support Taiwan's democracy. Their resolutions and visits keep us on Washington's agenda.",
  pre=["TAI_pl_washington"], eff=["chi:ussupport:4"], track="us")
F(pl, "TAI_pl_transit", "Transit Diplomacy", "Generic_Transport_Aircraft", 35,
  "Presidential stopovers in American cities are not state visits, but they make headlines in both Taipei and Beijing.",
  pre=["TAI_pl_capitol_hill"], eff=["var:identity:3", "chi:ussupport:2", "chi:tension:3"], track="us")
F(pl, "TAI_pl_tifa", "Revive the TIFA Talks", "ExpandTrade", 70,
  "The Trade and Investment Framework Agreement provides a forum to settle trade disputes with the United States.",
  pre=["TAI_pl_washington"], eff=["raw:add_opinion_modifier = { target = USA modifier = large_commercial_relations }", "var:usconf:3"], filt=TRD, track="us")
F(pl, "TAI_pl_us_crisis_comms", "Crisis Communication with Washington", "Socialist_Radio", 70,
  "Agreed channels for a crisis mean we can reach the right American officials in hours, not days.",
  pre=["TAI_pl_no_surprises"], eff=["chi:ussupport:3", "var:usconf:5"], track="us")
F(pl, "TAI_pl_us_credit", "Pre-Arranged U.S. Credit Facility", "generic_banks", 70,
  "A standby facility can be requested in an emergency. Approval, terms and delivery would still be Washington's decision.",
  pre=["TAI_pl_us_crisis_comms"], eff=["var:ptn:-5"], filt=ECO, track="us")

F(pl, "TAI_pl_tokyo", "Consult Tokyo: The Geographic Anchor", "align_to_japan", 35,
  "Japan's southern islands lie close to ours, and its sea lanes run past us.",
  pre=["TAI_pl_root"], eff=["raw:if = { limit = { country_exists = JAP } add_opinion_modifier = { target = JAP modifier = political_outreach } }"], ai=3, track="jap")
F(pl, "TAI_pl_japan_visa", "Visa-Free Japan", "JAP_flag_big", 35,
  "Visa-free travel brings tourists and business in both directions.",
  pre=["TAI_pl_tokyo"], avail=["date>2005.1.1"], eff=["stab:0.02", "raw:if = { limit = { country_exists = JAP } add_opinion_modifier = { target = JAP modifier = large_commercial_relations } }"], track="jap")
F(pl, "TAI_pl_japan_coast_guard", "Coast Guard Talks with Japan", "JAP_taiwan_naval", 70,
  "Our coast guards share waters, fishing disputes and search-and-rescue duties.",
  pre=["TAI_pl_tokyo", "TAI_na_gray_zone"], eff=["navy_xp:10", "var:ptn:-2"], track="jap")
F(pl, "TAI_pl_japan_dialogue", "Unofficial Security Dialogue with Japan", "alliance_JAP_USA", 70,
  "Retired officials and scholars can discuss regional security without a formal alliance.",
  pre=["TAI_pl_japan_coast_guard"], eff=["chi:ussupport:2", "chi:tension:2"], track="jap")
F(pl, "TAI_pl_japan_credit", "Japanese Credit Guarantees", "generic_banks", 70,
  "Pre-arranged trade credit guarantees with Japanese lenders could keep imports flowing in a crisis.",
  pre=["TAI_pl_japan_dialogue"], eff=["var:ptn:-5"], filt=ECO, track="jap")

F(pl, "TAI_pl_europe", "Europe's Commercial Stake", "align_to_europe", 70,
  "European firms buy our chips and sell us machines. Their governments care about stability in the Strait.",
  pre=["TAI_pl_root"], eff=["pp:25"], track="eu")
F(pl, "TAI_pl_eu_trade", "EU Trade and Investment Talks", "European_Society", 70,
  "Investment and trade talks with the European Union diversify our partners.",
  pre=["TAI_pl_europe"], eff=["var:dep:-3", "raw:if = { limit = { country_exists = GER } add_opinion_modifier = { target = GER modifier = large_commercial_relations } }"], filt=TRD, track="eu")
F(pl, "TAI_pl_european_parliament", "Friends in the European Parliament", "EU_constitution", 35,
  "Resolutions supporting our participation in international bodies raise our profile in Europe.",
  pre=["TAI_pl_europe"], eff=["stab:0.01", "pp:25"], track="eu")
F(pl, "TAI_pl_eu_supply", "European Industrial Supply Network", "Dutch_Maritime_Industry", 70,
  "Long-term supply contracts with European manufacturers diversify where our machines and parts come from.",
  pre=["TAI_pl_eu_trade"], eff=["var:chips:5", "var:ptn:-3"], filt=TRD, track="eu")

F(pl, "TAI_pl_india", "Look West to New Delhi", "align_to_india", 70,
  "India's engineers and growing market make it a natural partner. This alternate-history diplomacy goes beyond our historical ties.",
  pre=["TAI_pl_root"], eff=["raw:if = { limit = { country_exists = RAJ } add_opinion_modifier = { target = RAJ modifier = political_outreach } }"], track="ind")
F(pl, "TAI_pl_india_tier1", "Tier I: Engineers and Electronics", "Indian_flag", 70,
  "Electronics assembly, packaging and engineering exchanges help both sides without risking our core technology.",
  pre=["TAI_pl_india"], eff=["tech:CAT_information_technology:0.5:1", "raw:if = { limit = { country_exists = RAJ } add_opinion_modifier = { target = RAJ modifier = large_commercial_relations } }"], filt=TRD, track="ind")
F(pl, "TAI_pl_india_tier2", "Tier II: Controlled Licensing", "BLR_Hi_Tech_Park", 105,
  "Older process technology may be licensed under safeguards. Our crown jewels stay at home.",
  pre=["TAI_pl_india_tier1", "TAI_ss_crown_jewels"], eff=["money:3", "var:dep:-3"], filt=TRD, track="ind")
F(pl, "TAI_pl_india_market", "Indian Market Diversification", "Trade_with_the_east", 70,
  "Indian customers reduce our reliance on any single export market.",
  pre=["TAI_pl_india_tier1"], eff=["var:dep:-5"], filt=TRD, track="ind")
F(pl, "TAI_pl_india_partnership", "Strategic Partnership with New Delhi", "align_to_india", 105,
  "A broader partnership covers trade, technology and quiet security consultation.",
  pre=["TAI_pl_india_tier2"], avail=["date>2008.1.1"], eff=["var:ptn:-3", "chi:tension:3"], track="ind")

F(pl, "TAI_pl_keep_allies", "Keep the Diplomatic Allies", "Generic_Outside_Aid", 70,
  "Aid keeps the few states that recognise us on our side, at a steady cost and with scandal risks.",
  pre=["TAI_pl_root"], excl=["TAI_pl_end_checkbook"], eff=["money:-3", "pp:25"], filt=["FOCUS_FILTER_FOREIGN_POLICY", "FOCUS_FILTER_EXPENDITURE"], track="allies")
F(pl, "TAI_pl_end_checkbook", "End Checkbook Diplomacy", "Generic_Tear_Paper", 70,
  "Paying for recognition rewards the highest bidder. We will spend on real partnerships instead.",
  pre=["TAI_pl_root"], eff=["money:2", "stab:0.02"], track="allies")
F(pl, "TAI_pl_transparent_aid", "Transparent Aid Diplomacy", "Generic_Red_Cross", 70,
  "Published aid budgets and humanitarian projects earn respect rather than suspicion.",
  pre=[("TAI_pl_keep_allies", "TAI_pl_end_checkbook")], eff=["corr:-1", "pp:25"], track="allies")

F(pl, "TAI_pl_wto", "Complete WTO Accession", "accept_treaty", 70,
  "We applied as the Separate Customs Territory of Taiwan, Penghu, Kinmen and Matsu. Membership opens markets and exposes protected sectors.",
  pre=["TAI_pl_root"], avail=["date>2001.11.1"], eff=["raw:add_timed_idea = { idea = TAI_wto_membership days = 3650 }", "stab:-0.02"], filt=TRD, ai=5, track="space")
F(pl, "TAI_pl_wha", "Bid for the World Health Assembly", "generic_hospital", 70,
  "Observer status at the World Health Assembly would give our doctors direct access to global health information.",
  pre=["TAI_pl_wto"], eff=["pp:25", "chi:tension:2"], track="space")
F(pl, "TAI_pl_sars", "Lessons of SARS", "London_Health_Academy", 35,
  "SARS showed that exclusion from global health networks has real costs. Better surveillance and isolation wards will serve us in the next epidemic.",
  pre=["TAI_pl_wha"], avail=["date>2003.6.1"], eff=["raw:add_timed_idea = { idea = TAI_epidemic_preparedness days = 3650 }"], track="space")
F(pl, "TAI_pl_technical_seats", "Technical Seats at the Table", "Afghan_on_the_world_stage", 70,
  "Aviation, standards and scientific bodies matter in daily life even when sovereignty questions block full membership.",
  pre=["TAI_pl_sars"], eff=["pp:25", "stab:0.01"], track="space")
F(pl, "TAI_pl_apec", "Make APEC Count", "maritime_trade", 35,
  "APEC is one of the few regional forums where we sit as a full member economy.",
  pre=["TAI_pl_wto"], eff=["raw:add_opinion_modifier = { target = SIN modifier = large_commercial_relations }"], filt=TRD, track="space")
F(pl, "TAI_pl_offices", "Expand Representative Offices", "USA_diplomatic_corps", 70,
  "Economic and cultural offices abroad do the work of embassies without the name.",
  pre=["TAI_pl_root"], eff=["pp:25", "raw:add_timed_idea = { idea = TAI_representative_offices days = 1825 }"], track="space")
F(pl, "TAI_pl_document_coercion", "Prepare to Document Coercion", "Generic_Intelligence_Gathering", 70,
  "Careful records of every incident, published promptly, make it harder for Beijing to deny pressure.",
  pre=["TAI_pl_offices", "TAI_pl_us_crisis_comms"], eff=["chi:ussupport:3", "var:ptn:-3"], track="space")
F(pl, "TAI_pl_lifeline_holds", "The Lifeline Holds", "Afghan_on_the_world_stage", 140,
  "Partners in Washington, Tokyo and Europe now have arrangements ready for a crisis. None of them is an automatic promise to fight.",
  pre=["TAI_pl_us_credit", "TAI_pl_japan_credit", "TAI_pl_eu_supply"], eff=["idea:TAI_pacific_lifeline", "chi:ussupport:5"], ai=5, track="space")

# ---------------------------------------------------------------- Branch 7
bt = branch("bt", "Operation Blue Tiger", 0, ["FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_WAR_SUPPORT"])
F(bt, "TAI_bt_root", "Operation Blue Tiger", "american_shield", 70,
  "Defense, economy, diplomacy and democracy must now be planned as one national survival strategy. Our aim is to make Taiwan impossible to coerce at an acceptable price.",
  avail=["raw:TAI_blue_tiger_roots_ready = yes"], eff=["var:coord:10", "pp:50"], ai=5, track="strat")
F(bt, "TAI_bt_accommodation", "Strategy: Accommodation", "Generic_Imperial_China_Diplomacy", 35,
  "We keep extensive economic ties and minimise confrontation. Prosperity grows, and so does Beijing's leverage.",
  pre=["TAI_bt_root"], excl=["TAI_bt_blue_tiger", "TAI_bt_island_fortress"], eff=["idea:TAI_strategy_accommodation", "chi:tension:-5"], track="strat")
F(bt, "TAI_bt_blue_tiger", "Strategy: Blue Tiger", "american_shield", 35,
  "We keep selective ties while diversifying, strengthening partnerships and preparing for pressure.",
  pre=["TAI_bt_root"], excl=["TAI_bt_island_fortress"], eff=["idea:TAI_strategy_blue_tiger"], ai=5, track="strat")
F(bt, "TAI_bt_island_fortress", "Strategy: Island Fortress", "SIN_total_defense", 35,
  "We cut dependence quickly and stockpile heavily, accepting slower growth and a more alarmed Beijing.",
  pre=["TAI_bt_root"], eff=["idea:TAI_strategy_island_fortress", "chi:tension:5", "var:dep:-5"], track="strat")
F(bt, "TAI_bt_nsc", "The National Security Council Coordinates", "Generic_Command_Power", 70,
  "Defense, economic, energy and foreign ministries plan crises together under one council.",
  pre=[("TAI_bt_accommodation", "TAI_bt_blue_tiger", "TAI_bt_island_fortress")], eff=["var:coord:10"], ai=3, track="strat")
F(bt, "TAI_bt_adaptation_office", "Economic Adaptation Office", "economic_prosperity2", 70,
  "A standing office helps firms find new suppliers and markets before a crisis forces them to.",
  pre=["TAI_bt_nsc"], eff=["var:dep:-3", "var:ptn:-3"], filt=ECO, track="strat")
F(bt, "TAI_bt_count_the_days", "Count the Days", "Focus_Rationing", 35,
  "Every ministry reports how long its essential supplies would last under blockade.",
  pre=["TAI_bt_nsc"], eff=["var:coord:5", "pp:25"], track="strat")

F(bt, "TAI_bt_succession", "Unambiguous Succession", "Focus_Parliament_Constitution", 35,
  "Clear rules on who governs if leaders are killed or cut off deny an attacker a quick decapitation.",
  pre=["TAI_bt_nsc"], eff=["stab:0.03"], track="cog")
F(bt, "TAI_bt_alternate_seats", "Alternate Seats of Government", "Generic_Major_City", 70,
  "Ministries keep secure backup sites and records outside Taipei.",
  pre=["TAI_bt_succession"], eff=["money:-1", "stab:0.02"], track="cog")
F(bt, "TAI_bt_local_emergency", "Local Emergency Administration", "Generic_Policeman", 70,
  "County governments can run shelters, water and food distribution if the center is disrupted.",
  pre=["TAI_bt_alternate_seats", "TAI_df_local_government"], eff=["var:coord:5", "ws:0.02"], track="cog")
F(bt, "TAI_bt_emergency_limits", "Emergency Powers With Limits", "MEX_Defend_the_constitution", 70,
  "Emergency powers will be defined in law, time-limited and subject to legislative and judicial review.",
  pre=["TAI_bt_succession"], eff=["stab:0.03", "var:ptn:-3"], track="cog")

F(bt, "TAI_bt_wan_an", "Revive the Wan An Drills", "air_defense", 70,
  "The annual Wan An air-raid drills teach citizens where to shelter and how to help.",
  pre=["TAI_bt_nsc"], eff=["ws:0.03", "raw:add_timed_idea = { idea = TAI_civil_defense_drills days = 1825 }"], filt=["FOCUS_FILTER_WAR_SUPPORT"], track="cont")
F(bt, "TAI_bt_medical_surge", "Emergency Medical Surge", "generic_hospital", 70,
  "Hospitals plan for mass casualties and epidemics with stockpiles and reserve staff.",
  pre=["TAI_bt_wan_an"], eff=["money:-1", "stab:0.02"], track="cont")
F(bt, "TAI_bt_restore_grid", "Restore the Grid", "Generic_Public_Works", 70,
  "Repair crews and spare transformers can bring power back quickly after an attack.",
  pre=["TAI_bt_wan_an"], eff=["build:one_random_infrastructure", "var:ptn:-2"], track="cont")
F(bt, "TAI_bt_redundant_comms", "Redundant Communications", "Socialist_Radio", 70,
  "Backup radio, satellite and fiber links keep government and public informed when networks fail.",
  pre=["TAI_bt_restore_grid"], eff=["tech:CAT_encryption:0.5:1", "var:coord:3"], track="cont")
F(bt, "TAI_bt_financial_continuity", "Financial Continuity Plan", "generic_banks", 70,
  "Payment systems and banks rehearse working through outages and panics.",
  pre=["TAI_bt_nsc", "TAI_ss_fx_facility"], eff=["var:ptn:-3", "stab:0.02"], filt=ECO, track="cont")
F(bt, "TAI_bt_rationing", "Rationing Without Panic", "Focus_Rationing", 70,
  "Fair, published rationing plans prevent hoarding if supplies run short.",
  pre=["TAI_bt_count_the_days"], eff=["var:ptn:-3"], track="cont")
F(bt, "TAI_bt_ports_open", "Keep the Ports Open", "Generic_Maritime", 70,
  "Manual procedures let ports keep unloading ships if computer systems are attacked.",
  pre=["TAI_bt_redundant_comms"], eff=["var:ptn:-3"], filt=TRD, track="cont")
F(bt, "TAI_bt_airlift", "High-Value Airlift", "Generic_Transport_Aircraft", 70,
  "Aircraft can carry small, valuable cargo such as chip materials and medicine, but never bulk fuel or food.",
  pre=["TAI_bt_ports_open"], eff=["var:chips:5"], track="cont")
F(bt, "TAI_bt_emergency_procurement", "Emergency Procurement Networks", "Generic_Outside_Aid", 70,
  "Pre-approved suppliers in third countries speed emergency purchases, with audits to catch fraud.",
  pre=["TAI_bt_airlift", "TAI_bt_adaptation_office"], eff=["var:ptn:-3", "corr:-1"], track="cont")
F(bt, "TAI_bt_publish_reserves", "Publish the Reserve Levels", "Socialist_Radio", 35,
  "Regular, verified reports of fuel and food stocks take the air out of shortage rumours.",
  pre=["TAI_bt_count_the_days"], eff=["var:ptn:-5"], track="cont")
F(bt, "TAI_bt_document_incidents", "Document Every Incident", "Generic_Intelligence_Gathering", 35,
  "Every gray-zone incident is recorded and published with evidence.",
  pre=["TAI_bt_nsc", "TAI_pl_document_coercion"], eff=["chi:ussupport:3"], track="cont")
F(bt, "TAI_bt_semiconductor_continuity", "Semiconductor Continuity Pact", "ASML_world", 70,
  "The government and chipmakers agree how fabs, power and water will be protected in a crisis.",
  pre=["TAI_bt_nsc", "TAI_ss_silicon_shield"], eff=["var:chips:10"], track="cont")
F(bt, "TAI_bt_counterweapon", "The Counterweapon", "Generic_Espionage04", 70,
  "We prepare the option of restricting strategic chip exports to a coercer. Using it would cost us sales and push customers to build elsewhere.",
  pre=["TAI_bt_semiconductor_continuity"], eff=["pp:25", "chi:tension:3"], ai=0, track="cont")
F(bt, "TAI_bt_emergency_doctrine", "Blue Tiger Emergency Doctrine", "Russian_Emergency_Powers", 105,
  "Emergency procedures for gray-zone pressure, blockade, missile attack and invasion are written, rehearsed and bounded by law.",
  pre=["TAI_bt_emergency_limits", "TAI_bt_rationing", "TAI_bt_emergency_procurement"], eff=["idea:TAI_emergency_doctrine", "var:ptn:-5"], ai=3, track="cont")
F(bt, "TAI_bt_island_endures", "The Island Can Endure", "Generic_Liberty_Calling", 70,
  "Citizens know the plans, the reserves are real and the government is trusted. Hardship need not become surrender.",
  pre=["TAI_bt_emergency_doctrine"], eff=["var:ptn:-10", "ws:0.03"], track="cont")
F(bt, "TAI_bt_capstone", "Impossible to Coerce at an Acceptable Price", "american_shield", 140,
  "Taiwan does not have to become impossible to hurt. It has to become impossible to coerce at an acceptable price.",
  pre=["TAI_bt_island_endures", "TAI_pl_lifeline_holds", ("TAI_na_fortress_taiwan", "TAI_na_hybrid")], eff=["idea:TAI_impossible_to_coerce", "var:ptn:-10"], ai=5, track="cont")
