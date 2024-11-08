import numpy as np
import datetime
import time
import json
import image2world
import get_obj_pos

# Load configuration file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Load camera homographies
cam01_H = np.load(config["camera_matrices"]["cam01_H"])
cam02_H = np.load(config["camera_matrices"]["cam02_H"])
cam03_H = np.load(config["camera_matrices"]["cam03_H"])
cam04_H = np.load(config["camera_matrices"]["cam04_H"])

# Set constants and dictionaries
DEG_TO_RAD = config["constants"]["DEG_TO_RAD"]
canfd_dict = config["canfd_dict"]
cam_det_px_dict = config["cam_det_px_dict"]

def process_camera_objects(cam_pos, cam_index, cam_objs, homography, angle_offset, det_px_dict_key,mylat, mylon, my_head):
    global cam_obj_gps, cam_obj
    cam_pos[cam_index] = 1
    for obj in cam_objs:
        obj_class, det_x, det_y = obj
        px, py = image2world(homography, det_x, det_y)
        trans_lat, trans_lon = get_obj_pos(mylat, mylon, my_head + angle_offset, px, py)
        if (det_x > cam_det_px_dict[det_px_dict_key][0]) and (det_x < cam_det_px_dict[det_px_dict_key][1]) and \
           (det_y > cam_det_px_dict[det_px_dict_key][2]) and (det_y < cam_det_px_dict[det_px_dict_key][3]):
            cam_obj_gps.append([cam_index, obj_class, trans_lat, trans_lon])
        cam_obj.append([cam_index, obj_class, det_x, det_y])


def DEM_GEN(arg_list, ):
    dem_str = ""
    mct = 0
    del_t = 0
    raw_t = ""
    date_time = datetime.datetime.now()
    datetime_now = str()
    my_head = 0
    cam_pos = [0,0,0,0]
    cam_obj = []
    cam_obj_gps= []
    sign,gear = "", ""
    speed,handle = 0, 0
    past_speed = 0
    lat,lon = "", ""
    mylat, mylon = 0, 0
    
    timestamp_d = ''
    raw_t = ''
    
    while True:
        s_t = time.time()
        gps_d = arg_list[3]
        canfd_d = arg_list[0]
        timestamp_d = arg_list[1]     

        if del_t > 1:
            arg_list[2] = dem_str
            dem_str = ""
            del_t = 0

        if len(canfd_d):
            for c1 in canfd_d.split("\n"):
                try:
                    #print(c1)
                    canfd_line = c1.split()
                    if len(canfd_line) != 0: 
                        if canfd_dict["blink"][0] in canfd_line[1]:
                            if canfd_line[canfd_dict["blink"][1]] == canfd_dict["blink"][2]: #blink 2
                                sign = 3
                        if canfd_dict["gear"][0] in canfd_line[1]: # gear data7 D	0A	R	00	N,P	0B
                            #print(canfd_line)
                            if canfd_line[canfd_dict["gear"][1]] == canfd_dict["gear"][2]:
                                gear = "D"
                            elif canfd_line[canfd_dict["gear"][1]] == canfd_dict["gear"][3]:
                                gear = "R"
                            elif canfd_line[canfd_dict["gear"][1]] == canfd_dict["gear"][4]:
                                gear = "P"
                        if canfd_dict["speed"][0]  in canfd_line[1]: # speed data8                            
                            if len(canfd_line) > 10:
                                speed = int(canfd_line[canfd_dict["gear"][1]], 16)
                                past_speed = speed
                            else:
                                speed = past_speed
                            
                        if canfd_dict["blink2"][0] in canfd_line[1]: # re blink data5 꺼짐	01 -> 00 우측 11->10 좌측 05->04
                            if  canfd_line[canfd_dict["blink2"][1]] == canfd_dict["blink2"][2]:
                                sign = 0
                            elif canfd_line[canfd_dict["blink2"][1]] == canfd_dict["blink2"][3]:
                                sign = 1
                            elif canfd_line[canfd_dict["blink2"][1]] == canfd_dict["blink2"][4]:
                                sign = 2

                        if canfd_dict["handle"][0] in canfd_line[1] : # data 16 17 -> 9 10 11 12
                            handle = int(canfd_line[canfd_dict["handle"][1]],16)
                            + int(canfd_line[canfd_dict["handle"][2]],16)
                            + int(canfd_line[canfd_dict["handle"][3]],16)
                            + int(canfd_line[canfd_dict["handle"][4]],16)

                except Exception as E:
                    print(E)        

