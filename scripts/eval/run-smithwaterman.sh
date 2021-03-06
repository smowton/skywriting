#!/bin/bash
NUM_ROWS=10
NUM_COLS=10
MASTER="http://localhost:9000"
SWROOT="../.."

if [[ $1 == '--trace' ]]; then
    SCRIPT_FILE=$SWROOT/src/sw/smithwaterman-traced.sw
else
    SCRIPT_FILE=$SWROOT/src/sw/smithwaterman.sw
fi

export PYTHONPATH=$SWROOT/src/python/
export INPUT1=`$SWROOT/scripts/sw-load -m $MASTER horizontal_string_random | tr -d '\n'`
export INPUT2=`$SWROOT/scripts/sw-load -m $MASTER vertical_string_random | tr -d '\n'`
export NUM_ROWS
export NUM_COLS

for i in 1; do
#for c in 10000 5000 2500 2000; do
    echo "Running repetition $i: "
    export FOO=`date +%s`
    $SWROOT/scripts/sw-job -m $MASTER -e $SCRIPT_FILE 2>&1
done
