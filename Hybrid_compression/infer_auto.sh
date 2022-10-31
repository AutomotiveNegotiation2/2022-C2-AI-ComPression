#!/bin/bash
hd1=" "
hd2=" "
nls=" "
bss=" "
epoch=" "
./clean.sh
python3 data_gen_line.py
python3 run.py --file_name train_dataset/train.csv
./mk_weight.sh train_dataset/train.csv train $hd1 $hd2 $nls $bss 8 $epoch
