# Hybrid_compression_model



## Description

- AI 기반 압축 모델(Dzip)과 Rule 기반 압축(zlib)을 결합한 Hybrid 압축 모델 

  - 차량의 주행 상태에 따라 압축 방식을 달리하여 CAN 데이터를 압축함.
    - 차량 주행 상태에서는 AI 기반 압축 모델 활용
    - 차량 정차 상태에서는 Rule 기반 압축 모델 활용

![평가지표](README.assets/compression_process.JPG)



## DATA

- CAN_DATA : CAR HACKING: ATTACK & DEFENSE CHALLENGE 2020

  - https://ieee-dataport.org/open-access/car-hacking-attack-defense-challenge-2020-dataset
    - CITATION : Hyunjae Kang, Byung Il Kwak, Young Hun Lee, Haneol Lee, Hwejae Lee, Huy Kang Kim, February 3, 2021, "Car Hacking: Attack & Defense Challenge 2020 Dataset", IEEE Dataport, doi: [https://dx.doi.org/10.21227/qvr7-n418](https://www.google.com/url?q=https%3A%2F%2Fdx.doi.org%2F10.21227%2Fqvr7-n418&sa=D&sntz=1&usg=AOvVaw33jtPkJFFezo3LcnKQmvju)


  - 해당 데이터 셋에서 정상 주행 및 정차 데이터만 압축에 사용하였음.





## Hybrid Compression RESULT

- 압축 성능 지표는 Space savings 를 사용함.


![평가지표](README.assets/Space_saving.JPG)



- CAN 데이터 크기를 증가시키며 Space Savings 결과를 확인한 그래프 



## Environment

- Ubuntu 18.04
- CUDA 11.1
- cudnn 8
- docker
- Python 3.6.10





**CITE**

- DZip: improved general-purpose loss less compression based on novel neural network modeling
  - https://github.com/mohit1997/Dzip-torch
