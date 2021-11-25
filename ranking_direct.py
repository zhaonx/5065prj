import pandas as pd
import re
import os

rootdir = 'D:\\5065_data_handle\\results\\xlsx'
list = os.listdir(rootdir)

df_petrol = pd.read_csv('Petrol Station_WGS(1).csv')
column = ['ShapeID', 'id', 'name', 'type', 'address', 'wgs_lon', 'wgs_lat', 'point']
out_put_dic = {'ShapeID': [], 'id': [], 'name': [], 'type': [], 'address': [], 'wgs_lon': [], 'wgs_lat': [], 'point': []}
point_dic = {}
for index, rows in df_petrol.iterrows():
    point_dic[rows['ShapeID']] = 0


def get_drop_point(filename, dic):
    df = pd.read_excel(f"D:\\5065_data_handle\\results\\xlsx\\{filename}")
    for index,rows in df.iterrows():
        dic[rows['Name']] += rows['DemandCount']


for file in list:
    get_drop_point(file,point_dic)

for index, rows in df_petrol.iterrows():
    out_put_dic['ShapeID'].append(rows['ShapeID'])
    out_put_dic['id'].append(rows['id'])
    out_put_dic['name'].append(rows['name'])
    out_put_dic['type'].append(rows['type'])
    out_put_dic['address'].append(rows['address'])
    out_put_dic['wgs_lon'].append(rows['wgs_lon'])
    out_put_dic['wgs_lat'].append(rows['wgs_lat'])
    out_put_dic['point'].append(point_dic[rows['ShapeID']])

out_put_df = pd.DataFrame(columns=column)
for item in column:
    out_put_df[item] = out_put_dic[item]

out_put_df.to_excel('simple_added.xlsx')