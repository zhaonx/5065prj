import pandas as pd
import re
import os

from math import radians, degrees, sin, cos, asin, acos, sqrt

rootdir = 'D:\\5065_data_handle\\results\\xlsx'
list = os.listdir(rootdir)

df_petrol = pd.read_csv('Petrol Station_WGS(1).csv')
column = ['ShapeID', 'id', 'name', 'type', 'address', 'wgs_lon', 'wgs_lat', 'point']
out_put_dic = {'ShapeID': [], 'id': [], 'name': [], 'type': [], 'address': [], 'wgs_lon': [], 'wgs_lat': [],
               'point': []}
loc_dic = {}
for index, rows in df_petrol.iterrows():
    loc_dic[rows['ShapeID']] = [rows['wgs_lon'], rows['wgs_lat']]
df_demand_point = pd.read_excel('all_out_put.xlsx')
demand_point_dic = {}
for index, rows in df_demand_point.iterrows():
    demand_point_dic[index] = [rows['lon'], rows['lat']]


def cal_score(dis, point):
    return float(point) / float(dis) ** 2


def great_circle(lon1, lat1, lon2, lat2):
    radius_of_earth = 63714  # meter6371393
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return radius_of_earth * (acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))


def get_drop_point_value(filename, k, all_point_list):
    petrol_score_dic = {}
    point_all = 0
    df = pd.read_excel(f"D:\\5065_data_handle\\results\\xlsx\\{filename}")
    chosen_loc = []
    distance_dic_demand_point = {}
    for index, rows in df.iterrows():
        if rows['FacilityType'] == 3:
            chosen_loc.append(rows['Name'])
    for loc_p in chosen_loc:
        for loc_d in demand_point_dic:
            distance = max(great_circle(loc_dic[loc_p][0], loc_dic[loc_p][1], demand_point_dic[loc_d][0],
                                        demand_point_dic[loc_d][1]), 5)
            if loc_d not in distance_dic_demand_point:
                distance_dic_demand_point[loc_d] = []
            distance_dic_demand_point[loc_d].append([loc_p, distance])
    # print(distance_dic_demand_point)
    for item in distance_dic_demand_point.keys():
        petrol_score_list = sorted(distance_dic_demand_point[item], key=lambda x: x[1])
        for index_ in range(k):
            score = cal_score(petrol_score_list[index_][1], 1)
            if int(petrol_score_list[index_][0]) not in petrol_score_dic:
                petrol_score_dic[int(petrol_score_list[index_][0])] = 0
            petrol_score_dic[int(petrol_score_list[index_][0])] += score
            point_all += score
    all_point_list.append([filename.split('.')[0], point_all])

    df_output = pd.DataFrame(columns=['ShapeID', 'point', 'lon', 'lat'])
    out_put_dic_inside = {'ShapeID': [], 'point': [], 'lon': [], 'lat': []}
    for i in petrol_score_dic:
        out_put_dic_inside['ShapeID'].append(i)
        out_put_dic_inside['point'].append(petrol_score_dic[i])
        out_put_dic_inside['lon'].append(loc_dic[i][0])
        out_put_dic_inside['lat'].append(loc_dic[i][1])
    for item in ['ShapeID', 'point', 'lon', 'lat']:
        df_output[item] = out_put_dic_inside[item]
    df_output.to_excel(f"D:/5065_data_handle/results/point-3/{filename.split('.')[0]}_point.xlsx")
    # print(all_point_list)
    return petrol_score_dic


# get_drop_point_value('07.xlsx',2,[])
all_point_list = []
for file in list:
    get_drop_point_value(file, 3, all_point_list)
df_all_compare = pd.DataFrame(columns=['num', 'point'])
out_put_dic_point = {'num': [], 'point': []}
for i in all_point_list:
    out_put_dic_point['num'].append(i[0])
    out_put_dic_point['point'].append(i[1])
for j in ['num', 'point']:
    df_all_compare[j] = out_put_dic_point[j]
df_all_compare.to_excel('final_score_3.xlsx')


#
# for index, rows in df_petrol.iterrows():
#     out_put_dic['ShapeID'].append(rows['ShapeID'])
#     out_put_dic['id'].append(rows['id'])
#     out_put_dic['name'].append(rows['name'])
#     out_put_dic['type'].append(rows['type'])
#     out_put_dic['address'].append(rows['address'])
#     out_put_dic['wgs_lon'].append(rows['wgs_lon'])
#     out_put_dic['wgs_lat'].append(rows['wgs_lat'])
#     out_put_dic['point'].append(point_dic[rows['ShapeID']])
#
# out_put_df = pd.DataFrame(columns=column)
# for item in column:
#     out_put_df[item] = out_put_dic[item]
#
# out_put_df.to_excel('simple_added.xlsx')
#
# import pandas as pd
#
# df_building = pd.read_csv('latlng_building.csv')
# df_postoffice = pd.read_csv('latlng_postoffice.csv')
# building_list, post_list = [], []
# for index, rows in df_building.iterrows():
#     building_list.append([rows['FID'], rows['lat'], rows['lng'], rows['final_sc']])
# for index, rows in df_postoffice.iterrows():
#     post_list.append([rows['FID'], rows['lat'], rows['lng']])
# post_score_dic = {}
# building_distence_dic = {}
# building_score_dic = {}
# for build in building_list:
#     building_distence_dic[build[0]] = []
#     lat_b = build[1]
#     lng_b = build[2]
#     final_sc = build[3]
#     for post in post_list:
#         lat_p = post[1]
#         lng_p = post[2]
#         distance = max(great_circle(lng_b, lat_b, lng_p, lat_p), 5)  # 500m
#         building_distence_dic[build[0]].append([post[0], distance, final_sc, lat_b, lng_b, lat_p, lng_p])
#
#
# def topk(building_distence_dic, k):
#     for item in building_distence_dic.keys():
#         building_score_dic[item] = 0
#         building_score_list = sorted(building_distence_dic[item], key=lambda x: x[1])
#         for index_ in range(k):
#             score = cal_score(building_score_list[index_][1], building_score_list[index_][2])
#             if building_score_list[index_][0] not in post_score_dic:
#                 post_score_dic[building_score_list[index_][0]] = 0
#             building_score_dic[item] += score
#             post_score_dic[building_score_list[index_][0]] += score
#
#
# topk(building_distence_dic, 2)
# for item in post_score_dic:
#     print(f"{item}: score = {post_score_dic[item]}")
# column = ['FID', 'score']
# ans_df1 = pd.DataFrame(columns=column)
# ans_df2 = pd.DataFrame(columns=column)
# ans_df1_dic = {'FID': [], 'score': []}
# ans_df2_dic = {'FID': [], 'score': []}
# for item in post_score_dic:
#     ans_df1_dic['FID'].append(item)
#     ans_df1_dic['score'].append(post_score_dic[item])
# for item in building_score_dic:
#     ans_df2_dic['FID'].append(item)
#     ans_df2_dic['score'].append(building_score_dic[item])
# for item in column:
#     ans_df1[item] = ans_df1_dic[item]
#     ans_df2[item] = ans_df2_dic[item]
# ans_df1.to_excel('post_score.xlsx')
# ans_df2.to_excel('building_score.xlsx')
