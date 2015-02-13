#! /usr/bin/env bash

DATA="$1"
INPUT="./input.txt"
OUTPUT="./output.txt"

./pagerank_map < $DATA | sort | ./pagerank_reduce | ./process_map | sort | python2 process_reduce.py > $OUTPUT && cp $OUTPUT $INPUT

COUNT=1

while  [[ `grep -c 'FinalRank' $OUTPUT` -eq 0 ]]; do
    ./pagerank_map < $INPUT | sort | ./pagerank_reduce | ./process_map | sort | python2 process_reduce.py > $OUTPUT && cp $OUTPUT $INPUT    
    COUNT=$((COUNT + 1))
done

rm $INPUT
echo "Converged in $COUNT iterations"
cat $OUTPUT