import os, sys
import csv
from ManipulateRoadPOI import *
from data.data import code_dict


# df_info_name = 'DF_Road_Info#440300.csv'


province = '广东省'
city = '深圳市'
region = '南山区'

def filtered_data(province, city, region):
    df = os.listdir('./data')
    df = [i for i in df if 'DF' in i]
    data_list = []
    # 选择指定城市
    if city != '全部':
        df_info_name = 'DF_Road_Info#' + code_dict[city] + '.csv'
        df_info = os.path.join('data', dir, df_info_name)
        df = load_df_csv(file=df_info)
        df_road_info = load_df_csv(file=df_info)    
        df_filtered = filter_df_column(df=df_road_info,columns=['name_road','name_district'])   # 仅选用道路信息和城市信息
        
        # 选择指定区县 
        if region != '全部':
            df_filtered = filter_df_keyword(df=df_filtered,column='name_district', keyword=region)

        temp_list = df_filtered.to_numpy().tolist()
        data_list.append(temp_list)
        return data_list

    # 偷懒，由于没有收集到全部省份的道路信息，所以只写简化的处理逻辑
    # 所有城市的道路信息
    else:
        for dir in df:
            df_road_info = load_df_csv(file=df_info)
            df_filtered = filter_df_column(df=df_road_info,columns=['name_road','name_district'])
            df_filtered = filter_df_keyword(df=df_filtered,column='name_district', keyword=region)
            

            temp_list = df_filtered.to_numpy().tolist()
            data_list.append(temp_list)
            
        return data_list