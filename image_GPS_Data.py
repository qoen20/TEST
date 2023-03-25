import GPSYO
import math
import os
import re

from PIL import Image
import numpy as np
from haversine import haversine


H20TCamera = [4056, 3040]
H20TFoc = 0.0045
H20TCmos = [0.00617, 0.00455]

# 촬영 높이 정보
wall_height = 20
height_image = 15

# 지정된 폴더 경로
folder_path = 'C:/Users/Y/Desktop/GPS2.0v/wallPoint'
folder_path2 = 'C:/Users/Y/Desktop/GPS2.0v/wallimage'

# 폴더 경로 내 모든 파일 리스트
file_list = os.listdir(folder_path)
file_list2 = os.listdir(folder_path2)

# 이미지 파일 리스트
image_list = [file for file in file_list if file.endswith(('JPG','jpg', 'jpeg', 'png', 'gif'))]
image_list2 = [file for file in file_list2 if file.endswith(('JPG','jpg', 'jpeg', 'png', 'gif'))]
txt_list = [file for file in file_list2 if file.endswith('txt')]

T = []
TT = []
TTT = []
TTTT = []
TX = []
TX_IF = []
TX_EF = []

# 이미지 파일 불러오기
for image_name in image_list:
    image_path = os.path.join(folder_path, image_name)
    image = Image.open(image_path)
    # 이미지 처리 코드
    T.append(GPSYO.getGPS(image_path))

# 이미지 파일 불러오기2
for image_name2 in image_list2:
    image_path2 = os.path.join(folder_path2, image_name2)
    image = Image.open(image_path2)
    # 이미지 처리 코드
    TT.append(GPSYO.getGPS(image_path2))

# 이미지 파일 불러오기2 ================================================================================== 수정 . . . .
for txt_name in txt_list:
    txt_path = os.path.join(folder_path2, txt_name)
    with open(txt_path, 'r', encoding='utf-8') as f:
        txtdata = f.read()
        pattern = r'\d+'
        pattern_C=re.findall(pattern, txtdata)
        TX.append(pattern_C)
print(TX[2])

# 첫 번째 이미지의 GPS 좌표
lat1, lon1 = T[0][0], T[0][1]
print("L1 좌표",lat1,',',lon1)
# 두 번째 이미지의 GPS 좌표
lat2, lon2 = T[1][0], T[1][1]
print("L2 좌표",lat2,',',lon2)
# 두 GPS 좌표 사이의 거리 (km)
distance = haversine((lat1, lon1), (lat2, lon2))

print("드론 촬영 좌표 ", TT)

# L1, L2 GPS 좌표
L1 = (lat1, lon1)
L2 = (lat2, lon2)

# L1과 L2 사이의 거리 계산
distance = ((L1[0]-L2[0])**2 + (L1[1]-L2[1])**2)**0.5

# L1과 L2 사이의 거리를 1000등분하여 좌표 생성
latitudes = np.linspace(L1[0], L2[0], 1000)
longitudes = np.linspace(L1[1], L2[1], 1000)
coordinates = list(zip(latitudes, longitudes))

# 벽면 높이 할당
altitudes = np.linspace(0, 20, 201)
points = []
points_save = []
for altitude in altitudes:
    points.extend([(coord[0], coord[1], altitude) for coord in coordinates])
    points_save.extend([(coord[0], coord[1], altitude) for coord in coordinates])


# 해당 범위 내의 GPS 좌표와 해당 범위 밖의 GPS 좌표의 최소 거리 계산
in_range = [] # 5000개 포인트 루프
out_range = [] # 최소 거리에 대한 벽면 좌표
min_distance = [] # 최소 거리 값

