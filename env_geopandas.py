import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from cartopy import crs as ccrs
import geodatasets
import numpy as np

# 緯          經
# 12.097686, -68.908109
# -2.92674, -59.99778
# -31.2507, 136.80107
# 48.34525,-116.43933333333334

bs_path = 'gw_positions.txt'
bs_y = []
bs_x = []
with open(bs_path) as f:
    for line in f.readlines():
        s = line.split(' ')
        bs_x.append(float(s[0]))
        bs_y.append(float(s[1]))
f.close()

worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
worldmap.plot(color="lightgrey")
plt.scatter(bs_y, bs_x, s=5, marker='o', c='r')
plt.show()
