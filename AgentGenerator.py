from math import sin, cos, sqrt, atan2, radians
from SatGenerator import SatGenerator, Satellite
import scipy.constants as sc
import math
from geopy.distance import geodesic
from shapely import geometry

R = 6373.0
H = 610
Airplane_H = 10
diff_H = H - Airplane_H

class Agent:
    def __init__(self, number, source, destination, data_lat, data_long, coverage):
        self.number = number
        self.source = source
        self.destination = destination
        self.Tx = 10
        self.Rx = 10
        self.sat_load = 0.5
        self.speed = 15
        self.min_ele_angle = 10
        self.elevation_angle = self.compute_elevation_angle(source, data_lat, data_long) # ok
        self.visible_time = self.compute_visible_time() # 
        self.distance = self.compute_distance(source, destination) # ok
        self.candidate_sat = self.find_candidate_sat() # ok
        self.SNR = self.compute_SNR() # ng
        self.is_covered = self.compute_covered(source, coverage) # ok

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
        for SatIndex, angle in self.elevation_angle.items():
            if angle > self.min_ele_angle:
                candidate_sat.append(SatIndex)
        return candidate_sat 

    def compute_SNR(self): #出來數字很怪 -> dB 
         # ((transmit power)*(attena Tx*Rx)*(rain)/(Boltz constant)*(system noise temperature)*(Bandwidth)) * (light v/(4*pi*dist*centering freq))
         res = ((1)*(41)*(-23)/(sc.Boltzmann*(300)*(20))) * ((300000/(4*math.pi*700*28))**2)
         return res
    
    def compute_visible_time(self):
        pass

    def queueing_delay(self):
        pass
    
    def compute_elevation_angle(self, source, sat_lat, sat_long):
        
        sat_ele_angle = {}
        for IndexOfSat, info in sat_lat.items():
            try:
                position_satellite = (info, sat_long[IndexOfSat])
                position_airplane = (source[0], source[1])
                distance = geodesic(position_airplane, position_satellite).kilometers                    
                result = math.atan(diff_H/distance)
            except: # divide by zero
                result = 0
                #print(f'對第{IndexOfSat}顆衛星第{s}sec的angle: {result*180/math.pi}')
            if result*180/math.pi:
                sat_ele_angle[IndexOfSat] = result*180/math.pi

        return sat_ele_angle

    def compute_covered(self, source, coverage):
        covered_sat = []
        pt = (source[0], source[1])
        for IndexOfSat, square in coverage.items():
            if self.in_square(square, pt) == True:
                covered_sat.append(IndexOfSat)
        return covered_sat

    def in_square(self, sq, pt):
        line = geometry.LineString(sq)
        point = geometry.Point(pt)
        pg = geometry.Polygon(line)
        return pg.contains(point)
