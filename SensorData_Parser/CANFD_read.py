import socket
import time


def read_data(share_list, host='127.0.0.1', port=65432):
    delta_t = 0
    print("START_CANFD")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f'Connected to {host}:{port}')
        data_str = ""
        while True:
            before_recv_t = time.time()
            if delta_t > 1.0:
                share_list[0] = data_str
                data_str = ""
                delta_t = 0
            data = s.recv(10000000)
            data_str += (data.decode()[:] + "\n")
            if len(data) == 0:
                break
            after_recv_t = time.time()
            delta_t += (after_recv_t - before_recv_t)
            
            
if __name__ == "__main__":
    data_list = [[] for _ in range(6)]
    read_data(data_list)