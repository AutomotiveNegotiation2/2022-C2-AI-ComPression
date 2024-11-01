# 차량 센서 데이터 수집 프로그램

- 차량의 다종 센서(GPS, CANFD, Camera)에서 데이터를 수집하기 위한 프로그램

- Contributors : KETI(한국전자기술연구원)
- TASK : 차량 센서 데이터 수집



## File Layout

-  GPS_read.py


### GPS_read
- GPS 데이터 수집 환경
- 필요 프로그램
```
pip install pyubx2
pip install pyserial
```
- NMEA( The National Marine Electronics Association) 규격을 사용하는 데이터를 1초마다 수집함
- GPS 표준 프로토콜