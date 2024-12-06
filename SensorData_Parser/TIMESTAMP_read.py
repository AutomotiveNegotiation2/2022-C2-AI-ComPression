import serial
import time

global time_stamp
def get_millisecond(ms):
    global time_stamp
    time.sleep(0.001)
    time_stamp = ms
    
def read_data(share_list,port_name= "/dev/ttyACM1",baudrate = 115200) :
    print("START_TIMESTAMP")
    with serial.Serial(port_name, baudrate) as stream:
        while True:
            try:
                read_stream = stream.read(3)
                str_ms = read_stream.decode()
                get_millisecond(str_ms)

                share_list[1] = time_stamp                
            except Exception as E:
                print("ERROR: ",E)
                
if __name__  == "__main__":
    data_list = [[] for _ in range(6)]
    read_data(data_list,"/dev/ttyACM1",115200)