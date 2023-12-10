from math import sin, cos, sqrt, atan2, radians
from SatGenerator import SatGenerator, Satellite
import scipy.constants as sc
import math
from geopy.distance import geodesic
from shapely import geometry
import pandas as pd

R = 6373.0
H = 610
Airplane_H = 10
diff_H = H - Airplane_H

class Agent:
    def __init__(self, number, source, destination, data_lat, data_long, coverage, sec):
        self.number = number
        self.source = source
        self.destination = destination
        self.tx_gain = 10
        self.rx_gain = 10
        self.sat_load = 0.5
        self.speed = 15
        self.min_ele_angle = 10
        self.elevation_angle = self.compute_elevation_angle(source, data_lat, data_long, sec) # ok
        self.visible_time = self.compute_visible_time() # 
        self.distance = self.compute_distance(source, destination) # ok
        self.candidate_sat = self.find_candidate_sat() # ok
        self.SNR = self.compute_SNR() # ng
        self.is_covered = self.compute_covered(source, coverage, sec) # ok
        self.sec = sec

    def compute_distance(self, source, destination):
        lat1 = radians(source[0])
        lon1 = radians(source[1])
        lat2 = radians(destination[0])
        lon2 = radians(destination[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
    
    def find_candidate_sat(self):
        candidate_sat = []
        for satIndex, sec_and_angle in self.elevation_angle.items():
            sec, angle = sec_and_angle
            new_sec = sec
            if angle > self.min_ele_angle:
                if len(satIndex) == 3: # 2-1 to 2-9
                    tmp_angle = angle
                    while True:
                        new = str(satIndex).replace('-', '0')
                        fname = './data/satellite/Orbit_'+str(satIndex[0])+'/'+'Sat0'+new+'.csv'
                        df = pd.read_csv(fname, skiprows = new_sec,nrows = 15)
                        df_list = df.values.tolist()
                        # 計算最後一個15s的ele
                        # print(df_list[-1])
                        new_lat_long = (df_list[-1][0], df_list[-1][1])
                        pos_sat = new_lat_long
                        pos_airplane = self.source
                        distance = geodesic(pos_airplane, pos_sat).kilometers                    
                        result = math.atan(diff_H/distance)
                        tmp_angle = result*180/math.pi
                        if tmp_angle < self.min_ele_angle:
                            break
                        new_sec = new_sec + 15
                    candidate_sat.append((satIndex, new_sec-sec))
        return candidate_sat 

    def compute_SNR(self): #出來數字很怪 -> dB 
         # ((transmit power)*(attena Tx*Rx)*(rain)/(Boltz constant)*(system noise temperature)*(Bandwidth)) * (light v/(4*pi*dist*centering freq))
         res = ((1)*(41)*(-23)/(sc.Boltzmann*(300)*(20))) * ((300000/(4*math.pi*700*28))**2)
         return res
    
    def compute_visible_time(self):
        pass

    def queueing_delay(self):
        pass
    
    def compute_elevation_angle(self, source, sat_lat, sat_long, sec):
        sat_with_angle = {}
        for indexOfsat, info in sat_lat.items():
            try:
                position_satellite = (info, sat_long[indexOfsat])
                position_airplane = (source[0], source[1])
                distance = geodesic(position_airplane, position_satellite).kilometers                    
                result = math.atan(diff_H/distance)
            except: # divide by zero
                result = 0
            if result != 0:
                sat_with_angle[indexOfsat] = (sec, result*180/math.pi)

        return sat_with_angle # {'1-1': (Xs, 89.81308737155092), '1-2': (Xs, 9.376371137390949), ...}, X decide by input

    def compute_covered(self, source, coverage, sec):
        covered_sat = []
        pt = (source[0], source[1])
        for IndexOfSat, square in coverage.items():
            if self.is_in_coverage(square, pt) == True:
                covered_sat.append(IndexOfSat)
        return covered_sat

    def is_in_coverage(self, sq, pt):
        line = geometry.LineString(sq)
        point = geometry.Point(pt)
        pg = geometry.Polygon(line)
        return pg.contains(point)
