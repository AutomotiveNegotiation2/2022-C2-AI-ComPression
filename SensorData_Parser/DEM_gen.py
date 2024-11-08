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
