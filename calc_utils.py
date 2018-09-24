import pyproj
import math
import numpy as np

#平面直角座標系への変換
def latlon2Coord(lat_arr, lon_arr, offset = [0, 0]):
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")
    x_arr, y_arr = pyproj.transform(EPSG4612, EPSG2451, lon_arr, lat_arr)
    return x_arr - offset[0], y_arr - offset[1]

#360度角度を角度ベクトルへ変換
def angle2angvector_arr(angles):
    angvector_arr =  np.zeros((len(angles), 2))
    for i, angle in enumerate(angles):
        angles_rad = angle * (math.pi / 180.0);
        ang_x = math.cos(angles_rad);
        ang_y = math.sin(angles_rad);
        angvector_arr[i] = [ang_x, ang_y]
    return angvector_arr

#角度の平均値を算出
def calc_angle_average(angvector_arr):
    ave_ang_vec = np.average(angvector_arr, axis = 0)
    ave_ang =vector2angle(ave_ang_vec);
    return ave_ang, ave_ang_vec

def vector2angle(vector):
    ang = math.atan2(vector[1], vector[0]);
    return ang * 180/math.pi


def calc_latlon_average(x_arr,  y_arr,  select_points = []):
    select_arr_x = np.zeros((len(select_points), 1))
    select_arr_y = np.zeros((len(select_points), 1))
    for i in range(len(select_points)):
        select_arr_x[i] = x_arr[select_points[i]]
        select_arr_y[i] = y_arr[select_points[i]]
    return np.array([np.average(select_arr_x), np.average(select_arr_y)])

def get_unit_dir_vector(start_point, end_point):
    vector = end_point - start_point
    lenght = calc_vector_length(vector)
    return np.array([vector[0]/lenght, vector[1]/lenght])

def get_distance(start_point, end_point):
    return calc_vector_length(end_point - start_point)

def calc_angle_of_vctor(vector1, vector2):
    cos_shita = np.dot(vector1, vector2)/calc_vector_length(vector1) * calc_vector_length(vector2)
    angle = math.acos(cos_shita)
    return angle * 180/math.pi

def calc_vector_length(vector):
    return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])