for iii in range(0, len(TT)):
    for ii in range(0, 5000): # 5000개 점을 전부 지나칠때 까지.
            Sr = haversine((points[ii][0],points[ii][1]), TT[iii], unit='m') # 벽면 포인트 하나와 드론 촬영 포인트 하나 사이의 거리 측정
            in_range.append(Sr) # 위 거리값 수집
            ii = ii + 1

            if ii == 5000: # 5000개 점을 전부 지나치면

                min_distance.append(min(in_range)) # 최소 거리 값 수집
                OR = in_range.index(min(in_range)) # 최서 거리 값에 대한 리스트 번호 정의
                out_range.append(points[OR])

                print("Image Number:", iii)
                print("최단 거리 :", min(in_range), "m") # 가장 최소가 되는 거리값 추출
                print("드론 촬영 이미지의 최소 거리에 해당하는 벽면 좌표: ", out_range[iii])
                print("드론이 촬영한 이미지의 좌표 :", TT[iii])
                print("==============================================================")

                rs_long = (min(in_range) * H20TCmos[0]) / (H20TFoc * H20TCamera[0])
                image_lo = rs_long * H20TCamera[0]  # 가로 길이
                rs_lat = (min(in_range) * H20TCmos[1]) / (H20TFoc * H20TCamera[1])
                image_lat = rs_lat * H20TCamera[1]  # 세로 길이
                image_size = image_lo * image_lat
                print("\\\ 사진 해상도 수집 //")
                print('이미지 가로 픽셀당 크기 = ', rs_long, 'm')
                print("이미지 가로 길이 : ", image_lo, "m")
                print("세로 한 픽셀당 크기 : ", rs_lat, "m")
                print("이미지 세로 길이 : ", image_lat, "m")
                print("이미지 면적 :", image_size, "m^2")
                print("I==================================================================="
                      "===========================I")
                in_range.clear()





