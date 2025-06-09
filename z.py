import os, sys
import csv
from ManipulateRoadPOI import *
from data.data import code_dict
import pandas as pd

# df_info_name = 'DF_Road_Info#440300.csv'


province = '广东省'
city = '深圳市'
region = '南山区'

data_list = [['广东省', '深圳市'],['广东省', '广州市']]
data = pd.DataFrame(data_list,columns=['省','市'])