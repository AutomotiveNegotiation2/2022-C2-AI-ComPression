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
    compressed_path = os.path.join(arg_list[0].compressed_data_path) 
    raw_data_path = os.path.join(arg_list[0].raw_data_path,"GPS_DIR")
    file_list = os.listdir(raw_data_path)
    file_list.sort()
    gps_data_q = deque(file_list)
    gps_list = []
    
    
    while True:
        if len(gps_data_q) == 0 :
            file_list = os.listdir(raw_data_path)
            file_list.sort()
            print(f"gps_space_savings : {np.mean(gps_list)}")
            break

        if len(gps_data_q) != 0:
            gps_f = gps_data_q.popleft()
            file_name = gps_f.split(".")[0]
            compressed_res = os.path.join( compressed_path, f"GPS_{Vehicle_ID}" + file_name +".zip")
            my_zip = zipfile.ZipFile(compressed_res  ,mode= 'w', compresslevel = 9)  
            my_zip.write( os.path.join(raw_data_path,gps_f), compress_type=zipfile.ZIP_DEFLATED )       
            my_zip.close()
            com_size = os.path.getsize(compressed_res )
            ori_size = os.path.getsize(  os.path.join(raw_data_path,gps_f) )
            if (ori_size == 0) or (com_size == 0) :
                continue
            space_savings = (1 - ( com_size / ori_size)) * 100
            gps_list.append(space_savings)
            print(f"GPS_SPACE_SAVINGS : {space_savings:4.2f}_{compressed_res}")
            
            os.remove(os.path.join(raw_data_path,gps_f))


def CAM_compression(arg_list):
    Vehicle_ID = arg_list[1]["Vehicle_ID"]
    compressed_path = os.path.join(arg_list[0].compressed_data_path)

    raw_data_path = os.path.join(arg_list[0].raw_data_path,"CAM_DIR")
    dir_list = os.listdir(raw_data_path)
    dir_list.sort()
    cam_data_q = deque(dir_list)
    
    while True:
        if len(cam_data_q) == 0 :
            
            dir_list = os.listdir(raw_data_path)
            dir_list.sort()
            break

        if len(cam_data_q) != 0:
            ori_size = 0
            cam_d = cam_data_q.popleft()

            files = os.listdir( os.path.join(raw_data_path, cam_d ) )
            compressed_res = os.path.join(compressed_path, f"CAM_{Vehicle_ID}"+cam_d + ".zip")
            with zipfile.ZipFile( compressed_res ,mode = "w", compresslevel = 9) as camzip:
                for f in files:
                    camzip.write( os.path.join(raw_data_path, cam_d,f), compress_type=zipfile.ZIP_DEFLATED)
                    ori_size += os.path.getsize( os.path.join(raw_data_path, cam_d,f) )
                camzip.close()
            com_size = os.path.getsize(  compressed_res )
            if (ori_size == 0) or (com_size == 0) :
                continue
            
            space_savings = (1 - ( com_size / ori_size)) * 100
            print(f"CAM_SPACE_SAVINGS : {space_savings:4.2f}_{compressed_res}")
            
            shutil.rmtree(os.path.join(raw_data_path, cam_d))

def DEM_compression(arg_list):
    Vehicle_ID = arg_list[1]["Vehicle_ID"]
    compressed_path = os.path.join(arg_list[0].compressed_data_path) 
    raw_data_path = os.path.join(arg_list[0].raw_data_path,"DEM_DIR")

    file_list = os.listdir(raw_data_path)
    file_list.sort()
    dem_data_q = deque(file_list)
    dem_list = []

    while True:
        if len(dem_data_q) == 0 :
            file_list = os.listdir(raw_data_path)
            file_list.sort()
            print(f"[ Average ]dem_spacce_savings : {np.mean(dem_list)}")
            break

        if len(dem_data_q) != 0:
            dem_f = dem_data_q.popleft()
            file_name = dem_f.split(".")[0]
            compressed_res =  os.path.join( compressed_path, f"DEM_{Vehicle_ID}"+file_name +".zip")
            my_zip = zipfile.ZipFile(compressed_res ,mode='w', compresslevel = 9)  # zip파일 쓰기모드
            
            my_zip.write( os.path.join(raw_data_path, dem_f) , compress_type=zipfile.ZIP_DEFLATED )         # 압축할 파일 write
            my_zip.close()

            com_size = os.path.getsize( compressed_res )
            ori_size = os.path.getsize(  os.path.join(raw_data_path,dem_f) )
            if (ori_size == 0) or (com_size == 0) :
                continue
            space_savings = (1 - ( com_size / ori_size)) * 100
            dem_list.append(space_savings)
            print(f"DEM_SPACE_SAVINGS : {space_savings:4.2f}_{compressed_res}")
            os.remove(os.path.join(raw_data_path,dem_f))



def CANFD_compression(arg_list):
    Vehicle_ID = arg_list[1]["Vehicle_ID"]
    compressed_path = os.path.join(arg_list[0].compressed_data_path) 
    raw_data_path = os.path.join(arg_list[0].raw_data_path, "CAN_DIR")
    file_list = os.listdir(raw_data_path)
    sorted(file_list)
    canfd_data_q = deque(file_list)
    canfd_list = []
    while True:

        if len(canfd_data_q) == 0 :
            file_list = os.listdir(raw_data_path)
            sorted(file_list)
            print(f"canfd_space_savings {np.mean(canfd_list)}")    
            break

        if len(canfd_data_q) != 0:
            canfd_f = canfd_data_q.popleft()
            file_name = canfd_f.split(".")[0]
            compressed_res =  os.path.join( compressed_path,f"CAN_{Vehicle_ID}" + file_name +".zip")
            my_zip = zipfile.ZipFile( compressed_res ,mode= 'w', compresslevel = 9)  # zip파일 쓰기모드
            my_zip.write( os.path.join(raw_data_path,canfd_f), compress_type=zipfile.ZIP_DEFLATED )         # 압축할 파일 write
            my_zip.close()

            com_size = os.path.getsize(compressed_res )
            ori_size = os.path.getsize(  os.path.join(raw_data_path,canfd_f) )
            if (ori_size == 0) or (com_size == 0) :
                continue
            space_savings = (1 - ( com_size / ori_size)) * 100
            print(f"CAN_SPACE_SAVINGS : {space_savings:4.2f} _ {compressed_res}")
            os.remove(os.path.join(raw_data_path,canfd_f))

def RuleCompression():

    parser = get_argument_parser()
    args = parser.parse_args()

    manager = Manager()
    arg_list = manager.list()
    arg_list.append(args)
    arg_list.append({"Vehicle_ID" : "123eab0804567_"})


    p1_GPS = Process(target=GPS_compression,args=(arg_list, ))
    p1_GPS.start()
    
    p2_CAM = Process(target=CAM_compression,args=(arg_list, ))
    p2_CAM.start()

    p3_DEM = Process(target=DEM_compression,args=(arg_list, ))
    p3_DEM.start()

    p4_CANFD = Process(target=CANFD_compression,args=(arg_list, ))
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