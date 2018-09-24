import numpy as np
import matplotlib.pyplot as plt
import calc_utils
import json

BASE_LATLON = [35.5553063, 139.7225792]
LEFT_BOTTOM = [35.55515,139.7218]
RIGHT_TOP = [35.5557,139.7228]
BULUDING_LAT = np.array([35.55561896421401,35.55536663092798,35.55516687208936, 35.55540556040712, 35.55561896421401])
BULUDING_LON = np.array([139.72205128744986,139.721954278491, 139.7226606675556, 139.72275596032546,139.72205128744986])

base_xy = [0, 0]
left_bottom_xy = [0, 0]
rigth_top_xy = [0, 0]
building_x = 0
building_y = 0
offset = [0, 0] #左下を0にする補正オフセット

#主に緯度経度を座標系に変換
def init_param():
    offset[0], offset[1] = calc_utils.latlon2Coord(LEFT_BOTTOM[0], LEFT_BOTTOM[1])
    left_bottom_xy[0], left_bottom_xy[1] = calc_utils.latlon2Coord(LEFT_BOTTOM[0], LEFT_BOTTOM[1], offset)
    base_xy[0], base_xy[1] = calc_utils.latlon2Coord(BASE_LATLON[0], BASE_LATLON[1], offset)
    rigth_top_xy[0], rigth_top_xy[1] = calc_utils.latlon2Coord(RIGHT_TOP[0], RIGHT_TOP[1], offset)
    global building_x, building_y
    building_x, building_y = calc_utils.latlon2Coord(BULUDING_LAT, BULUDING_LON, offset)

def make_json(lat_arr, lon_arr):
    json_data = []
    for i in range(len(lat_arr)):
        json_data.append({
            "name": str(i),
            "lat": lat_arr[i],
            "lng": lon_arr[i]})
    with open('data.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)

def plot_position(x_arr, y_arr, start_point, end_point, unit_dir_vector):
    plt.figure()
    plt.scatter(x_arr, y_arr)
    plot_common(start_point, end_point, unit_dir_vector)

def plot_direction(x_arr, y_arr, angvector_arr, start_point, end_point, unit_dir_vector):
    plt.figure()
    for i in range(len(angvector_arr)):
        plt.quiver(x_arr[i], y_arr[i],
                   angvector_arr[i][0], angvector_arr[i][1],angles='xy',scale_units='xy',scale=0.2)
    plot_common(start_point, end_point, unit_dir_vector)

def plot_common(start_point, end_point, unit_dir_vector):
    # グラフ表示
    plt.quiver(start_point[0], start_point[1], unit_dir_vector[0], unit_dir_vector[1],angles='xy',scale_units='xy',scale=0.2)
    plt.plot(np.array([start_point[0], end_point[0]]), np.array([start_point[1], end_point[1]]), marker="o", c='red')
    plt.plot(building_x, building_y)
    plt.xlim([left_bottom_xy[0],rigth_top_xy[0]])
    plt.ylim([left_bottom_xy[1] ,rigth_top_xy[1]])
    plt.xticks(np.arange(left_bottom_xy[0],rigth_top_xy[0], 20))
    plt.yticks(np.arange(left_bottom_xy[1] ,rigth_top_xy[1], 20))
    plt.draw()
    plt.show()