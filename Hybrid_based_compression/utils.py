import numpy as np
import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
import struct

class CustomDL(Dataset):

  def __init__(self, features, labels):

    self.features = features
    self.labels = labels

  def __len__(self):
    return len(self.features)

  def __getitem__(self, idx):
    if torch.is_tensor(idx):
        idx = idx.tolist()
    feat = self.features[idx]
    lab = self.labels[idx]
    sample = {'x': feat, 'y': lab}

    return sample

def strided_app(a, L, S):  # Window len = L, Stride len/stepsize = S
    nrows = ((a.size - L) // S) + 1
    n = a.strides[0]
    return np.lib.stride_tricks.as_strided(a, shape=(nrows, L), strides=(S * n, n), writeable=False)

def generate_single_output_data(series,batch_size,time_steps):
    series = series.reshape(-1)
    series = series.copy()
    data = strided_app(series, time_steps+1, 1)
    l = int(len(data)/batch_size) * batch_size

    data = data[:l] 
    X = data[:, :-1]
    Y = data[:, -1]

    return X,Y

def var_int_encode(byte_str_len, f):
    # byte to ascci
    while True:
        this_byte = byte_str_len&127
        byte_str_len >>= 7
        if byte_str_len == 0:
                f.write(struct.pack('B',this_byte))
                break
        f.write(struct.pack('B',this_byte|128))
        byte_str_len -= 1

def read_data(data_dir):
    # RAW CAN data preprocessing 
    # 
    f = open(data_dir)
    lines = f.readlines()[4:]
    f.close()
    return lines
  
def preprocessing(spd_list):
    # classified state based speed
    # 0 : static
    # 1 : dynamic
    spd = np.mean(spd_list)
    if spd == 0.0:
        state = "static"
    else:
        state = "dynamic"
    return state

def transform_hex(datafield):
    # hex to binary datafield style
    binary = ""
    for bt in datafield:
        front_byte_deci = int(bt[0],16)
        back_byte_deci = int(bt[1],16)
        front_byte_binary = bin(front_byte_deci)[2:]
        back_byte_binary = bin(back_byte_deci)[2:]
        len_front = len(front_byte_binary)
        len_back = len(back_byte_binary)
        if len_front !=4:
            front_byte_binary = "0"*(4-len_front) + front_byte_binary
        if len_back != 4:
            back_byte_binary = "0"*(4 - len_back) + back_byte_binary
        byte_sum = front_byte_binary + back_byte_binary
        binary += byte_sum[::-1]
    return binary
  
def split_can_msg(msg_line):
    line_data_field = msg_line.split()
    canid = line_data_field[1][:-1]
    data_len = line_data_field[2]
    timestamp = line_data_field[3]
    datafield = line_data_field[4:]
    return [canid, data_len, timestamp] + [datafield]
