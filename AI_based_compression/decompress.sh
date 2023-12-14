#!/bin/bash
FILE=$1
BASE=$FILE
JOINT=_
EXT=bstrap
OUTPUT=$2
MODEL_PATH=$3

echo Using $MODEL_PATH for decoding
echo "DECOMRESSING START!"
StartTime=$(date +%s.%N)
python3 decompress_adaptive.py --file_name $BASE --output $OUTPUT --model_weights_path $MODEL_PATH
EndTime=$(date +%s.%N)
diff=$( echo "scale=1;($EndTime - $StartTime)*1000" | bc -l) 
echo "DECOMPRESSING TIME : $diff msec"
echo "DECOMP DONE"