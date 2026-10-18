#!/bin/bash
# Rebuild the RoC integration bundle. Run from the tools directory that holds spec.py.
# usage: rebuild.sh <repo_mirror> <work_dir>
set -e
REPO=$1; W=$2; T=$(cd "$(dirname "$0")/.." && pwd)
rm -rf "$W"; mkdir -p "$W"
python3 -B "$T/gen.py" "$REPO" "$W/gen" > "$W/gen_report.txt"
grep -E "^(WARN|ERROR)" "$W/gen_report.txt" && exit 1 || true
python3 -B "$T/events_gen.py" "$REPO" "$W/ev" > /dev/null 2>&1 || true
python3 -B "$T/m5/rec_gen.py" "$W/rec" > /dev/null
python3 -B "$T/m9/build9.py" "$W/b9" > /dev/null
python3 -B "$T/m10/mob10.py" "$W/m10" > /dev/null
python3 -B "$T/roc/build_roc.py" "$W/roc" "$W/gen/focus_loc.yml" > /dev/null
python3 -B "$T/roc/make_docs.py" "$W/docs" > /dev/null
B=$W/bundle; mkdir -p $B/new $B/replace/common/national_focus $B/replace/events $B/replace/common/decisions $B/replace/common/scripted_triggers
cp -r $W/roc/* $B/new/
cp $W/gen/05_taiwan.txt $B/replace/common/national_focus/
cp $W/ev/Taiwan_Blue_Tiger.txt $W/rec/Taiwan_Reclamation.txt $B/replace/events/
cp $W/b9/common/decisions/OBT_defense_decisions.txt $B/replace/common/decisions/
cp $W/m10/common/scripted_triggers/99_OBT_reserve_scripted_triggers.txt $B/replace/common/scripted_triggers/
(cd $B/replace && find . -type f | sed 's|^\./||' | sort | while read f; do echo "$(sha256sum "$REPO/$f" | cut -d' ' -f1)  $f"; done) > $B/base_hashes.txt
echo "bundle ready: $(find $B -type f | wc -l) files"
