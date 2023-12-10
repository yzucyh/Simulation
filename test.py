import math
from shapely import geometry

# import matplotlib.pyplot as plt

# # 输入数据
# horizontal_distance = 100  # 飞机与卫星之间的水平距离（单位：公里）
# aircraft_height = 10  # 飞机高度（单位：公里）
# satellite_height = 780  # 卫星高度（单位：公里）
# earth_radius = 6371  # 地球的平均曲率半径（单位：公里）

# # 计算斜边
# distance_to_satellite = math.sqrt((earth_radius + satellite_height) ** 2 - (earth_radius + aircraft_height) ** 2)

# # 检查是否超出定义域范围
# if -1 <= distance_to_satellite / (2 * earth_radius) <= 1:
#     # 计算仰角（弧度）
#     elevation_angle_rad = math.asin(distance_to_satellite / (2 * earth_radius))

#     # 将弧度转换为度
#     elevation_angle_deg = math.degrees(elevation_angle_rad)

#     print(f"仰角（弧度）：{elevation_angle_rad}")
#     print(f"仰角（度）：{elevation_angle_deg}")

#     # 创建图形
#     plt.plot([0, horizontal_distance], [aircraft_height, aircraft_height])
#     plt.plot([horizontal_distance, 0], [satellite_height, satellite_height])
#     plt.plot([0, horizontal_distance], [aircraft_height, satellite_height], linestyle='--', color='red')
#     plt.xlabel("horizontal km")
#     plt.ylabel("height km")
#     plt.title("plt")
#     plt.show()
# else:
#     print("仰角无效，超出定义域范围")

# import csv 
# import os

# sat_number = 1
# file_dir = './data/satellite/Orbit_'+str(1)
# fileList = []
# allList = os.walk(file_dir)
# for _, _, txt in allList:
#     allList_index = txt
# for index in allList_index:
#     fileList.append(file_dir+'/'+index)
# for fname in fileList:
#     with open(fname, 'r', encoding='UTF-8') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)
#         tmp_lat = []
#         tmp_long = []
#         for r in reader:
#             print(r)
#         csvfile.close()
#     sat_number = sat_number + 1

source = [86.40433644,58.18551796]
coverage = {'1-1': [(86.42133531,54.34108931), (86.4186104,55.30535397), (86.41486669,56.26787347), (86.41010735,57.22810612)],
            '1-2': [(50.008872936737724, 143.57577811264377), (50.008872936737724, 131.1206162873562), (57.38318828326228, 143.57577811264377), (57.38318828326228, 131.1206162873562)]
            }

def compute_covered(source, coverage):
    covered_sat = []
    pt = (source[0], source[1])
    print(pt)
    for IndexOfSat, square in coverage.items():
        if in_square(square, pt) == True:
            covered_sat.append(IndexOfSat)
    return covered_sat

s = (0.5, 0.5)
sq = [(0,0), (1,0), (1,1), (0,1)]

def in_square(sq, pt):
    line = geometry.LineString(sq)
    point = geometry.Point(pt)
    sq = geometry.Polygon(line)
    return sq.contains(point)

print(compute_covered(source, coverage))

#(82.71040112673772, 117.82141069596275), (82.71040112673772, 0.4577582640372597), (90.08471647326228, 117.82141069596275), (90.08471647326228, 0.4577582640372597)