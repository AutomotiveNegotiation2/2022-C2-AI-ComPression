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

