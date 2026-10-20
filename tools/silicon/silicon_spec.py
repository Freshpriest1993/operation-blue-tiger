# Operation Blue Tiger: Silicon Island rework (focus side).
#
# Science-park focuses build real Millennium Dawn microchip plants (microchip_plant) instead of generic
# civilian factories. Each build goes through a scripted effect in
# common/scripted_effects/99_OBT_silicon_scripted_effects.txt: if Taiwan lacks the workers, has an
# energy deficit, or is under a full blockade, the plant is deferred and a decision lets the player
# build it later. AUG's civilian factories in the Central Taiwan Science Park focus are unchanged.
#
# Loaded at the end of spec.py:  import silicon_spec; silicon_spec.integrate(sys.modules[__name__])
# Set OBT_SKIP_SILICON=1 to build without these changes.

def integrate(S):
    A = {f["id"]: f for b in S.BRANCHES for f in b["focuses"]}

    def swap(fid, old, new):
        eff = A[fid]["eff"]
        eff[eff.index(old)] = new

    swap("TAI_ss_deepen_hsinchu", "build:one_random_industrial_complex", "raw:TAI_science_park_fab_hsinchu = yes")
    swap("TAI_ss_southern_park", "build:one_random_industrial_complex", "raw:TAI_science_park_fab_tainan = yes")
    A["TAI_ss_central_park"]["eff"].append("raw:TAI_science_park_fab_taichung = yes")
    A["TAI_ss_advanced_process"]["eff"].append("raw:TAI_science_park_fab_any = yes")

    for fid in ("TAI_ss_deepen_hsinchu", "TAI_ss_southern_park", "TAI_ss_central_park", "TAI_ss_advanced_process"):
        mods = A[fid].setdefault("aimods", [])
        guard = "factor = 0 has_active_mission = bankruptcy_incoming_collapse"
        if guard not in mods:
            mods.append(guard)
        staff = "factor = 0 can_staff_an_microchip_plant = no"  # Millennium Dawn's AI convention for focuses that build plants
        if staff not in mods:
            mods.insert(0, staff)

    # Energy Security Review: two fossil-fuel power stations (Taichung and Kaohsiung), deferred if
    # Taiwan lacks the workers. See TAI_energy_review_power_stations.
    A["TAI_ss_energy_review"]["eff"].insert(0, "raw:TAI_energy_review_power_stations = yes")
    mods = A["TAI_ss_energy_review"].setdefault("aimods", [])
    for m in ("factor = 3 has_an_energy_deficit = yes", "factor = 0 has_active_mission = bankruptcy_incoming_collapse"):
        if m not in mods:
            mods.append(m)
