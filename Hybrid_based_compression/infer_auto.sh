#!/bin/bash
can_dir=""
hd1=" "
hd2=" "
nls=" "
bss=" "
epoch=" "
bash clean.sh
python3 data_gen_line.py --file_name $can_dir
python3 run.py --file_name train_dataset/train.csv
bash mk_weight.sh train_dataset/train.csv train $hd1 $hd2 $nls $bss 8 $epoch
