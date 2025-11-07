#!/bin/bash

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
# - env TARGET: path to target work dir
# - env OUT: path to directory where artifacts are stored
# - env SHARED: path to directory shared with host (to store results)
# - env PROGRAM: name of program to run (should be found in $OUT)
# - env ARGS: extra arguments to pass to the program
# - env FUZZARGS: extra arguments to pass to the fuzzer
##

ARGS=${ARGS:-"@@"}
mkdir -p "$SHARED/findings"

flag_cmplog=(-m none -c "$OUT/cmplog/$PROGRAM")

export AFL_SKIP_CPUFREQ=1
export AFL_NO_AFFINITY=1
export AFL_NO_UI=1
export AFL_MAP_SIZE=256000
export AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1
export AFL_IGNORE_UNKNOWN_ENVS=1
export AFL_FAST_CAL=1
export AFL_NO_WARN_INSTABILITY=1
export AFL_BENIGN_PROGRAM_ABNORMAL_EXIT=1

for i in $OUT/*.dict $OUT/*.dic $OUT/afl/*.dict $OUT/afl/*.dic; do
    test -f "$i" && DICT="$DICT -x $i"
done

cp $FUZZER/repo/openai_key.txt .
cp $FUZZER/repo/program_to_format.json .
cp $FUZZER/repo/model_setting.json .

python $FUZZER/repo/program_gen.py --output "$SHARED/findings" --program $PROGRAM

"$FUZZER/repo/afl-fuzz" -d -t 1000+ -m none -i "$SHARED/findings/default/gen_seeds/" -k "$FUZZER/repo" -o "$SHARED/findings" \
    "${flag_cmplog[@]}" \
    $DICT $FUZZARGS -- "$OUT/afl/$PROGRAM" $ARGS 2>&1
