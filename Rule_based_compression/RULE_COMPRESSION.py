import zipfile
from collections import deque
from multiprocessing import Process, Manager
import numpy as np
import os
import argparse
import shutil



def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_data_path', type=str, default="RAW_DATA_STORAGE_DIR",
                        help='raw_data_path')
    parser.add_argument('--compressed_data_path', type=str, default="COMPRESSED_DATA_STORAGE_DIR",
                        help='compressed_data_path')
    
    return parser

def GPS_compression(arg_list):
    Vehicle_ID = arg_list[1]["Vehicle_ID"]
    compressed_path = os.path.join(arg_list[0].compressed_data_path) #,"GPS_DIR")
    raw_data_path = os.path.join(arg_list[0].raw_data_path,"GPS_DIR")
    file_list = os.listdir(raw_data_path)
    file_list.sort()
    gps_data_q = deque(file_list)
    gps_list = []
    
    

def CAM_compression(arg_list):
    Vehicle_ID = arg_list[1]["Vehicle_ID"]
    compressed_path = os.path.join(arg_list[0].compressed_data_path)#,"CAM_DIR")

    raw_data_path = os.path.join(arg_list[0].raw_data_path,"CAM_DIR")
    dir_list = os.listdir(raw_data_path)
    dir_list.sort()
    cam_data_q = deque(dir_list)
    

def DEM_compression(arg_list):
    Vehicle_ID = arg_list[1]["Vehicle_ID"]
    compressed_path = os.path.join(arg_list[0].compressed_data_path) # ,"DEM_DIR")
    raw_data_path = os.path.join(arg_list[0].raw_data_path,"DEM_DIR")

    file_list = os.listdir(raw_data_path)
    file_list.sort()
    dem_data_q = deque(file_list)
    dem_list = []



def CANFD_compression(arg_list):
    Vehicle_ID = arg_list[1]["Vehicle_ID"]
    compressed_path = os.path.join(arg_list[0].compressed_data_path) # ,"CANFD_DIR")
    raw_data_path = os.path.join(arg_list[0].raw_data_path, "CAN_DIR")
    file_list = os.listdir(raw_data_path)
    sorted(file_list)
    canfd_data_q = deque(file_list)
    canfd_list = []


def RuleCompression():

    parser = get_argument_parser()
    args = parser.parse_args()

    manager = Manager()
    arg_list = manager.list()
    arg_list.append(args)
    arg_list.append({"Vehicle_ID" : "123eab0804567_"})


    p1_GPS = Process(target=GPS_compression,args=(arg_list))
    p1_GPS.start()
    
    p2_CAM = Process(target=CAM_compression,args=(arg_list))
    p2_CAM.start()

    p3_DEM = Process(target=DEM_compression,args=(arg_list))
    p3_DEM.start()

    p4_CANFD = Process(target=CANFD_compression,args=(arg_list))
    p4_CANFD.start()


    p1_GPS.join()
    print("___GPS_PROCESS END___")
    p2_CAM.join()
    print("___CAM_PROCESS END___")
    p3_DEM.join()
    print("___DEM_PROCESS END___")
    p4_CANFD.join()
    print("___CANFD_PROCESS END___")
    
    return 1
if __name__ == "__main__":
    RuleCompression()