import socket

def read_data(share_list, host='localhost', port=9092):

    #print("DETECT_START")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        datas= "start"
        try:
            while datas:
                datas = s.recv(10000)
                if len(datas)!= 0:
                    share_list[6] = datas.decode()
        except ConnectionResetError:
            print('Connection closed by server.')

if __name__ == "__main__":
    data_list = [[] for _ in range(7)]
    try:
        while True:
            read_data(data_list)
    except Exception as e:
        print(e)