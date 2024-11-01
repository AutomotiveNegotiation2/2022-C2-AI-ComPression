import cv2
import time
# opencv library info
# https://pypi.org/project/opencv-python/
def read_data(share_list ) :
    print("START_CAMERA")

    RTSP_URL1 = "rtsp:"
    RTSP_URL2 = "rtsp:"
    RTSP_URL3 = "rtsp:"
    RTSP_URL4 = "rtsp:"
    interval = 30
    
    cap1 = cv2.VideoCapture(RTSP_URL1)
    cap2 = cv2.VideoCapture(RTSP_URL2)
    cap3 = cv2.VideoCapture(RTSP_URL3)
    cap4 = cv2.VideoCapture(RTSP_URL4)
    frame_count = 0
    
    while True :
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        ret4, frame4 = cap4.read()
        
        if not ret1 :
            break
        
        frame_count += 1
        
        if frame_count % interval == 0 :
            frame_count = 0
            now_time = round(time.time(), 3)
            share_list[4] = [frame1,frame2,frame3,frame4]



if __name__ == "__main__":
    main()