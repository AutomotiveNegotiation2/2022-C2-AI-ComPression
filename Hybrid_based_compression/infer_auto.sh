#!/bin/bash
can_dir="2022_09_06_12_30_06.txt"
hd1=" "
hd2=" "
nls=" "
bss=" "
epoch=" "
bash clean.sh
python3 data_gen_line.py --file_name $can_dir
python3 run.py --file_name train_dataset/train.csv
bash mk_weight.sh train_dataset/train.csv train $hd1 $hd2 $nls $bss 8 $epoch
