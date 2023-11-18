import numpy as np
from SatGenerator import SatGenerator
from AgentGenerator import Agent


if __name__ == '__main__':
    S = [52, 140] # [-56.1980567,-178.4860009] 
    D = [59.94888889, -151.6922222]

    OrbitList = []
    Orbit_1 = SatGenerator(1)
    OrbitList.append(Orbit_1)
    Orbit_2 = SatGenerator(2)
    OrbitList.append(Orbit_2)
    # Orbit_3 = SatGenerator(3)
    # OrbitList.append(Orbit_3)
    # Orbit_4 = SatGenerator(4)
    # OrbitList.append(Orbit_4)
    # Orbit_5 = SatGenerator(5)
    # OrbitList.append(Orbit_5)
    # Orbit_6 = SatGenerator(6)
    # OrbitList.append(Orbit_6)
    # Orbit_7 = SatGenerator(7)
    # OrbitList.append(Orbit_7)
    # Orbit_8 = SatGenerator(8)
    # OrbitList.append(Orbit_8)

    data_lat = {}
    data_long = {}
    data_coverage = {}
    IndexOfOrbit = 1
    sec = int(input("看第幾秒: ")) # 有第0秒(衛星起始位置)

    for orb in OrbitList:
        orb.GenerateOrbit()
        for IndexOfSat,v in orb.GetSatInfo().items():
            index = str(IndexOfOrbit)+'-'+str(IndexOfSat)
            data_lat[index] = v.sat_lat[sec] # 上一版是傳一個list看n到k秒，之後會是iteration所以改成看特定秒
            data_long[index] = v.sat_long[sec]
            data_coverage[index] = v.coverage[sec]
        IndexOfOrbit = IndexOfOrbit + 1

    Airplane_1 = Agent(1, S, D, data_lat, data_long, data_coverage) 

    #print(Airplane_1.elevation_angle) # {'1-1': 16.369005141803093, '1-2': 17.05518920757602, ... }
    print(f"航線{Airplane_1.number}第{sec}秒的候選衛星: {Airplane_1.candidate_sat}")
    print(f"被哪些衛星覆蓋: {Airplane_1.is_covered}")
