import serial
from pyubx2 import UBXReader
import time
# pyubx2 Library info
#https://pypi.org/project/pyubx2/0.1.0/

def read_data(share_list, port_name = "/dev/ttyACM2",baudrate= 115200) :
    # share_list  -> 수집된 데이터를 공유 데이터 리스트에 저장
    delta_t = 0
    data_str = ""
    print("START_GPS")

    while True:
        if delta_t > 1.0:
            share_list[3] = data_str
            data_str = ""
            delta_t = 0  
        before_recv_t = time.time()              
        stream = serial.Serial(port_name, baudrate, timeout = 3)
        ubr = UBXReader(stream,protfilter = 1)
        (raw_data, _) = ubr.read()
        data_str += raw_data.decode()
        data_str += "\n"
        after_recv_t = time.time()
        delta_t += (after_recv_t - before_recv_t)
        

if __name__  == "__main__":
    data_list = [[] for _ in range(6)]
    read_data(data_list,"/dev/ttyACM0",115200)
    