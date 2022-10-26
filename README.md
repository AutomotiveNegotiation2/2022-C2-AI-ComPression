# 차량 내부 네트워크 데이터 압축 프로그램 모듈

- 차량 내부 네트워크 내 시계열 데이터 특성을 활용한 AI 기반 압축 SW

- Contributors : KETI(한국전자기술연구원)
- TASK : 차량 센서 데이터 압축 기술 구현



## Directory Layout

- Compression Code
  - AI_based_compression
  - Rule_based_compression
  - Hybrid_compression


### Compression Code Description

- **AI_based_compression** : biGRU 기반 AI 압축 모델(Dzip)
- **Rule_based_compression** : 복셀라이제이션 기반 압축 모델
- **Hybrid_compression** : Rule and AI 기반 압축 모델

---



# RESULT

### 압축 성능 지표

- 데이터 압축 성능 지표

 ![평가지표](README.assets/Space_saving.JPG)



### CAN Compression

- **AI 기반 압축 모델(Dzip) 및 룰셋 기반 압축 성능 비교**
  - 1차년도의 룰셋 기반 압축 알고리즘(LZMA, bz2, zlib)
  - 2차년도 AI 기반 압축 모델(Dzip)


![image-20220816134853427](README.assets/image-20220816134853427.png)


- 정차 상황에서 룰셋 기반 압축의 성능(Space savings)은 주행 상황보다 높으며, AI 기반 압축 모델은 정차 및 주행 상황 모두에서 압축 성능이 뛰어남. 



- **하이브리드 기반 압축 모듈 성능 평가**





### Lidar Compression

- 2차년도 룰셋 기반 압축 모델(Voxelization)
  - Rule 기반 압축 모델 활용 차량 라이다 데이터 성능 평가


![image_voxelization](README.assets/voxelization_result.png)
