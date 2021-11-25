import pandas as pd
import re
import os

rootdir = 'D:\\5065_data_handle\\drop_excel\\drop_point_results'
list = os.listdir(rootdir)
column = ['lon', 'lat', 'time']
out_put_dic = {'lon': [], 'lat': [], 'time': []}
for path in list:
    df = pd.read_excel(f"{rootdir}\\{path}")
    for index, rows in df.iterrows():
        out_put_dic['lon'].append(rows['Lon'])
        out_put_dic['lat'].append(rows['Lat'])
        out_put_dic['time'].append(rows['time'])
out_put_df = pd.DataFrame(columns=column)
for item in column:
    out_put_df[item] = out_put_dic[item]
out_put_df.to_excel('all_out_put.xlsx')
