# 차량 센서 데이터 수집 프로그램

- 차량의 다종 센서(GPS, CANFD, Camera)에서 데이터를 수집하기 위한 프로그램

- Contributors : KETI(한국전자기술연구원)
- TASK : 차량 센서 데이터 수집

## File Layout
- GPS_read.py
- CAMERA_read.py
- CANFD_read.py
- SENSOR_PARSER.py
- TIMESTAMP_read.py
- DEM_gen.py

### GPS_read
![GPS_device](README.assets/GPS_device.png)
- GPS 데이터 수집 환경
    - NEO-7M GPS 모듈 활용
```
pip install pyubx2
pip install pyserial
```
- NMEA( The National Marine Electronics Association) 규격을 사용하는 데이터를 1초마다 수집함
- GPS 표준 프로토콜

### TIMESTAMP_read
![alt2 text](README.assets/Device.png)
![alt3 text](README.assets/sketch.png)
- TIMESTAMP 수집환경
    - 아두이노를 활용하여 1ms 단위의 누적 timestamp 생성
    - GPS의 pps(Pulse per second) 신호가 발생할 때마다 timestamp 갱신

### CAMERA_read
![CAMERA_device](README.assets/CAMERA_device.png)
- CAMERA 데이터 수집 환경
    - GPI IP Mobile Outdoor 카메라
```
pip install opencv-python
```
- RTSP를 활용하여 영상 데이터를 실시간으로 수집함
- 카메라 4대가 전,후,좌,우로 설치되어 있으며 1초에 카메라별 1장씩 데이터를 저장함

### CANFD_read
![Controller_Area_Network](README.assets/CANFD_network.png)
![alt text](README.assets/peakcan.png)
- CANFD 데이터 수집 환경
    - 상용차량(샤시캔), PCAN-USB Pro FD
- CAN Logger 장치 사에서 제공하는 프로그램과 Local 통신하여 데이터 수집
- 1초 동안 데이터를 수집하여 저장함

### DETECT_read
![alt bb](README.assets/bbox.png)
- YOLO BBOX의 하단 중심점 좌표(x,y)를 나타내며, 사람, 차량 클래스를 포함함
- ex) [1, 343, 123] : 사람(1), x점(343), y점(123)을 나타냄
- YOLO 모델에서 수집한 BBOX 정보를 socket으로 받아 저장함


### DEM_gen
![DEM]( README.assets/DEM_proto.png)
- CANFD, GPS, CAMERA 데이터를 활용하여 자율 주행 중 주변 상황에 대한 정보를 포함함
    - DeepLearning model을 활용한 Object Detection 정보
    - Object Detection된 카메라 정보
    - Object Detection 정보와 GPS 정보를 활용하여 주변 객체의 픽셀 및 GPS 위치 정보
    - CANFD에서 추출한 차량의 속도, 지시등, 핸들, 변속 기어 정보
    - GPS에서 추출한 차량의 GPS 위치 정보
- 메시지는 정보를 1초마다 갱신하여 저장함

### SENSOR_PARSER
- 각종 센서 데이터를 모아서 저장하는 프로그램
- 센서별 비동기적 프로세스를 multiprocessing을 활용 동시에 수집함
- Timestamp를 활용하여 동기적으로 각종 데이터를 저장함
    - GPS, CANFD, DEM, CAMRERA

