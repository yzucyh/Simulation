import os
import csv
import math 

class SatGenerator:
    def __init__(self, number):
        self.number = number
        self.head = None
        self.tail = None
        self.sat_info = {1:Satellite, 2:Satellite, 3:Satellite, 4:Satellite, 5:Satellite, 6:Satellite, 7:Satellite, 8:Satellite, 9:Satellite, 10:Satellite} # 一個軌道固定10顆衛星

    def add_satellite(self, number, sat_lat, sat_long, coverage):
        if not isinstance(number, Satellite):
            self.sat_info[number] = Satellite(number, 28, 500, 10, 10, 100, sat_lat, sat_long, coverage)

    def GenerateOrbit(self):
        sat_number = 1
        file_dir = './data/satellite/Orbit_'+str(self.number)
        fileList = []
        allList = os.walk(file_dir)
        for _, _, txt in allList:
            allList_index = txt
        for index in allList_index:
            fileList.append(file_dir+'/'+index)
        for fname in fileList:
            with open(fname, 'r', encoding='UTF-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                tmp_lat = []
                tmp_long = []
                for r in reader:
                    tmp_lat.append(float(r[0]))
                    tmp_long.append(float(r[1]))
                coverage = self.add_coverage(tmp_lat, tmp_long)
                self.add_satellite(sat_number, tmp_lat, tmp_long, coverage)
                csvfile.close()
            sat_number = sat_number + 1

     # https://www.jianshu.com/p/1d71ec4367d4
    def add_coverage(self, lat, long):
        R = 6373 * 1000 # 單位: m
        distance = 580 * 1000 
        azimuth = 135
        coverage = []
        for i in range(0, len(lat)):
            tmp = []
            for index in range(0, 4): # +-
                if index == 0:
                    lat2 = lat[i] + distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                    lon2 = long[i] + distance * math.sin(math.radians(azimuth)) / (R * 2 * math.cos(math.radians(lat[i])) * math.pi/ 360)
                elif index == 1:
                    lat2 = lat[i] + distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                    lon2 = long[i] - distance * math.sin(math.radians(azimuth)) / (R * 2 * math.cos(math.radians(lat[i])) * math.pi/ 360)
                elif index == 2:
                    lat2 = lat[i] - distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                    lon2 = long[i] + distance * math.sin(math.radians(azimuth)) / (R * 2 * math.cos(math.radians(lat[i])) * math.pi/ 360)
                else:
                    lat2 = lat[i] - distance * math.cos(math.radians(azimuth)) / (R * 2 * math.pi / 360)
                    lon2 = long[i] - distance * math.sin(math.radians(azimuth)) / (R * 2 * math.cos(math.radians(lat[i])) * math.pi/ 360)
                tmp.append((float(lat2), float(lon2)))
            coverage.append(tmp)
        # print(coverage[0])
        return coverage

    def GetSatInfo(self):
        return self.sat_info
    
class Satellite:
    def __init__(self, number, freq, bandwidth, Tx, Rx, channel_num, sat_lat, sat_long, coverage):
        self.next = None
        self.number = number
        self.Freq = freq
        self.Bandwidth = bandwidth
        self.Tx = Tx
        self.Rx = Rx
        self.numChannel = channel_num
        self.ISL_link = 2
        self.ISL_state = {0, 1}
        self.sat_lat = sat_lat
        self.sat_long = sat_long
        self.coverage = coverage