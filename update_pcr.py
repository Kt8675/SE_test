# 更新 省-市-区 分划的python文件
import csv
import pandas as pd
import json

file = './AMap_adcode_citycode.xlsx'
df = pd.read_excel(file)


# print(df.keys())
# print(df['中文名'])
# print(df['adcode'])
# print(df['citycode'])
l = len(df)
# print(l)
list_province = []
dict_city = {}
dict_region = {}
code_dict ={}
city_code_dict = {}

province = '北京市'
city =  '北京市'
region = None
for i in range(1, l):
    # print(df['adcode'][i], df['citycode'][i], df['中文名'][i])
    
    if df['adcode'][i] % 10000 == 0:    # 省、直辖市或特别行政区
        province = df['中文名'][i]
        list_province.append(province)
        dict_city[province] = []
        code_dict[df['中文名'][i]] = int(df['adcode'][i])
        if '市' in province or '行政区' in province:
            city = province
            dict_city[province] = []
            dict_region[province] = []
            city_code_dict[df['adcode'][i]] = df['中文名'][i]
    elif df['adcode'][i] % 100 == 0:     # 市
        city = df['中文名'][i]
        dict_region[city] = []
        dict_city[province].append(city)
        code_dict[df['中文名'][i]] = int(df['adcode'][i])
        city_code_dict[df['adcode'][i]] = df['中文名'][i]
    else:                               # 区
        region = df['中文名'][i]
        # dict_region[region] = city
        dict_region[city].append(region)
        
with open('data.txt', 'w', encoding='utf-8') as f:
    f.write(str(list_province)+'\n')
    f.write(str(dict_city)+'\n')
    f.write(str(dict_region)+'\n')
    f.write(str(code_dict)+'\n')
    f.write(str(city_code_dict))

# with open('data.json', 'w', encoding='utf-8') as json_file:
    # json.dump(json_data, json_file, indent=4)