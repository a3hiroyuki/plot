# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from math import *
from PIL import Image
import pandas as pd

LEFT_BOTTOM = [139.72108336404472,35.55540011134171]
RIGHT_TOP = [139.72195508197456,35.555945639717535]

CUR_DIR = 'C:\\aaa\\'

df = pd.read_csv(CUR_DIR + 'aaa.csv', dtype = 'object')

print(np.array(df['lat'].values))

BIAS = 0.0001
# angles = np.array([10.0, 30.0, -10.0, -30.0])
# x_arr = np.array([0, 1, 2, 3], dtype='float') * BIAS + 139.7210
# y_arr = np.array([0, 1, 2, 3], dtype='float') * BIAS + 35.5554
angles = df['direction'].values.astype('float')
x_arr = df['lat'].values.astype('float') * BIAS + LEFT_BOTTOM[0]
y_arr = df['lon'].values.astype('float') * BIAS + LEFT_BOTTOM[1]
vectors = np.zeros((len(angles), 2))

print(angles)
print (x_arr)
print (y_arr)

ave_ang_x = 0.0
ave_ang_y = 0.0

for i, angle in enumerate(angles):
    angles_rad = angle * (pi / 180.0);
    ang_x = BIAS * cos(angles_rad);
    ang_y = BIAS * sin(angles_rad);
    vectors[i] = [ang_x, ang_y]

print (vectors)

for i in range(len(vectors)):
    ave_ang_x += vectors[i][0]
    ave_ang_y += vectors[i][1]

ave_ang_x = ave_ang_x / len(vectors)
ave_ang_y = ave_ang_y / len(vectors)

print (ave_ang_x)

plt.figure()

# 画像の読み込み
#img = np.array( Image.open('C:\\aaa\\map.png') )

# 画像の表示
#plt.imshow( img )

for i in range(len(vectors)):
# 矢印（ベクトル）
    plt.quiver(x_arr[i], y_arr[i],
               vectors[i][0],vectors[i][1],angles='xy',scale_units='xy',scale=1)

plt.quiver(0.005, 0.005,ave_ang_x,ave_ang_y,angles='xy',scale_units='xy',scale=1)

left = np.array([LEFT_BOTTOM[0] + 0.0003, LEFT_BOTTOM[0] + 0.0005])
height = np.array([LEFT_BOTTOM[1] + 0.0003, LEFT_BOTTOM[1] + 0.0005])
plt.plot(left, height, marker="o")
#plt.scatter(LEFT_BOTTOM[0] + 0.0003, LEFT_BOTTOM[1] + 0.0004)


# グラフ表示
plt.xlim([LEFT_BOTTOM[0],RIGHT_TOP[0]])
plt.ylim([LEFT_BOTTOM[1] ,RIGHT_TOP[1]])
plt.xticks(np.arange(139.72108336404472,139.72195508197456,0.0001))
plt.yticks(np.arange(35.55540011134171 ,35.555945639717535,0.0001))
#plt.grid()
plt.draw()
plt.show()


def CAL_PHI(ra,rb,lat):
    return atan(rb/ra*tan(lat))

def CAL_RHO(Lat_A,Lon_A,Lat_B,Lon_B):
    ra=6378.140  # equatorial radius (km)
    rb=6356.755  # polar radius (km)
    F=(ra-rb)/ra # flattening of the earth
    rad_lat_A=radians(Lat_A)
    rad_lon_A=radians(Lon_A)
    rad_lat_B=radians(Lat_B)
    rad_lon_B=radians(Lon_B)
    pA=CAL_PHI(ra,rb,rad_lat_A)
    pB=CAL_PHI(ra,rb,rad_lat_B)
    xx=acos(sin(pA)*sin(pB)+cos(pA)*cos(pB)*cos(rad_lon_A-rad_lon_B))
    c1=(sin(xx)-xx)*(sin(pA)+sin(pB))**2/cos(xx/2)**2
    c2=(sin(xx)+xx)*(sin(pA)-sin(pB))**2/sin(xx/2)**2
    dr=F/8*(c1-c2)
    rho=ra*(xx+dr)
    return rho