from multiprocessing import Process, Manager , Lock
import cv2
import time
import numpy as np
import os
import argparse
import datetime
import CAMERA_read
import GPS_read
import CANFD_read


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin_data_path', type=str, default='/root/data/(20240605)compression_AI-main/compression_model/data/dummy_data',
                        help='raw_data_path')
    parser.add_argument('--raw_data_path', type=str, default='/root/data/(20240605)compression_AI-main/compression_model/data/RAW_DATA_STORAGE_DIR',
                        help='raw_data_path')
    return parser

def GPS_PARSER(arg_list,):
    GPS_read.read_data(arg_list)
    
def CAM_PARSER(arg_list, ):
    CAMERA_read.read_data(arg_list)

def CANFD_PARSER(arg_list,):
    CANFD_read.read_data(arg_list,)


def DAT_GEN(arg_list,):
        # 0 : canfd
        # 3 : GPS
        # 4 : Camera

    save_dir = ""
    dir_CAM = "CAM_DIR"
    dir_CANFD = "CAN_DIR"
    dir_GPS = "GPS_DIR"
    can_data = ""
    gps_data = ""
    cam_data = ""
    
    while True:
        # data_dir = os.path.join(save_dir,glob_t)
        # os.mkdir(data_dir)     
        gps_data = arg_list[3]
        cam_data = arg_list[4]
        can_data = arg_list[0]
        glob_t = datetime.datetime.now()
        if len(gps_data) * len(can_data) * len(gps_data) * len(cam_data):
            print("dem : ",len(arg_list[2]) , " can : ",len(arg_list[0]) ," g : ", len(arg_list[3]) ," cam : ", len(arg_list[4]))

            start_t = time.time()
            print(glob_t)
            # CANFD
            with open( os.path.join(save_dir,dir_CANFD, glob_t +".txt"),"a"  ) as cf:
                cf.write(  can_data )
            # gps
            with open( os.path.join(save_dir,dir_GPS, glob_t +".txt"),"w"  ) as gf:
                gf.write(gps_data)
                
            cam_ffff = os.path.join(save_dir,dir_CAM, glob_t )
            
            if not os.path.isdir(cam_ffff):
                os.mkdir( cam_ffff )
            for cname,cdata in zip(["cam1","cam2","cam3","cam4"],cam_data ):
                cv2.imwrite(os.path.join(cam_ffff,cname+".jpg"), cdata)
            end_t = time.time()
            time.sleep(1 - (end_t - start_t))


if __name__ == "__main__":

    parser = get_argument_parser()
    args = parser.parse_args()
    lock = Lock()
    manager = Manager()
    data_list = manager.list()
    for _ in range(7):
        # 0 : CANFD
        # 3 : GPS
        # 4 : Camera
        data_list.append([])
    
    p1_GPS = Process(target=GPS_PARSER,args=(data_list,))
    p1_GPS.start()

    p2_CAM = Process(target=CAM_PARSER,args=(data_list,))
    p2_CAM.start()

    p4_CANFD = Process(target=CANFD_PARSER,args=(data_list,))
    p4_CANFD.start()

    p7_DAT_GEN = Process(target=DAT_GEN, args=(data_list,))
    p7_DAT_GEN.start()    
    
    p1_GPS.join()
    p2_CAM.join()
    p4_CANFD.join()
    p7_DAT_GEN.join()