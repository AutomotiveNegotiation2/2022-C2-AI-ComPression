import numpy as np
import os
import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser();
    parser.add_argument('--file_name', type=str, default='can.csv',
                        help='The name of the input file')
    return parser

parser = get_argument_parser()
args = parser.parse_args()

file_name = args.file_name

unit_lines = 24
# CAN 데이터 기준 timmstamp 2400 개가 1000 ms
# 최소 주기는 10 ms 로 24개 정도 나옴
# CANFD  데이터 기준 1800개 정도 1000ms
f = open(file_name,"r")
line_datas = f.readlines()
f.close()
data_len = len(line_datas)
total_lines = (data_len // unit_lines) * unit_lines
new_data = []
line_num = 0                                                
one_sec_list = []
print("MAKE_SPLIT_DATASET")
print("CAN_PERIOD_SPLIT : 0.1 ms, 0.5 ms, 1.0 ms, 2.0 ms")
os.mkdir("split_dataset")
f = open(file_name,"r")
while True:
    l = f.readline()
    if "Timestamp" in l:
        print("continue_data_lines : ",line_num)
        continue
    if not l:
        print("break_line : ",line_num)
        break
    if line_num == total_lines -1:
        fn = open(f"./split_dataset/data.csv","w")
        for j in new_data:
            fn.write(j)
        fn.close()
        break
    data_len = l.split(",")[2]

    if data_len != "8":
        data_field = l.split(",")[-2]
        f_add_zero =  8 - int(data_len)
        data_field = data_field + " 00"*f_add_zero
    else:
        data_field = l.split(",")[-2]
    f_col = l.split(",")[0]
    if len(f_col) <= 17:    
       
       add_zero = 17 - len(f_col)
       f_col = '0'*add_zero + f_col
    else :
        f_col = f_col[:17]
    id_s = l.split(",")[1][5:]
    list_l = l.split(",")[2:-2]
    list_l = [f_col] + [id_s] + list_l + [data_field]
    lsd = ','.join(list_l)
    new_data.append(lsd+"\n")
    line_num += 1
f.close()


data_unit = [0.1, 0.5, 1.0, 2.0]
data_lines = [ i*10*240 for i in data_unit]

for n, d in enumerate(data_lines):
    os.mkdir(f"./split_dataset/{data_unit[n]}")
    f = open("./split_dataset/data.csv")
    new_data = []
    line_num = 0
    one_sec_list = []
    while True: 
        l = f.readline()
        if "Timestamp" in l:
            continue
        if not l:
            break
        if line_num == d:
            one_sec_list.append(new_data)
            new_data = []
            line_num =0
        new_data.append(l)
        line_num += 1
    f.close()

    for i in range(len(one_sec_list)):
        fn = open(f"split_dataset/{data_unit[n]}/{i}.csv","w")
        for j in one_sec_list[i]:
            fn.write(j)
        fn.close()
        if i > 500:
            break
print("DONE")