# Operation Blue Tiger: political prerequisite fixes (OBT-authored focuses only).
#
# N1 (Nuclear Policy): the Green Party can still reach its capstone after Maanshan Nuclear Power Plant
# Expansion (AUG's focus, unchanged and still mutually exclusive with A Nuclear-Free Homeland).
# Wind and Sun and Let the People Decide on Nuclear Power each accept either A Nuclear-Free Homeland or
# Environmental Impact Assessment. Both are OBT focuses (party branches, milestone 6).
#
# Loaded at the end of spec.py:  import politics_spec; politics_spec.integrate(sys.modules[__name__])
# Set OBT_SKIP_POLITICS=1 to build without these changes, or OBT_SKIP_N1=1 for this fix alone.
import os

N1 = {
    "TAI_su_gpt_wind_and_sun": ("TAI_su_gpt_nuclear_free", "TAI_su_gpt_impact_assessment"),
    "TAI_su_gpt_nuclear_referendum": ("TAI_su_gpt_nuclear_free", "TAI_su_gpt_impact_assessment"),
}


def integrate(S):
    A = {f["id"]: f for b in S.BRANCHES for f in b["focuses"]}
    if os.environ.get("OBT_SKIP_N1") != "1":
        for fid, either in N1.items():
            assert A[fid]["pre"] == [either[0]], (fid, A[fid]["pre"])
            A[fid]["pre"] = [either]
