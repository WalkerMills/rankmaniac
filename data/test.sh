#! /usr/bin/env bash

DATA="$1"
INPUT="./input.txt"
OUTPUT="./output.txt"

python2 pagerank_map.py < $DATA | sort | python2 pagerank_collect.py | python2 process_map.py | sort | python2 process_reduce.py > $OUTPUT && cp $OUTPUT $INPUT

COUNT=1

while  [[ `grep -c 'FinalRank' $OUTPUT` -eq 0 ]]; do
    python2 pagerank_map.py < $INPUT | sort | python2 pagerank_collect.py | python2 process_map.py | sort | python2 process_reduce.py > $OUTPUT && cp $OUTPUT $INPUT    
    COUNT=$((COUNT + 1))
done

rm $INPUT
echo "Converged in $COUNT iterations"
cat $OUTPUT