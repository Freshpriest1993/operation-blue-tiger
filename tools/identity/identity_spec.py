# Operation Blue Tiger: National Identity, the Status Quo route to a DPP capstone.
#
# Reaffirm the Status Quo -> The Republic of China (Taiwan) -> Pragmatic Sovereignty.
# Pragmatic Sovereignty is a separate DPP capstone. It shares A New Generation and The Economic
# Advisory Conference with Taiwan's Own Path, which is unchanged. The two capstones stay exclusive
# through the existing exclusion between Reaffirm the Status Quo and Name Rectification.
#
# Pragmatic Sovereignty keeps DPP programme II and adds its own spirit (TAI_dpp_pragmatic_sovereignty,
# written to common/ideas/05_taiwan.txt by apply_identity_text.py).
# Project National Glory exclusion: roc_spec adds the capstone to DEMO_CAPS when it is in the tree, and
# nav_spec adds it to DEMOCRATIC_CAPSTONES.
#
# Names, descriptions, icons and rewards are provisional, pending review of names and effects.
#
# Loaded from spec.py before the RoC-development integration:
#   import identity_spec; identity_spec.integrate(sys.modules[__name__])
# Set OBT_SKIP_IDENTITY=1 to build without these two focuses.

ROC_TAIWAN = "TAI_su_dpp_roc_taiwan"
CAPSTONE = "TAI_su_dpp_pragmatic_sovereignty"
SPIRIT = "TAI_dpp_pragmatic_sovereignty"


def integrate(S):
    dpp = next(b for b in S.BRANCHES if b["key"] == "dpp")
    ids = {f["id"] for f in dpp["focuses"]}
    for need in ("TAI_su_dpp_status_quo", "TAI_su_dpp_new_generation", "TAI_su_dpp_advisory_conference", "TAI_su_dpp_own_path"):
        assert need in ids, need
    assert ROC_TAIWAN not in ids and CAPSTONE not in ids

    S.PF(dpp, ROC_TAIWAN, "The Republic of China (Taiwan)", "Focus_Parliament_Constitution",
         "Taiwan is already a sovereign state, and under the constitution its name is the Republic of China. "
         "No formal change is needed, and our partners abroad can count on us not to alter the status quo.",
         ["TAI_su_dpp_status_quo"], ["dpp", "date>2006.1.1"],
         ["var:identity:5", "var:usconf:5", "chi:tension:-3", "stab:0.03"], ai=3)
    S.PF(dpp, CAPSTONE, "Pragmatic Sovereignty", "MNT_democracy",
         "Our sovereignty rests on our democracy, not on a declaration. We will defend it through strong "
         "institutions and trusted partners abroad, without needless escalation.",
         [ROC_TAIWAN, "TAI_su_dpp_new_generation", "TAI_su_dpp_advisory_conference"], ["dpp"],
         [f"idea:{SPIRIT}"], ai=5)
    cap = dpp["focuses"][-1]
    # The AI on the Project National Glory path should not close that path with a democratic capstone.
    cap["aimods"] = ["factor = 0 has_global_flag = TAI_PNG_FOCUS_PATH"]
    # Layout: on the capstone row, three columns left of Reaffirm the Status Quo, where no line from its
    # three prerequisites runs through another focus.
    cap["lay_anchor"] = ("TAI_su_dpp_status_quo", -3, 3)
