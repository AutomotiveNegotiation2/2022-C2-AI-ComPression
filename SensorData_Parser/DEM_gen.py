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

        if len(gps_d):
            for g1 in gps_d.split("\n"):
                data_line_sp = g1.split(",")
                if data_line_sp[0] == "$GPRMC":
                    utc_time = data_line_sp[1]
                    hour = int(utc_time[:2]) +9 
                    minute = int(utc_time[2:4])
                    second =int( utc_time[4:6])
                    lat = data_line_sp[3]
                    lon = data_line_sp[5]
                    
                    lat = float(str(lat)[:2]) + float(str(lat)[2:]) /60
                    lon = float(str(lon)[:3]) + float(str(lon)[3:]) /60
                    if len(data_line_sp[8]) !=0:
                        head = float(data_line_sp[8])
                    else:
                        #NOT_TRACK_HEAD"
                        head = my_head
                    
                    mylat = lat
                    mylon = lon
                    my_head = head
                    yr = str(time.localtime().tm_year)
                    month = "0"+ str(time.localtime().tm_mon) if len(str(time.localtime().tm_mon)) == 1 else str(time.localtime().tm_mon) 
                    day = "0" +str(time.localtime().tm_mday) if len(str(time.localtime().tm_mday)) == 1 else str(time.localtime().tm_mday)
                    
                    raw_data_name = f"{yr}{month}{day}_{hour:02d}{minute:02d}{second:02d}"
                    raw_t = f"{yr}{month}{day}_{hour:02d}{minute:02d}{second:02d}"
                    
                else:
                    yr = str(time.localtime().tm_year)
                    month = "0"+ str(time.localtime().tm_mon) if len(str(time.localtime().tm_mon)) == 1 else str(time.localtime().tm_mon) 
                    day = "0" +str(time.localtime().tm_mday) if len(str(time.localtime().tm_mday)) == 1 else str(time.localtime().tm_mday)
                    
                    hour= int(time.localtime().tm_hour)
                    minute = int(time.localtime().tm_min)
                    second = int(time.localtime().tm_sec)
                    
                    raw_t = f"{yr}{month}{day}_{hour}{minute:02d}{second:02d}"

        
        global_t = f'{raw_t}_{timestamp_d}'
        detect_d = arg_list[6]
        if len(detect_d):

            j_d = json.loads(detect_d)
            cam1 = j_d["cam1"]
            cam2 = j_d["cam2"]
            cam3 =  j_d["cam3"]
            cam4 = j_d["cam4"]
            #print(detect_d)
            cam_pos[0] = 1

            # Process camera 1
            process_camera_objects(cam_pos,0, cam1, cam01_H, 0, "cam1", mylat, mylon, my_head)

            if sign == 1:
                # Process camera 2 and 4
                process_camera_objects(cam_pos,1, cam2, cam02_H, 90, "cam2", mylat, mylon, my_head)
                process_camera_objects(cam_pos,3, cam4, cam04_H, 180, "cam4",mylat, mylon, my_head)
            elif sign == 2:
                # Process camera 3 and 4
                process_camera_objects(cam_pos,2, cam3, cam03_H, 270, "cam3",mylat, mylon, my_head)
                process_camera_objects(cam_pos,3, cam4, cam04_H, 180, "cam4",mylat, mylon, my_head)
            elif sign == 3:
                # Process camera 2, 3, and 4
                process_camera_objects(cam_pos,1, cam2, cam02_H, 90, "cam2",mylat, mylon, my_head)
                process_camera_objects(cam_pos,2, cam3, cam03_H, 270, "cam3",mylat, mylon, my_head)
                process_camera_objects(cam_pos, 3, cam4, cam04_H, 270, "cam4",mylat, mylon, my_head)
                    
        if len(global_t) > 6:
            arg_list[5] = global_t
            

            e_t =  time.time()
            ttt = (e_t - s_t)
            if ttt < 1:
                mct += 1
                DEM_format = {
                        'Timestamp': f'{raw_t}_{timestamp_d}', 
                        'Messagecount': mct, 
                        'CarSpeed': speed, 
                        'CarSign': sign, 
                        'CarMission': gear, 
                        'CarAngle': handle, 
                        'CarPosition': [lat, lon], 
                        'CameraPosition': cam_pos, 
                        'CameraDetectObj': cam_obj,
                        'CameraDetectObj_gps' : cam_obj_gps
                        
                        }

                dem_str += str(DEM_format)
                dem_str += "\n"
                cam_obj = []
                cam_obj_gps= []
                time.sleep(1 - ttt)
            else:
                print("over turn : ", ttt)
        l_t = time.time()
        del_t += (l_t - s_t)

