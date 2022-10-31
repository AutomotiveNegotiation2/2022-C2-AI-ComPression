import numpy as np
import os

new_data = []
line_num = 0                                                
one_sec_list = []
file_name = ""
unit_lines = 24
crit_timestamp = 0.0
config_num = 4
# timmstamp 2400 개가 1000 ms
# 최소 주기는 10 ms 로 24개 정도 나옴
f = open(file_name,"r")
line_datas = f.readlines()[4:]
f.close()
data_len = len(line_datas)
total_lines = (data_len // unit_lines) * unit_lines
crit_timestamp = float(line_datas[0].split()[3])
train_data_len = int(total_lines * 0.8)
eval_data_len = int(total_lines * 0.2)
data_l = [train_data_len, train_data_len+eval_data_len]
# Data 80% -> train 20% -> eval

print("total_len" , len(line_datas))
f = open(file_name,"r")
while True:
    l = f.readline()
    if line_num < config_num:
        print("continue_data_lines : ",line_num)
        line_num +=1
        continue
    if not l:
        print("break_line : ",line_num)
        break
    if line_num == data_l[0]:
        fn = open(f"./train_dataset/train.csv","w")
        for j in new_data:
            fn.write(j)
        fn.close()
        new_data = []
    elif line_num == data_l[1]:
        fe = open(f"./eval_dataset/eval.csv","w")
        for k in new_data:
            fe.write(k)
        fe.close()
        new_data = []
    l_list = l.split(" ")
    can_id = l_list[1]
    data_len = l_list[2]
    Timestamp = l_list[3]
    f_Timestamp = float(Timestamp)
    if line_num % 2404  == 0:
        crit_timestamp = f_Timestamp
    
    new_Timestamp =  round(f_Timestamp - crit_timestamp,2)
    new_Timestamp = str(new_Timestamp)
    if len(new_Timestamp) != 5:
        new_Timestamp = "0" *(5 - len(new_Timestamp)) + new_Timestamp
    data_field = l_list[4:]
    can_id = can_id[:-1]
    lsd = ' '.join([str(new_Timestamp), can_id,data_len] +data_field)
    new_data.append(lsd)
    line_num += 1
print("end_len : ",line_num)
f.close()

data_unit = [1.0]
data_lines = [ i*10*240 for i in data_unit]
# if you want another unit, you can add data_unit


for n, d in enumerate(data_lines):
    os.mkdir(f"./eval_dataset/{data_unit[n]}")
    f = open("./eval_dataset/eval.csv")
    new_data = []
    line_num = 0
    one_sec_list = []
    while True: 
        l = f.readline()
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
        fn = open(f"eval_dataset/{data_unit[n]}/{i}.csv","w")
        for j in one_sec_list[i]:
            fn.write(j)
        fn.close()
print("done")