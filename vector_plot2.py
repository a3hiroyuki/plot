# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import calc_utils
import plot_utils

CUR_DIR = 'C:\\aaa\\'
START_TO_END_DISTANCE = 40.00

class TDataFactry():

    def __init__(self, path):
        plot_utils.init_param()
        self.df = pd.read_csv(path, dtype = 'object')
        self.angle_arr = self.df['dir'].values.astype('float')
        self.lat_arr = self.df['lat'].values.astype('float')
        self.lon_arr = self.df['lon'].values.astype('float')
        self.x_arr, self.y_arr = calc_utils.latlon2Coord(self.lat_arr, self.lon_arr, plot_utils.offset)
        self.angvector_arr = calc_utils.angle2angvector_arr(self.angle_arr)
        self.list = []

    def create(self, name = "none", start_points= [], end_points = []):
        start_point = max(start_points) + 1 #スタートポイントはとらない
        end_point = min(end_points)
        lat_arr = self.lat_arr[start_point:end_point]
        lon_arr = self.lon_arr[start_point:end_point]
        x_arr = self.x_arr[start_point:end_point]
        y_arr = self.y_arr[start_point:end_point]
        angvector_arr = self.angvector_arr[start_point:end_point]
        start_ave_point = calc_utils.calc_latlon_average(self.x_arr, self.y_arr, select_points = start_points)
        end_ave_vector= calc_utils.calc_latlon_average(self.x_arr, self.y_arr, select_points = end_points)
        t_data = TData(name, lat_arr, lon_arr, x_arr, y_arr, angvector_arr,start_ave_point , end_ave_vector)
        self.list.append(t_data)

    def get_item(self, num = 0):
        return self.list[num]

class TData:

    def __init__(self, name, lat_arr, lon_arr, x_arr, y_arr, angvector_arr, start_point, end_point):
        self.name = name
        self.lat_arr = lat_arr
        self.lon_arr = lon_arr
        self.x_arr = x_arr
        self.y_arr = y_arr
        self.start_point = start_point
        self.end_point = end_point
        self.unit_dir_vector = calc_utils.get_unit_dir_vector(start_point, end_point)

        self.angvector_arr = angvector_arr
        self.ave_angle, self.angle_unit_vector = calc_utils.calc_angle_average(angvector_arr)
        print (self.angle_unit_vector)

    def plot_position(self):
        start_to_end_dist = calc_utils.get_distance(self.start_point, self.end_point)
        dist_diff = START_TO_END_DISTANCE - start_to_end_dist
        print ("name：" + self.name)
        print ("誤差(距離)：" + str(dist_diff))
        print ("誤差(x)：" + str(dist_diff * self.unit_dir_vector[0]))
        print ("誤差(y)：" + str(dist_diff * self.unit_dir_vector[1]))
        plot_utils.plot_position(self.x_arr, self.y_arr, self.start_point, self.end_point, self.unit_dir_vector)

    def plot_direction(self):
        angle_diff = calc_utils.calc_angle_of_vctor(self.unit_dir_vector, self.angle_unit_vector)
        print ("name：" + self.name)
        print ("進行方向の角度：" + str(calc_utils.vector2angle(self.unit_dir_vector)))
        print ("平均角度：" + str(self.ave_angle))
        print ("進行方向との差:" + str(angle_diff))
        plot_utils.plot_direction(self.x_arr, self.y_arr, self.angvector_arr, self.start_point, self.end_point, self.unit_dir_vector)

    def make_json(self):
        plot_utils.make_json(self.lat_arr, self.lon_arr)

if __name__ == "__main__":
    f = TDataFactry(CUR_DIR + 'aaa.csv')
    f.create(name = "first",  start_points = [0,1], end_points = [5,6])
    f.create(name = "second",  start_points = [7,8], end_points = [12,13])
    f.get_item(0).plot_direction()
    f.get_item(1).plot_direction()
    f.get_item(1).make_json()
    #f.get_item(0).plot_googlemap()