#
#                 iiii = 0
#                 iiiii = 0
#                 TTTTT = []
#                 TO = []
#                 TP = []
#
#
#                 for iiii in range(0, len(points)):  # 0.1m 높이에 대한 벽면 가로 좌표부터 20m 높이 벽면 가로좌표 까지.
#                     x, y, z = points[iiii][0], points[iiii][1], points[iiii][2]
#                     # print(x, y, z)
#                     if height_image - (image_lat / 2) <= z <= height_image + (image_lat / 2): # 높이 범위가 이미지 해상도 범위 안에 있을 때.
#                         TTT.append(z) # 해당 points 수집.
#                         Sr2 = haversine((x,y),(out_range[iii][0], out_range[iii][1]), 'm')
#                         if (image_lo / 2) <= Sr2 <= (image_lo / 2) + 0.1:
#                             TTTT.append(iiii)
#
#
#
#                         if (image_lo / 2) >= Sr2:
#                             TO.append(points[iiii])
#                         #     TTTTT.append(points[iiii]) # 추후 중복 제거를 해야할 필요가 있을 때 개시
#                         #     print(TTTTT)
#                         #     if points[iiii] in points_save:
#                         #         points_save = [o for o in points_save if o not in TTTTT]
#                         #         TTTTT.clear()
#                             # print(points_save)
#
#
#                     iiii = iiii + 1
#
#                 OT = []
#                 OB = []
#
#                 # print(len(TTT))
#                 print("벽면에서 이미지가 포함되는 영역", points[min(TTTT)], points[max(TTTT)])
#                 result = [[t for t in TO if t[2] == z] for z in set(t[2] for t in TO)]
#                 # print(result[0][0][1])
#                 if len(TX[iii]) > 2:
#                     p = 0
#                     for p in range(0, len(result)):
#                         k = 0
#                         for k in range(0, len(result[p])):
#                             x, y, z = result[p][k][0], result[p][k][1], result[p][k][2]
#                             # print(x, y, z)
#                             if height_image - (image_lat / 2) <= z <= height_image + (image_lat / 2):  # 높이 범위가 이미지 해상도 범위 안에 있을 때.
#                                 Sr3 = haversine((x, y), (out_range[iii][0], out_range[iii][1]), 'm')
#                                 if k >= (len(result[p]) / 2):
#                                     print("뒷열", k)
#                                     OT.append(result[p][k])
#                                 else:
#                                     print("앞열", k)
#                                     OB.append(result[p][k])
#                                 if (image_lo / 2) >= Sr3:
#                                     # print(Sr3)
#                                     TX_IF.append(iiiii)
#                                     # print(Sr3)
#                             # for a in range(0, len(TX_IF)):
#                             #     x, y, z = points[TX_IF[a]][0], points[TX_IF[a]][1], points[TX_IF[a]][2]
#                             #     Sr4 = haversine((x, y), (out_range[iii][0], out_range[iii][1]), 'm')
#                             #     for b in range(0, len(TX[iii])):
#                             #         if b == 3:
#                             #             if ((height_image - (image_lat / 2)) + (rs_lat * int(TX[iii][b - 2])) <= z <= ((height_image - (image_lat / 2)) + (rs_lat * int(TX[iii][b])))):
#                             #                 # print((image_lo / 2) - (rs_long * int(TX[iii][b-3])), ((image_lo / 2) - (rs_long * int(TX[iii][b-1]))))
#                             #                 # print(Sr4)
#                             #                 if abs((image_lo / 2) - (rs_long * int(TX[iii][b-3]))) >= Sr4 >= abs((image_lo / 2) - (rs_long * int(TX[iii][b-1]))):
#                             #
#                             #
#                             #                     print(Sr4)
#                             #                     # pass
#
#                                 iiiii = iiiii + 1
#                             k = k + 1
#                         p = p + 1
#                         TTT.clear()
#                     # print(len(points_save))
#
#                         # if len(TX[iii]) > 2:
#                         #     for iiiii in range(0, len(points)):  # 0.1m 높이에 대한 벽면 가로 좌표부터 20m 높이 벽면 가로좌표 까지.
#                         #         x, y, z = points[iiiii][0], points[iiiii][1], points[iiiii][2]
#                         #
#                         #         if height_image - (image_lat / 2) <= z <= height_image + (image_lat / 2):  # 높이 범위가 이미지 해상도 범위 안에 있을 때.
#                         #             Sr3 = haversine((x, y), (out_range[iii][0], out_range[iii][1]), 'm')
#                         #             # print(Sr3)
#                         #             if (image_lo / 2) >= Sr3:
#                         #                 # print(Sr3)
#                         #                 TX_IF.append(iiiii)
#                         #     for a in range(0, len(TX_IF)):
#                         #         x, y, z = points[TX_IF[a]][0], points[TX_IF[a]][1], points[TX_IF[a]][2]
#                         #         Sr4 = haversine((x, y), (out_range[iii][0], out_range[iii][1]), 'm')
#                         #         for b in range(0, len(TX[iii])):
#                         #             if b == 3:
#                         #                 if ((height_image - (image_lat / 2)) + (rs_lat * int(TX[iii][b - 2])) <= z <= ((height_image - (image_lat / 2)) + (rs_lat * int(TX[iii][b])))):
#                         #                     # print((image_lo / 2) - (rs_long * int(TX[iii][b-3])), ((image_lo / 2) - (rs_long * int(TX[iii][b-1]))))
#                         #                     # print(Sr4)
#                         #                     if abs((image_lo / 2) - (rs_long * int(TX[iii][b-3]))) >= Sr4 >= abs((image_lo / 2) - (rs_long * int(TX[iii][b-1]))):
#                         #
#                         #
#                         #                         # print(Sr4)
#                         #                         pass
#                         #
#                         #         iiiii = iiiii + 1
#                         #
#                         # TTT.clear()
#                         # print(TP)
#                         # print(len(TTTT))
#                         # # print(len(points_save))
#     iii = iii + 1
#
# # (image_lo / 2) - (rs_long * int(TX[iii][b-3])) <= Sr3 <= (image_lo / 2) - (rs_long * int(TX[iii][b-1]))
# # print(len(result[1]))
# # print(TO[100])
# print(max(OT), min(OT))
# # print(OT)
# print("===-=-=-=============")
# print(max(OB), min(OB))