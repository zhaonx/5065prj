import pandas as pd
import re
import os

rootdir = 'D:\\5065_data_handle'
list = os.listdir(rootdir)


def get_drop_point(filename):
    hour = re.findall('time(.*?)\.csv', filename)[0]
    df = pd.read_csv(filename)
    status_dic = {}
    column = ['Lon', 'Lat', 'status_before', 'status_now', 'time']
    ans_df = pd.DataFrame(columns=column)
    ans_dic = {'Lon': [], 'Lat': [], 'status_before': [], 'status_now': [], 'time': []}
    for index, rows in df.iterrows():
        if rows['VEHICLEID'] not in status_dic:
            status_dic[rows['VEHICLEID']] = rows['STATE']
            continue
        if status_dic[rows['VEHICLEID']] == '重车' and rows['STATE'] == '空车':
            ans_dic['Lon'].append(rows['Lon'])
            ans_dic['Lat'].append(rows['Lat'])
            ans_dic['status_before'].append(status_dic[rows['VEHICLEID']])
            ans_dic['status_now'].append(rows['STATE'])
            ans_dic['time'].append(rows['TIME'])
        status_dic[rows['VEHICLEID']] = rows['STATE']

    for item in column:
        ans_df[item] = ans_dic[item]
    ans_df.to_csv(f'drop_point_results\\{hour}_drop_point.csv')
    print(f"{hour} finished")


for file in list:
    if 'h.csv' in file:
        get_drop_point(file)
