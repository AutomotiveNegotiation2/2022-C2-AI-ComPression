import time
from multiprocessing import Process, Manager
import numpy as np
from ai_based_compression import *
from rule_base_compression import *
from viewer import *
from utils import *
from models_torch import *
import time
import json
import argparse

def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hybrid_param_path', type=str, default='hybrid_param.json',
                        help='hybrid_param_path')
    return parser


if __name__ == "__main__":
    # Hybrid parameter 
    # need hybrid_param.json file in the google drive
    # hybrid file have Rule based compression param info and AI based compression info
    parser = get_argument_parser()
    args = parser.parse_args()
    if os.path.isfile(args.hybrid_param_path):

        with open(args.hybrid_param_path) as f:
            hparam = json.load(f)
        data_dir = hparam["data_dir"]
        speed_can_id = hparam ["speed_can_id"]
        speed_can_datafield_area =hparam ["speed_can_datafield_area"]
    else:
        print(f"CHECK_PARAMETER_PATH : {args.hybrid_param_path}")

    if os.path.isfile(hparam["RULE_param"]) and os.path.isfile(hparam["AI_param"]):
        print("COMPRESSION_PARAMETER_FILE_LOAD")
    else:
        if not os.path.isfile(hparam["RULE_param"]):
            print("CHECK_RULE_COMPRESSION_PARAMETER_FILE")
        elif not os.path.isfile(hparam["AI_param"]):
            print("CHECK_AI_COMPRESSION_PARAMETER_FILE")
  
    lines = read_data(data_dir)
    manager = Manager()
    AI_list = manager.list()
    AL_list = manager.list()
    AI_res_list = manager.list()
    AL_res_list = manager.list()
    now_spd_list = manager.list()
    delay_list = manager.list()
    comp_id,comp_num = 0, 1
    spd_list = []
    collect_line, state = "", ""
    past_timestamp,interval_time,change_delay_time,before_timestamp = 0.0, 0.0, 0.0 , 0.0
    # multiprocess start
    # main process parsing the can DB
    # classified parsed can data using speed data
    # if speed over 0 dynamic state -> AI compression process
    # else static state -> Rule compression process
    # compression result -> viewer process
    print("process AI start")
    p1 = Process(target=AI_compression,args=(AI_list,AI_res_list,))
    p1.start()

    print("process alg start")
    p2 = Process(target=alg_compression,args=(AL_list,AL_res_list,))
    p2.start()

    print("viewer start")
    p3 = Process(target=view,args=(AI_res_list,AL_res_list,now_spd_list,delay_list,))
    p3.start()

    for n,l in enumerate(lines,start = 1):
        canid, data_len, timestamp, datafield = split_can_msg(l)

        if n == 1:
            past_timestamp = float(timestamp)
            

        interval_time = round(float(timestamp) - past_timestamp,2)
        delay_time = round(float(timestamp) - before_timestamp,2) 
        delta_timestamp = str(interval_time)

        if len(delta_timestamp) != 5:
            delta_timestamp = "0"*(5 - len(delta_timestamp) ) + delta_timestamp
        can_msg = [ delta_timestamp, canid, data_len] + datafield
        str_can_msg = " ".join(can_msg) + " \n"
        collect_line += str_can_msg
        
        if int(canid,16) == speed_can_id:
            # Need CAN speed id and datafield area info
            spd = int(datafield[speed_can_datafield_area],16)
            spd_list.append(spd)

        if state == "dynamic" and spd == 0.0:
            change_delay_time += delay_time
        if state == "static" and spd > 0.0:        
            change_delay_time += delay_time

        before_timestamp = float(timestamp)

        if n % 2400 == 0:
            # can data parsing 2400 packets
            # it is about 1 second

            past_timestamp = float(timestamp)
            time.sleep(2)
            # not real time

            # classifed based on speed
            if state == "static" and np.mean(spd_list) == 0.0:
                change_delay_time =0.0
            if state == "dynamic" and np.mean(spd_list) > 0.0:
                change_delay_time = 0.0
            
            delay_list.append(change_delay_time )
            state = preprocessing(spd_list)
            AI_list.append([collect_line, comp_id,state])
            AL_list.append([collect_line, comp_id,state])
            now_spd_list.append(spd_list)

            spd_list = []
            comp_id +=1
            collect_line = ""
            comp_num += 1
        
    AI_list.append(["break"])
    AL_list.append(["break"])
    AI_res_list.append(["break"])
    AL_res_list.append(["break"])
    p1.join()
    p2.join()
    p3.join()

