import json
import pandas as pd
import random
import time
import os
import sys
import requests
from sklearn.cluster import KMeans
import re

# 道路类型字典（道路名称中可能出现的类型定义分词映射至其可能所属的道路类型，其中键大致按照后缀顺序排列，保证先出现的路名分词不是后出现的路面分词的后缀）
DICT_TYPE_ROAD={
    r"高速":"高速公路",
    r"快速":"城市快速路",
    r"高速路":"高速公路",
    r"快速路":"城市快速路",
    r"公路":"普通公路",
    r"支路":"支路",
    r"辅路":"辅路",
    r"路":"一般市政道路",

    r"立交桥":"立交桥",
    r"高架桥":"高架桥",
    r"跨线桥":"跨线桥",
    r"跨铁路桥":"跨铁路桥",
    r"水库桥":"水库桥",
    r"通道桥":"通道桥",
    r"特大桥":"特大桥",
    r"大桥":"大桥",
    r"中桥":"中桥",
    r"小桥":"小桥",
    r"天桥":"天桥",
    r"桥":"一般桥梁",
    r"立交":"立交桥",
    r"高架":"高架桥",
    r"桥涵":"涵洞桥梁",
    r"隧道":"隧道",

    r"国道":"国道",
    r"省道":"省道",
    r"县道":"县道",
    r"乡道":"乡道",
    r"村道":"村道",
    r"通道":"通道",
    r"干道":"干道",
    r"大道":"大道",
    r"绿道":"绿道",
    r"辅道":"辅道",
    r"匝道":"匝道",
    r"栈道":"栈道",
    r"联络道":"联络道",
    r"连接道":"连接道",
    r"巡逻道":"巡逻道",
    r"骑行道":"骑行道",
    r"道":"一般市政道",

    r"商业步行街":"商业步行街",
    r"商业.街":"商业街",
    r"商业街":"商业街",
    r"工业.街":"工业街",
    r"工业街":"工业街",
    r"商住街":"商住街",
    r"步行街":"步行街",
    r"市场街":"市场街",
    r"文化街":"文化街",
    r"美食街":"美食街",
    r"中心街":"中心街",
    r"大街":"大街",
    r"街":"一般市政街",

    r"环线":"环线",
    r"干线":"干线",
    r"支线":"支线",
    r"连接线":"连接线",
    r"联接线":"联接线",
    r"线":"一般连线",

    r"工业区":"工业区",
    r"停车区":"停车区",
    r"新区":"新区",
    r"社区":"社区",
    r"区":"一般区",

    r"巷":"一般巷",
    r"段":"段",
    r"坊":"坊",
    r"村":"村",
    r"径":"径",
    r"坑":"坑",
    r"里":"里",
    r"横":"横",
    r"围":"围",
    r"岗":"岗",
    r"互通":"互通"
}
# 特殊道路类型映射字典（用于识别以特定含义的字母开头的道路：国、省、县、乡、村道）
DICT_TYPE_WAY={
    "G":"国道",
    "S":"省道",
    "X":"县道",
    "Y":"乡道",
    "C":"村道"
}

CITY=None   # 待查询的城市行政区划代码（限制必须为市级行政区）（必须由命令行参数提供，否则程序报错退出）
DATA_PATH=None  # 当前城市的道路和行政区划数据存储文件父级路径（非必要命令行参数，程序将可执行文件所在自身目录作为默认目录）
AMAP_KEY_ID=None    # 高德地图API调用密钥（非必要命令行参数，程序提供默认密钥）
DF_ADCODE=None  # 全中国行政区划代码表格（必要文件，必须和程序的可执行文件存储在相同目录下）
try:
    DF_ADCODE=pd.read_excel(io=f"./AMap_adcode_citycode.xlsx",sheet_name=0,dtype=str,engine="openpyxl")    # 从XLSX文件读取全中国行政区划代码表格
    if list(DF_ADCODE.columns)!=["中文名","adcode","citycode"]:
        sys.stderr.write(f"Corrupted Necessary File: \"./AMap_adcode_citycode.xlsx\"\n")
        sys.exit(1)
except FileNotFoundError:
    sys.stderr.write(f"Missing Necessary File: \"./AMap_adcode_citycode.xlsx\"\n{FileNotFoundError}\n")
    sys.exit(1)

sys_argv=sys.argv   # 获取程序命令行参数（不考虑第一个命令行参数，即程序的可执行文件自身，下同）
if len(sys_argv)<=1:    # 若程序在命令行运行时无额外参数提供则报错退出（至少需要输入必需的待获取道路信息的城市的行政区划代码）
    sys.stderr.write(f"Missing Necessary Argument: AD-Code of Target City (\"XXXX00\")\n")
    sys.exit(2)
else:
    try:    # 使用异常处理控制结构以捕获命令行参数解析时预期可能发生的错误（下同）
        arg_city=str(int(sys_argv[1]))  # # 解析程序第一个命令行参数（两次类型转换用于检查参数格式是否为数字）
        if arg_city in {"110000","120000","310000","500000"}:   # 若输入参数表示直辖市则将其行政区划代码（实际为省级）转换为对应城区的市级行政区划代码
            CITY=str(int(arg_city)+100) # 命令行参数赋值给程序全局参数（下同）
        elif (arg_city in {"110100","120100","310100","500100","500200"}
            or (arg_city in set(DF_ADCODE["adcode"]) and int(arg_city)%100==0 and int(arg_city)%10000!=0)): # 检查命令行参数是否对应某一城市都行政区划代码
            CITY=arg_city
        else:   # 上述检查不满足条件则说明命令行参数格式正确但取值错误，程序报错退出
            sys.stderr.write(f"Erroneous Argument Value: AD-Code of Target City (\"{arg_city}\")\n")
            sys.exit(2)
    except ValueError:  # 上述检查中捕获类型转换错误则说明命令行参数格式错误，程序报错退出
        sys.stderr.write(f"Erroneous Argument Format: AD-Code of Target City\n{ValueError}\n")
        sys.exit(2)
try:    # 尝试解析第二个命令行参数作为程序数据存储文件的父级路径（需要检查参数自身是否存在以及参数对应路径是否存在）
    DATA_PATH=f"{sys.argv[2]}/Data_Info#{CITY}/" if os.path.exists(f"{sys.argv[2]}") else f"./Data_Info#{CITY}/"
except IndexError:  # 若解析第二个命令行参数捕获数组越界错误则说明命令行实际并未提供第二个参数，此时设置数据存储文件的默认父级路径
    DATA_PATH=f"./Data_Info#{CITY}/"
try:    # 尝试解析第三个命令行参数作为程序调用高德地图API的密钥
    AMAP_KEY_ID=sys.argv[3]
except IndexError:  # 若解析第三个命令行参数捕获数组越界错误则说明命令行实际并未提供第三个参数，此时设置默认密钥
    AMAP_KEY_ID=f"e8a1fd2d4525c1b35838fee0deaa41ec"

print(f"\nCITY:\t{CITY}\nDATA_PATH:\t{DATA_PATH}\nAMAP_KEY_ID:\t{AMAP_KEY_ID}\nDF_ADCODE:\n{DF_ADCODE}\n")  # 控制台输出显示程序全局参数以确认程序运行配置
if not os.path.exists(f"{DATA_PATH}"):  # 检查上述指定的当前城市数据的存储文件夹是否存在，若不存在则创建之
    os.makedirs(f"{DATA_PATH}")
if not os.path.exists(f"{DATA_PATH}/JSON_Road"):    # 若不存在则创建当前城市原始道路数据（JSON文件）的存储文件夹
    os.makedirs(f"{DATA_PATH}/JSON_Road")



# 高德地图Web-API请求获取指定城市的行政区划信息（精确到城市-区县-街道的3级行政区划结构）
def request_ad(key:str,adcode_city:str):    # 字符串传入参数key指定API调用密钥、adcode_city指定待查询城市的行政区划代码
    time.sleep(0.4) # 每次查询前程序暂停0.4秒以满足高德地图API的并发查询QPS上限限制
    api_response=requests.get(  # 调用Web-API查询传入参数指定城市的行政区划信息
        url=f"https://restapi.amap.com/v3/config/district", # API调用的http请求命令本体
        params={    # http请求的参数字典，上述get函数中自动拼接为完整的http请求命令
            "key":key,  # 传入API调用密钥
            "output":"json",    # 指定响应数据格式为json文件
            "keywords":adcode_city, # 传入待查询参数的行政区划代码作为查询关键词
            "filter":adcode_city,   # 传入待查询参数的行政区划代码作为查询过滤器（限制仅返回指定区域下辖的行政区划信息）
            "subdistrict":3,    # 指定返回的行政区划信息粒度至少达到3级子行政区（城市-区县-街道，若待查询城市无区县级行政区则为城市-街道）
            "offset":20,    # 指定响应数据最外层每一页至多包含20条数据（不限制每一条数据内部的子数据数量）
            "page":1,   # 指定查询第一分页（指定城市的行政区划查询其响应数据数量有限，请求第一分页查询一次即可）
            "extensions":"base" # 指定响应数据仅包含基本字段（不包含行政区划的边界坐标点）
        })
    if api_response.status_code!=200 or api_response.json().get("count","0")=="0":  # 检查响应数据状态代码和返回的数据条数是否正常
        print(f"Request Ad-Info Failure Response: {api_response.status_code}#{api_response.text}")
        return dict()   # 若查询请求出现任何形式的异常结果则返回空字典以表示查询失败
    else:
        print(f"Request Ad-Info Success Response: {api_response.text}")
        return api_response.json().get("districts",[dict()])[0] # 若查询请求成功得到正常结果则返回JSON数据解析得到的“城市级行政区”字典数据结构
# 获取行政区划信息原始数据（Web-API返回的JSON文件响应数据）并解析生成格式化表格数据（关系型表格模式、dataframe数据结构、csv文件格式）
def get_parse_ad_info(key:str,adcode_city:str): # 字符串传入参数key指定API调用密钥、adcode_city指定待获取行政区划信息的城市的行政区划代码
    dict_city=request_ad(key=key,adcode_city=adcode_city)  # 调用高德地图API查询获取指定城市的完整行政区划信息的字典数据结构
    if not dict_city:   # 预先检查Web-API查询返回的结果是否为空（异常处理）
        return
    list_ad_info=list()  # 预先创建行政区划表格的数据临时存储列表（后续转换成dataframe数据结构）
    df_column_label=list()  # 预先创建行政区划表格的dataframe数据结构的表头列标签列表
    if dict_city["districts"][0]["level"]=="district":  # 检查待解析城市的行政区划结构类型（3级：城市-区县-街道，或者2级：城市-街道）
        df_column_label.extend(["towncode","township","location_town","adcode_district","name_district","location_district","adcode_city","citycode","name_city","location_city"])  # 若待解析城市为3级行政区划结构则据此设置其dataframe数据结构的表头列标签
        list_district=dict_city.get("districts",list()) # 获取当前城市下辖全部区县级行政区信息的列表-字典数据结构
        for dict_district in list_district: # 遍历每一个区县级行政区信息字典
            list_street=dict_district.get("districts",list())   # 获取当前区县下辖全部街道级行政区信息的列表-字典数据结构
            for dict_street in list_street: # 遍历每一个街道级行政区信息字典
                list_ad_info.append([   # 将街道级行政区的信息添加进入指定城市的行政区划信息列表（与字典-列表数据结构相反的信息组织方式，遵循数据库关系型表格的数据组织结构）
                    f"{dict_district.get("adcode","#")}000000", # 街道（级行政区）的12位行政区划代码（尚未实际获取，此处仅作为占位符）
                    dict_street.get("name","#"),    # 街道的名称
                    dict_street.get("center","#"),  # 街道的中心坐标
                    dict_district.get("adcode","#"),    # 区县（级行政区）的6位行政区划代码
                    dict_district.get("name","#"),  # 区县的名称
                    dict_district.get("center","#"),    # 区县的中心坐标
                    dict_city.get("adcode","#"),    # 城市（级行政区）的6位行政区划代码
                    dict_city.get("citycode","#"),  # 城市的电话号码前缀
                    dict_city.get("name","#"),  # 城市的名称
                    dict_city.get("center","#")])   # 城市的中心坐标
    else:   # 若待解析城市为2级行政区划结构则首先据此设置其dataframe数据结构的表头列标签
        df_column_label.extend(["towncode","township","location_town","adcode_city","citycode","name_city","location_city"])
        list_street=dict_city.get("districts",list())   # 获取当前城市直接下辖全部街道级行政区信息的列表-字典数据结构
        for dict_street in list_street: # 遍历每一个街道级行政区信息字典
            list_ad_info.append([   # 将街道级行政区的信息添加进入待解析城市的行政区划信息列表
                f"{dict_city.get("adcode","#")}000000", # 街道（级行政区）的12位行政区划代码（尚未实际获取，此处仅作为占位符）
                dict_street.get("name","#"),    # 街道（级行政区）的名称
                dict_street.get("center","#"),  # 街道的中心坐标
                dict_city.get("adcode","#"),    # 城市（级行政区）的6位行政区划代码
                dict_city.get("citycode","#"),  # 城市的电话号码前缀
                dict_city.get("name","#"),  # 城市的名称
                dict_city.get("center","#")])   # 城市的中心坐标
    df_ad_csv=pd.DataFrame(data=list_ad_info,columns=df_column_label,dtype=str,copy=True)  # 根据上述解析存储的城市行政区划信息列表和对应表头列标签创建dataframe数据结构
    df_ad_csv.sort_values(by=(["adcode_district","location_town"] if "adcode_district" in df_ad_csv.columns else "location_town"),ascending=True,inplace=True,ignore_index=True)  # 根据街道级行政区的中心坐标和其所属区县的6位行政区划代码（若有）排序表格数据
    df_ad_csv.to_csv(path_or_buf=f"{DATA_PATH}DF_AD_CSV#{adcode_city}.csv",sep="\t",index=False,columns=None,encoding="utf-8")    # 将行政区划信息表格（dataframe数据结构，暂不包含街道的行政区划代码）存储至csv文件（指定\t作为行内分隔符）
    print(f"\n\n{df_ad_csv}\nParse Result: Administrative Division Information Dataframe{df_ad_csv.shape}")   # 输出显示行政区划信息表格，表示指定城市的行政区划信息解析成功完成
# 高德地图Web-API请求获取指定城市区县（或城市）的部分主要道路信息（关键词搜索）
def request_road(key:str,adcode_district:str):  # 字符串传入参数key指定API调用密钥、adcode_district指定待查询区县的行政区划代码
    page_num=0  # 辅助计数变量，指示当前请求查询的分页编号
    list_road=list()    # 存储主要道路信息字典的列表数据结构（临时）
    while True: # 循环执行相同参数不同分页的Web-API查询请求
        time.sleep(0.4) # 每一循环中程序暂停0.4秒以满足高德地图API的并发查询QPS上限限制
        page_num+=1 # 自增分页编号
        api_response=requests.get(  # 调用Web-API查询传入参数指定区县的部分主要道路信息
            url=f"https://restapi.amap.com/v5/place/text",  # API调用的http请求命令本体
            params={    # http请求的参数字典，上述get函数中自动拼接为完整的http请求命令
                "key":key,  # 传入API调用密钥
                "output":"json",    # 指定响应数据格式为json文件
                "types":"190301",   # 使用类型代码指定查询的地点类型为道路名称
                "city":adcode_district, # 指定待查询的地理范围为指定区县（或城市，如果指定城市无区县级行政区）
                "city_limit":"true",    # 限制查询仅返回指定区县下辖的道路信息
                "page_size":20, # 指定响应数据每一页至多包含20条数据
                "page_num":page_num,    # 指定当前查询的分页数
                "show_fields":"children"    # 指定响应数据包含地点的子地点信息（若有）
            })
        if api_response.status_code!=200:   # 检查响应数据状态代码是否正常（若失败则中断退出循环）
            print(f"Request Road-Info#{adcode_district} Failure Response: {api_response.status_code}#{api_response.text}")
            break
        else:
            print(f"Request Road-Info#{adcode_district} Success Response#{page_num}: {api_response.text}")
            page=api_response.json().get("pois",list()) # 当前查询成功时获取响应数据中当前分页（最多20条）的道路信息列表-字典数据结构
            if len(page)>=1:    # 若当前分页的道路信息列表-字典数据结构非空则说明当前相同参数的查询仍存在下一分页，此时将当前分页添加进入主要道路信息列表并继续循环
                list_road.extend(page)
                continue
            else:   # 若当前分页的道路信息列表-字典数据结构为空则说明当前相同参数的查询已经结束，此时正常中断退出循环
                break
    return list_road    # 函数最终返回主要道路信息列表（列表-字典数据结构），供上级函数写入至文件以及为后续“周边搜索”查询请求提供坐标数据
# 高德地图Web-API请求获取指定城市内部指定坐标附近的部分地点信息（周边搜索）
def request_vicinity(key:str,adcode_city:str,coordinate:str,poi_type:str):  # 字符串传入参数key指定API调用密钥、adcode_city指定查询限制城市的行政区划代码、coordinate指定待查询地点的坐标
    page_num=0  # 辅助计数变量，指示当前请求查询的分页编号
    list_vicinity=list()    # 存储周边地点信息字典的列表数据结构（临时）
    while True: # 循环执行相同参数不同分页的Web-API查询请求
        time.sleep(0.4) # 每一循环中程序暂停0.4秒以满足高德地图API的并发查询QPS上限限制
        page_num+=1 # 自增分页编号
        api_response=requests.get(  # 调用Web-API查询传入参数指定坐标附近的部分地点信息
            url=f"https://restapi.amap.com/v5/place/around",    # API调用的http请求命令本体
            params={    # http请求的参数字典，上述get函数中自动拼接为完整的http请求命令
                "key":key,  # 传入API调用密钥
                "output":"json",    # 指定响应数据格式为json文件
                "types":poi_type,   # 传入参数使用类型代码指定查询的地点类型（道路/桥梁/隧道）
                "location":coordinate,  # 指定待查询地点的坐标
                "region":adcode_city,   # 限制待查询的地理范围为指定城市辖区内部（或城市，如果指定城市无区县级行政区）
                "city_limit":"true",    # 限制查询仅返回指定城市下辖的地点信息
                "radius":4000,  # 指定查询周边的范围（圆形半径，单位为米）
                "sortrule":"distance",  # 指定响应数据按照到传入参数指定坐标的距离由近及远排序
                "page_size":20, # 指定响应数据每一页至多包含20条数据
                "page_num":page_num,    # 指定当前查询的分页数
                "show_fields":"children"    # 指定响应数据包含地点的子地点信息（若有）
            })
        if api_response.status_code!=200:   # 检查响应数据状态代码是否正常（若失败则中断退出循环）
            print(f"Request Vicinity-Info#{coordinate} Failure Response: {api_response.status_code}#{api_response.text}")
            break
        else:
            print(f"Request Vicinity-Info#{coordinate} Success Response#{page_num}: {api_response.text}")
            page=api_response.json().get("pois",list()) # 当前查询成功时获取响应数据中当前分页（最多20条）的地点信息列表-字典数据结构
            if len(page)>=1:    # 若当前分页的地点信息列表-字典数据结构非空则说明当前相同参数的查询仍存在下一分页，此时将当前分页添加进入周边地点信息列表并继续循环
                list_vicinity.extend(page)
                continue
            else:   # 若当前分页的地点信息列表-字典数据结构为空则说明当前相同参数的查询已经结束，此时正常中断退出循环
                break
    return list_vicinity    # 函数最终返回周边地点信息列表（列表-字典数据结构），供上级函数写入至文件
# 高德地图Web-API第一次查询指定城市下辖的全部道路信息（内部封装request_road和request_vicinity函数）
def get_road_info(key:str,adcode_city:str): # 字符串传入参数key指定API调用密钥、adcode_city指定待查询城市的行政区划代码
    list_adcode_district=list(filter(   # 从全中国行政区划代码表格获取传入参数指定城市下辖的全部区县级行政区划代码，形成列表数据结构
        lambda adcode:adcode.startswith(str(int(int(adcode_city)/100))) and not adcode.endswith("00"),DF_ADCODE["adcode"]))
    # list_adcode_district=[] # 程序调试使用，可手动单独指定仅查询城市下辖某些行政区的道路信息
    list_file=os.listdir(path=f"{DATA_PATH}/JSON_Road/")    # 打开指定城市数据目录下存储原始道路数据的子文件夹并列出全部下属文件
    if len(list_adcode_district)<=0:    # 检查指定城市的行政区划类型（城市-区县-街道或者城市-街道）
        list_street_road=request_road(key=key,adcode_district=adcode_city)  # 若指定城市为2级行政区划则首先查询得到城市下辖部分主要道路信息，从函数返回值获取原始道路信息的列表-字典数据结构
        json.dump(  # 将主要道路信息列表写入指定文件（及时保存以避免程序中途出错导致的数据丢失，下同）
            obj=list_street_road,   # 指定写入文件的目标数据为主要道路信息列表（列表-字典数据结构，包含指定区县或城市的部分主要道路信息）
            fp=open(file=f"{DATA_PATH}/JSON_Road/KeyWord#{adcode_city}.json",mode="w",encoding="utf-8"),    # 指定存储文件带路径的完整名称，下同
            indent=4,
            skipkeys=False,
            ensure_ascii=False,
            check_circular=True,
            allow_nan=True,
            cls=None,
            separators=(",",":"),
            default=None,
            sort_keys=False)
        for dict_road in list_street_road:  # 遍历城市下辖每一条主要道路
            if f"Vicinity#{dict_road.get("location","-").replace(".","").replace(",","")}.json" not in list_file:   # 防止重复写入文件（配合上述可复现的关键词道路信息列表，可实现程序意外错误中断后重新运行而不重复写入已经保存的文件）
                list_vicinity=request_vicinity(key=key,adcode_city=adcode_city,coordinate=dict_road.get("location","113.926687,22.485890"),poi_type="190301")   # 查询每一条主要道路周边的部分道路信息
                json.dump(  # 将周边道路信息列表写入指定文件
                    obj=list_vicinity,  # 指定写入文件的目标数据为周边道路信息列表（列表-字典数据结构，包含指定坐标附近的部分道路信息）
                    fp=open(file=f"{DATA_PATH}/JSON_Road/Vicinity#{dict_road.get("location","-").replace(".","").replace(",","")}.json",mode="w",encoding="utf-8"),
                    indent=4,
                    skipkeys=False,
                    ensure_ascii=False,
                    check_circular=True,
                    allow_nan=True,
                    cls=None,
                    separators=(",",":"),
                    default=None,
                    sort_keys=False)
    else:   # 若指定城市为3级行政区划则进行2层循环遍历
        for adcode_district in list_adcode_district:    # 遍历城市下辖每一个区县级行政区
            list_district_road=request_road(key=key,adcode_district=adcode_district)    # 首先查询得到区县下辖部分主要道路信息，从函数返回值获取原始道路信息的列表-字典数据结构
            json.dump(  # 将主要道路信息列表写入指定文件
                obj=list_district_road,  # 指定写入文件的目标数据为主要道路信息列表（列表-字典数据结构，包含指定区县的部分主要道路信息）
                fp=open(file=f"{DATA_PATH}/JSON_Road/KeyWord#{adcode_district}.json",mode="w",encoding="utf-8"),
                indent=4,
                skipkeys=False,
                ensure_ascii=False,
                check_circular=True,
                allow_nan=True,
                cls=None,
                separators=(",",":"),
                default=None,
                sort_keys=False)
            for dict_road in list_district_road:    # 遍历区县下辖每一条主要道路
                if f"Vicinity#{dict_road.get("location","-").replace(".","").replace(",","")}.json" not in list_file:   # 防止重复写入文件（配合上述可复现的关键词道路信息列表，可实现程序意外错误中断后重新运行而不重复写入已经保存的文件）
                    list_vicinity=request_vicinity(key=key,adcode_city=adcode_city,coordinate=dict_road.get("location","113.926687,22.485890"),poi_type="190301")   # 查询每一条主要道路周边的部分道路信息
                    json.dump(  # 将周边道路信息列表写入指定文件
                        obj=list_vicinity,  # 指定写入文件的目标数据为周边道路信息列表（列表-字典数据结构，包含指定坐标附近的部分道路信息）
                        fp=open(file=f"{DATA_PATH}/JSON_Road/Vicinity#{dict_road.get("location","-").replace(".","").replace(",","")}.json",mode="w",encoding="utf-8"),
                        indent=4,
                        skipkeys=False,
                        ensure_ascii=False,
                        check_circular=True,
                        allow_nan=True,
                        cls=None,
                        separators=(",",":"),
                        default=None,
                        sort_keys=False)
                else:
                    print(f"Vicinity#{dict_road.get("location","-").replace(".","").replace(",","")}.json")
# 将道路信息原始数据（Web-API返回的json文件响应数据）解析后生成格式化表格数据（关系型表格模式、dataframe数据结构、csv文件格式）
def parse_road_info(adcode_city:str):   # 字符串传入参数adcode_city指定待解析道路信息的城市的行政区划代码
    list_file=os.listdir(path=f"{DATA_PATH}/JSON_Road/")    # 列出指定城市的原始道路数据（JSON文件）存储文件夹下的全部文件
    hash_dict_road_info=dict()  # 预先创建用于存储格式化道路信息表格的字典数据结构（临时，后续转换成dataframe数据结构）
    df_column_label=["id","name_road","location_road","typecode","name_type","towncode","adcode_district","name_district","address","count","source"]   # 预先创建道路信息表格的dataframe数据结构的表头列标签列表
    count_raw_data=0    # 辅助计数变量，统计指定城市通过高德地图API查询获取的原始数据数量
    for file_json in list_file: # 遍历指定城市原始道路数据存储文件夹下的每一个文件
        list_dict_road=json.load(fp=open(file=f"{DATA_PATH}/JSON_Road/{file_json}",mode="r",encoding="utf-8"))  # 载入当前文件所存储的原始道路信息的列表-字典数据结构
        count_raw_data+=len(list_dict_road) # 统计当前文件所包含的道路原始信息条数并保存至辅助计数变量
        for dict_road in list_dict_road:    # 遍历当前文件的列表-字典数据结构，取出每一条道路的原始信息字典
            if dict_road.get("parent","")!="":  # 检查当前道路是否存在“父元素”字段（仅作查看，用于判断当前道路是否被记录为某些其它道路的衍生路段）
                print(f"{file_json}\tSub-Road:\n{dict_road}")
            if dict_road.get("id","#") in hash_dict_road_info:  # 使用道路“元素”的唯一id判断，若当前道路已经在格式化道路信息表格中出现则记录其部分已有信息
                count=int(list(hash_dict_road_info[dict_road.get("id","#")])[9])+1  # 记录当前道路在指定城市的原始数据中出现的次数
                source=0 if file_json.startswith(f"KeyWord#") else int(list(hash_dict_road_info[dict_road.get("id","#")])[10])  # 判断当前道路的最初数据来源（0表示由get_road函数通过关键词搜索方法得到、1表示由get_vicinity函数通过周边搜索方法得到）
            else:   # 若当前道路在指定城市的解析遍历中首次出现
                count=1 # 初始化当前道路在指定城市的原始数据中出现的次数为1
                source=0 if file_json.startswith(f"KeyWord#") else 1    # 初始化记录当前道路的最初数据来源（0表示由get_road函数通过关键词搜索方法得到、1表示由get_vicinity函数通过周边搜索方法得到）
            hash_dict_road_info[dict_road.get("id","#")]=[  # 将当前道路原始信息的有效字段添加进入格式化道路信息表格（此时实际为字典数据结构，每条道路以其唯一id作为键，便于高效去重）
                dict_road.get("id","#"),    # 当前道路的唯一id（高德地图范围内适用）
                dict_road.get("name","#"),  # 当前道路的规范化名称
                dict_road.get("location","#"),  # 当前道路的坐标（原始信息中本字段以靠近道路中段的某一点坐标近似代替作为道路自身的坐标）
                dict_road.get("typecode","#"),  # 当前道路的类别编码（绝大多数为“道路名”对应编码）
                dict_road.get("type","#").replace(";","&"), # 当前道路的类别名称（绝大多数为“道路名”）
                f"{dict_road.get("adcode","#")}000000", # 当前道路所属街道级行政区的12位行政区划代码
                dict_road.get("adcode","#"),    # 当前道路所属区县级行政区的6位行政区划代码
                dict_road.get("adname","#"),    # 当前道路所属区县级行政区的名称
                dict_road.get("address","#"),   # 当前道路的详细规范化地址（绝大多数与其所属区县级行政区的名称相同）
                count,source]   # 当前道路在指定城市原始信息中出现的次数、当前道路的最初数据来源类型编码
        del list_dict_road  # 当前文件遍历解析完毕，及时释放其临时列表-字典数据结构占用的内存空间
    df_road_csv=pd.DataFrame(data=list(hash_dict_road_info.values()),columns=df_column_label,dtype=str,copy=True)  # 根据上述解析存储的城市道路信息字典和对应表头列标签创建dataframe数据结构
    df_road_csv.sort_values(by=["adcode_district","id"],inplace=True,ascending=True,ignore_index=True) # 根据城市道路所属区县级行政区的行政区划代码和其唯一id排序表格数据
    df_road_csv.to_csv(path_or_buf=f"{DATA_PATH}DF_Road_CSV1#{adcode_city}.csv",sep="\t",index=False,columns=None,encoding="utf-8")    # 将城市道路格式化信息表格（dataframe数据结构，暂不包含道路所属街道信息）存储至csv文件（指定\t作为行内分隔符）
    print(f"\n\n{df_road_csv}\nParse Result: Road Information Dataframe {df_road_csv.shape}/{count_raw_data}")    # 输出显示城市道路格式化信息表格以及指定城市的原始道路数据总条数，表示指定城市的道路信息解析成功完成
# 高德地图Web-API第二次查询指定城市下辖的部分道路信息（内部封装request_vicinity函数，以现有道路的聚类中心点为坐标）
def add_road_info(key:str,adcode_city:str): # 字符串传入参数key指定API调用密钥、adcode_city指定待查询道路信息的城市的行政区划代码
    df_road_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_CSV1#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（初始）格式化道路信息表格
    df_ad_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Ad_CSV#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（初始）格式化行政区划信息表格
    list_coordinate=[(float(location.split(",")[0]),float(location.split(",")[1])) for location in list(df_road_csv["location_road"])] # 获取指定城市目前记录的全部道路的坐标
    kmeans=KMeans(n_clusters=12*int(df_ad_csv.shape[0]),   # 指定聚类中心点数量为指定城市所包含街道级行政区数量的12倍
        init="k-means++",
        n_init="auto",
        max_iter=100000,
        tol=1e-4,
        verbose=0,
        random_state=1, # 指定模型的随机数种子参数以使得结果可复现
        copy_x=True,
        algorithm="lloyd")  # 定义KMeans模型
    kmeans.fit(X=list_coordinate,sample_weight=None)  # 使用指定城市目前全部道路的坐标训练KMeans聚类模型
    list_centroids=[f"{centroid[0]:.6f},{centroid[1]:.6f}" for centroid in kmeans.cluster_centers_] # 获取训练后模型生成的聚类中心点坐标（存储为字符串列表）
    list_file=os.listdir(path=f"{DATA_PATH}/JSON_Road/")    # 打开指定城市数据目录下存储原始道路数据的子文件夹并列出全部下属文件
    for centroid in list_centroids: # 遍历每一个聚类中心点，调用高德地图API查询获取其附近的道路信息
        if f"Centroid#{centroid.replace(".","").replace(",","")}.json" not in list_file:    # 防止重复写入文件（配合上述可复现的KMeans聚类中心点列表，可实现程序意外错误中断后重新运行而不重复写入已经保存的文件）
            list_vicinity=request_vicinity(key=key,adcode_city=adcode_city,coordinate=centroid,poi_type="190301")
            json.dump(  # 将周边道路信息列表写入指定文件
                obj=list_vicinity,  # 指定写入文件的目标数据为周边道路信息列表（列表-字典数据结构，包含指定坐标附近的部分道路信息）
                fp=open(file=f"{DATA_PATH}/JSON_Road/Centroid#{centroid.replace(".","").replace(",","")}.json",mode="w",encoding="utf-8"),
                indent=4,
                skipkeys=False,
                ensure_ascii=False,
                check_circular=True,
                allow_nan=True,
                cls=None,
                separators=(",",":"),
                default=None,
                sort_keys=False)
# 高德地图Web-API查询指定城市下辖的部分桥梁和隧道信息（内部封装request_vicinity函数，以现有道路的聚类中心点为坐标）
def add_other_info(key:str,adcode_city:str):    # 字符串传入参数key指定API调用密钥、adcode_city指定待查询桥梁和隧道信息的城市的行政区划代码
    df_road_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_CSV1#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（初始）格式化道路信息表格
    df_ad_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Ad_CSV#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（初始）格式化行政区划信息表格
    list_coordinate=[(float(location.split(",")[0]),float(location.split(",")[1])) for location in list(df_road_csv["location_road"])] # 获取指定城市目前记录的全部道路的坐标
    kmeans=KMeans(n_clusters=12*int(df_ad_csv.shape[0]),   # 指定聚类中心点数量为指定城市所包含街道级行政区数量的12倍
        init="k-means++",
        n_init="auto",
        max_iter=100000,
        tol=1e-4,
        verbose=0,
        random_state=1, # 指定模型的随机数种子参数以使得结果可复现
        copy_x=True,
        algorithm="lloyd")  # 定义KMeans模型
    kmeans.fit(X=list_coordinate,sample_weight=None)  # 使用指定城市目前全部道路的坐标训练KMeans聚类模型
    list_centroids=[f"{centroid[0]:.6f},{centroid[1]:.6f}" for centroid in kmeans.cluster_centers_] # 获取训练后模型生成的聚类中心点坐标（存储为字符串列表）
    list_file=os.listdir(path=f"{DATA_PATH}/JSON_Road/") # 打开指定城市数据目录下存储原始道路数据的子文件夹并列出全部下属文件
    for centroid in list_centroids: # 遍历每一个聚类中心点，调用高德地图API查询获取其附近的道路信息
        if f"Other#{centroid.replace(".","").replace(",","")}.json" not in list_file:   # 防止重复写入文件（配合上述可复现的KMeans聚类中心点列表，可实现程序意外错误中断后重新运行而不重复写入已经保存的文件）
            list_vicinity=request_vicinity(key=key,adcode_city=adcode_city,coordinate=centroid,poi_type="190306|190307|190310")
            json.dump(  # 将周边道路信息列表写入指定文件
                obj=list_vicinity,  # 指定写入文件的目标数据为周边道路信息列表（列表-字典数据结构，包含指定坐标附近的部分道路信息）
                fp=open(file=f"{DATA_PATH}/JSON_Road/Other#{centroid.replace(".","").replace(",","")}.json",mode="w",encoding="utf-8"),
                indent=4,
                skipkeys=False,
                ensure_ascii=False,
                check_circular=True,
                allow_nan=True,
                cls=None,
                separators=(",",":"),
                default=None,
                sort_keys=False)
# 高德地图Web-API请求获取指定地理坐标对应的格式化地址信息（逆地理编码）
def request_town(key:str,coordinate:str):   # 字符串传入参数key指定API调用密钥、coordinate指定待查询地点的坐标
    time.sleep(0.4) # 每次查询前程序暂停0.4秒以满足高德地图API的并发查询QPS上限限制
    api_response=requests.get(  # 调用Web-API查询传入参数指定坐标的逆地理编码
        url=f"https://restapi.amap.com/v3/geocode/regeo",   # API调用的http请求命令本体
        params={    # http请求的参数字典，上述get函数中自动拼接为完整的http请求命令
            "key":key,  # 传入API调用密钥
            "output":"JSON",    # 指定响应数据格式为json文件
            "location":coordinate,  # 指定待查询地点的坐标
            "poitype":"190301", # 使用类型代码指定查询的地点类型为道路名称
            "radius":1000,  # 指定查询地点的范围（圆形半径，单位为米）
            "extensions":"all", # 指定响应数据返回指定地点的完整信息
            "roadlevel":0,  # 指定响应数据返回指定地点附近的完整道路信息
            "homeorcorp":0  # 指定响应数据无需针对地址类型（住宅或企业）执行排序优化
        })
    if api_response.status_code!=200 or api_response.json()["infocode"]!="10000":   # 检查响应数据状态代码是否正常
        print(f"Request Town-Info#{coordinate} Failure Response: {api_response.status_code}#{api_response.text}")
        return dict()   # 若查询请求出现任何形式的异常结果则返回空字典以表示查询失败
    else:
        print(f"Request Town-Info#{coordinate} Success Response: {api_response.text}")
        return api_response.json().get("regeocode",dict())  # 若查询请求成功得到正常结果则返回JSON数据解析得到的“逆地理编码”字典数据结构
# 高德地图Web-API请求获取指定城市部分代表性地点的所属街道信息（内部封装request_town函数）
def get_town_info(key:str,adcode_city:str): # 字符串传入参数key指定API调用密钥、adcode_city指定待查询街道信息的城市的行政区划代码
    df_road_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_CSV1#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（初始）格式化道路信息表格
    df_ad_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Ad_CSV#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（初始）格式化行政区划信息表格
    list_coordinate=[(float(location.split(",")[0]),float(location.split(",")[1])) for location in list(df_road_csv["location_road"])] # 获取指定城市目前记录的全部道路的坐标
    kmeans=KMeans(n_clusters=12*int(df_ad_csv.shape[0]),   # 指定聚类中心点数量为指定城市所包含街道级行政区数量的12倍
        init="k-means++",
        n_init="auto",
        max_iter=100000,
        tol=1e-4,
        verbose=0,
        random_state=1, # 指定模型的随机数种子参数以使得结果可复现
        copy_x=True,
        algorithm="lloyd")  # 定义KMeans模型
    kmeans.fit(X=list_coordinate,sample_weight=None)  # 使用指定城市全部道路的坐标训练KMeans聚类模型
    list_centroids=[f"{centroid[0]:.6f},{centroid[1]:.6f}" for centroid in kmeans.cluster_centers_] # 获取训练后模型生成的聚类中心点坐标（存储为字符串列表）
    list_dict_town=list()   # 预先创建聚类中心点坐标对应逆地理编码的列表-字典数据结构
    for centroid in list_centroids: # 遍历每一个聚类中心点，调用高德地图API查询获取其逆地理编码信息字典并按照原顺序（重要！）添加进入上述列表-字典数据结构
        list_dict_town.append(request_town(key=key,coordinate=centroid))
    json.dump(  # 将聚类中心点坐标对应逆地理编码的列表-字典数据结构存储至指定文件
        obj=list_dict_town,
        fp=open(file=f"{DATA_PATH}/JSON_ReGeo.json",mode="w",encoding="utf-8"),
        indent=4,
        skipkeys=False,
        ensure_ascii=False,
        check_circular=True,
        allow_nan=True,
        cls=None,
        separators=(",",":"),
        default=None,
        sort_keys=False)
    json.dump(  # 将聚类中心点编号列表存储至指定文件（列表隐含下标，与存储指定城市道路信息的dataframe数据结构的行下标一一对应，列表每个位置的内容指示其下标对应道路被分配至聚类中心点的下标编号）
        obj=[f"{centroid_idx}" for centroid_idx in kmeans.labels_],
        fp=open(file=f"{DATA_PATH}/JSON_Label.json",mode="w",encoding="utf-8"),
        indent=4,
        skipkeys=False,
        ensure_ascii=False,
        check_circular=True,
        allow_nan=True,
        cls=None,
        separators=(",",":"),
        default=None,
        sort_keys=False)
# 将指定城市部分代表性地点的街道信息原始数据（Web-API返回的json文件响应数据）解析并除错（对于街道和区县行政区划代码不一致的道路需要根据其坐标重新调用Web-API查询所属街道）后整合至存储道路信息和行政区划信息的dataframe表格
def check_parse_town_info(key:str,adcode_city:str): # 字符串传入参数key指定API调用密钥、adcode_city指定待解析街道级行政区划信息的城市的行政区划代码
    df_road_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_CSV1#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")    # 读取指定城市的（初始）格式化道路信息表格
    df_ad_csv=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Ad_CSV#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")    # 读取指定城市的（初始）格式化行政区划信息表格
    list_address=json.load(fp=open(file=f"{DATA_PATH}/JSON_ReGeo.json",mode="r",encoding="utf-8"))  # 读取指定城市聚类中心点的逆地理编码信息（列表-字典数据结构）
    list_label=json.load(fp=open(file=f"{DATA_PATH}/JSON_Label.json",mode="r",encoding="utf-8"))    # 读取指定城市的道路和聚类中心点编号对应关系的列表
    dict_town=dict()    # 预先创建指定城市街道级行政区其行政区划代码和名称对应关系的字典
    for idx in range(0,len(list_label),1):  # 遍历指定城市的每一条道路（根据其在道路信息表格中的行下标按顺序遍历）
        dict_address=list_address[int(list_label[idx])]["addressComponent"] # 获取当前道路对应聚类中心点的逆地理编码信息（仅取用其“详细地址要素”字段字典）
        dict_town[str(dict_address["township"])]=dict_address["towncode"]   # 根据聚类中心点的逆地理编码信息在全局关系字典中记录其所属街道级行政区代码和名称的对应关系（为方便查询，实际以街道级行政区的名称作为键）
        df_road_csv.loc[idx,"towncode"]=dict_address["towncode"] if dict_address["towncode"]!=list() else df_road_csv.loc[idx,"towncode"]   # 记录当前道路对应聚类中心点的所属街道等效于当前道路的所属街道（重要的近似关系！）
    for idx in range(0,int(df_ad_csv.shape[0]),1):  # 根据全局关系字典的内容更新记录指定城市行政区划表格中每个街道级行政区的行政区划代码
        if df_ad_csv.loc[idx,"township"] in dict_town:
            df_ad_csv.loc[idx,"towncode"]=dict_town[df_ad_csv.loc[idx,"township"]]
        else:   # 若指定街道未出现在指定城市街道级行政区其行政区划代码和名称对应关系的字典中（说明当前街道不拥有任何一个聚类中心点）则需要另行查询其行政区划代码
            dict_address=request_town(key=key,coordinate=df_ad_csv.loc[idx,"location_town"])["addressComponent"]   # 调用高德地图API重新查询“尚未查询到行政区划代码的街道”坐标对应的逆地理编码字典，直接获取其“详细地址要素”字段字典
            if dict_address["township"]==df_ad_csv.loc[idx,"township"]:
                df_ad_csv.loc[idx,"towncode"]=dict_address["towncode"]  # 若另行查询确实得到正确（符合预期）的街道信息则在行政区划信息表格中记录当前街道的正确行政区划代码
    for idx in range(0,int(df_road_csv.shape[0]),1):    # 再次遍历指定城市每一条道路，检查上述（根据道路所属的聚类中心点近似分配其所属街道）解析后是否存在所属街道与所属区县（若有）不一致的道路
        if int(int(df_road_csv.loc[idx,"towncode"])/1000000)!=int(df_road_csv.loc[idx,"adcode_district"]):  # 若道路所属街道与所属区县（若有）不一致则需要重新查询其真实的所属街道
            dict_address=request_town(key=key,coordinate=df_road_csv.loc[idx,"location_road"])["addressComponent"] # 调用高德地图API重新查询“错误分配所属街道”道路坐标对应的逆地理编码字典，直接获取其“详细地址要素”字段字典
            df_road_csv.loc[idx,"towncode"]=dict_address["towncode"] if dict_address["towncode"]!=list() else df_road_csv.loc[idx,"towncode"]   # 道路信息表格中重新记录当前道路的正确所属街道
    df_ad_csv.sort_values(by="towncode",ascending=True,inplace=True,ignore_index=True)  # 根据街道级行政区的12位行政区划代码排序指定城市的行政区划信息表格数据
    df_ad_csv.to_csv(path_or_buf=f"{DATA_PATH}DF_AD_Info#{adcode_city}.csv",sep="\t",index=False,columns=None,encoding="utf-8") # 将更新后的行政区划信息表格（dataframe数据结构）存储至新csv文件
    df_road_csv.sort_values(by=["towncode","id"],inplace=True,ascending=True,ignore_index=True) # 根据城市道路所属街道级行政区的行政区划代码和其唯一id排序表格数据
    df_road_csv.to_csv(path_or_buf=f"{DATA_PATH}DF_Road_CSV2#{adcode_city}.csv",sep="\t",index=False,columns=None,encoding="utf-8") # 将更新后的城市道路格式化信息表格（dataframe数据结构）存储至新csv文件
    print(f"\n\n{df_road_csv}\n\n{df_ad_csv}\nParse Result: Dataframe including Town Information")  # 输出显示城市道路格式化信息表格和行政区划信息表格，表示指定城市包含所属街道的道路和行政区划信息解析成功完成
# 根据道路名称解析其所属具体道路类型并保存至原dataframe数据结构存储文件
def classify_road_info(adcode_city:str):    # 字符串传入参数adcode_city指定待解析道路类型的城市的行政区划代码
    df_road_info=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_CSV2#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（包含街道行政区划代码信息的）格式化道路信息表格
    for idx in range(0,int(df_road_info.shape[0]),1):   # 遍历道路信息表格每一行
        name_road=df_road_info.loc[idx,"name_road"] # 获取当前道路的名称
        set_typecode_road=set(df_road_info.loc[idx,"typecode"].split("|"))  # 获取当前道路由高德地图API记录的道路类型代码（字符串切割为集合形式）
        entity_road=name_road.split("(")[-2] if name_road.endswith(")") else name_road  # 获取当前道路本体名称（若当前道路完整名称以括号内容结尾则去除其名称尾部的括号内容）
        suffix_road=None    # 定义记录道路类型（后缀）的字符串（以None变量表示其内容为空）
        for type_road in DICT_TYPE_ROAD.keys(): # 遍历道路类型字典的键
            if (type_road=="商业.街" or type_road=="工业.街") and re.compile(type_road).search(entity_road) and entity_road.endswith("街"):
                suffix_road=DICT_TYPE_ROAD[type_road]   # 若道路名称以“商业.街”或“工业.街”结尾则确定其对应类型（包含不定字符的正则表达式匹配，需要优先处理）
                break   # 及时中断退出循环，避免同一道路匹配不同的道路类型（下同）
            elif entity_road.endswith(type_road):   # 若道路名称以某种路面分词结尾则确定其对应类型
                suffix_road=DICT_TYPE_ROAD[type_road]
                break
        if not suffix_road: # 严格匹配路面本体后缀的查找失败（未能够识别任何一种已知的路面分词作为后缀）则在整个路面中执行正则表达式匹配，尝试确定道路类型
            for type_road in DICT_TYPE_ROAD.keys():
                if re.compile(type_road).search(entity_road):
                    suffix_road=DICT_TYPE_ROAD[type_road]
                    break
        if suffix_road in {"辅路","支路","辅道","匝道","段"}:    # 若当前通过路面分词识别到的道路类型为“辅路”或相似含义的类型，则需要在路面中去除该分词后重新执行正则表达式匹配以查找其完整类型
            entity_road=entity_road.replace(suffix_road,"") # 在路面中去除该分词后重新执行正则表达式匹配以查找其完整类型
            for type_road in DICT_TYPE_ROAD.keys(): # 例如道路名称很可能为“XX路辅路”的形式，则需要确定“辅路”之前的名称部分对应的道路类型
                if re.compile(type_road).search(entity_road):
                    suffix_road=f"{DICT_TYPE_ROAD[type_road]}|{suffix_road}"
                    break
        if not suffix_road and entity_road[0] in DICT_TYPE_WAY.keys():  # 若道路名称以表示特殊行政道路（国道等）的字母起始则需要将对应特殊道路类型添加进入道路类型后缀字符串
            suffix_road=DICT_TYPE_WAY[entity_road[0]]
        elif suffix_road and entity_road[0] in DICT_TYPE_WAY.keys() and DICT_TYPE_WAY[entity_road[0]] not in set(suffix_road.split("|")):
            suffix_road=f"{DICT_TYPE_WAY[entity_road[0]]}|{suffix_road}"
        if not suffix_road: # 若上述查找匹配均失败则将当前道路类型记录为“其它”
            suffix_road="其它"
        for typecode in set_typecode_road:  # 处理当前道路的道路类型代码（上述查找匹配从道路名称中提取分词以尝试确定其道路类型，与此处解析道路类型代码无关）
            if typecode not in {"190301","190306","190307","190310"}:   # 若当前道路的道路类型代码集合中包含不属于4种典型道路的代码（4种典型道路代码依次表示“道路名”、“立交桥”、“桥”、“隧道”）
                suffix_road=f"{suffix_road}|{
                    df_road_info.loc[idx,"name_type"].replace(
                        "地名地址信息&交通地名&道路名","").replace(
                        "地名地址信息&交通地名&桥","").replace(
                        "地名地址信息&交通地名&立交","").replace(
                        "地名地址信息&交通地名&隧道","").replace(
                        "|","")}"   # 从原道路信息表格中获取上述“不属于4种典型道路的代码”对应文本描述并添加进入道路类型后缀字符串
        if "190306" in set_typecode_road and "190307" in set_typecode_road: # 若当前道路同时属于“立交桥”和“桥”则规定其类型代码仅包含“立交桥”即可
            set_typecode_road.remove("190307")
        if "190301" in set_typecode_road and ("190306" in set_typecode_road or "190307" in set_typecode_road or "190310" in set_typecode_road): # 若当前道路同时属于“道路名”，和“桥”或“隧道”类型，则规定其类型代码中不应当包含“道路名”
            set_typecode_road.remove("190301")
        df_road_info.loc[idx,"typecode"]="".join([f"|{typecode}" for typecode in sorted(list(set_typecode_road))])[1:]  # 将上述解析完成的道路类型代码集合重新拼接为字符串（“|”作为分隔符）并保存至对应道路在道路信息表格中的“道路类型代码”字段
        df_road_info.loc[idx,"name_type"]=suffix_road   # 将上述解析完成的道路类型后缀字符串（“|”作为分隔符）保存至对应道路在道路信息表格中的“道路类型名称”字段
    df_road_info.to_csv(path_or_buf=f"{DATA_PATH}DF_Road_CSV3#{adcode_city}.csv",sep="\t",index=False,columns=None,encoding="utf-8")    # 将更新后的城市道路格式化信息表格（dataframe数据结构）存储至原csv文件
# 城市道路名称去重（相同区县级行政区的同名道路添加数字编号后缀以示区分；由于道路唯一ID不同，无需去除同名道路）
def uniquify_road_info(adcode_city:str):    # 字符串传入参数adcode_city指定待去重道路名称的城市的行政区划代码
    df_road_info=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_CSV3#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")   # 读取指定城市的（包含街道行政区划代码信息的）格式化道路信息表格
    dict_unique_name_road=dict()    # 创建{道路标记:计数}字典以统计每个特定名称的道路在道路信息表格中的出现次数
    for idx in range(0,int(df_road_info.shape[0]),1):   # 首次遍历道路信息表格中每一条道路并初始化上述字典，以道路名称和其所属区县的行政区划代码的拼接字符串作为键
        dict_unique_name_road[f"{df_road_info.loc[idx,"name_road"]}&{df_road_info.loc[idx,"adcode_district"]}"]=0
    for idx in range(0,int(df_road_info.shape[0]),1):   # 再次遍历道路信息表格中每一条道路，计数其同名道路的出现次数并对出现次数超过1的道路添加对应的数字后缀标记
        dict_unique_name_road[f"{df_road_info.loc[idx,"name_road"]}&{df_road_info.loc[idx,"adcode_district"]}"]+=1
        if dict_unique_name_road[f"{df_road_info.loc[idx,"name_road"]}&{df_road_info.loc[idx,"adcode_district"]}"]>=2:
            df_road_info.loc[idx,"name_road"]=f"{df_road_info.loc[idx,"name_road"]}#{dict_unique_name_road[
                f"{df_road_info.loc[idx,"name_road"]}&{df_road_info.loc[idx,"adcode_district"]}"]}"
    df_road_info.to_csv(path_or_buf=f"{DATA_PATH}DF_Road_Info#{adcode_city}.csv",sep="\t",index=False,columns=None,encoding="utf-8")    # 将更新后的城市道路格式化信息表格（dataframe数据结构）存储至原csv文件

# 调用高德地图Web-API测试道路数据的覆盖率
def test_data_coverage(key:str,adcode_city:str,index_street:int):
    df_road=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_Info#{adcode_city}.csv",sep="\t",dtype=str,encoding="utf-8")
    list_coord=list(df_road["location_road"])
    idx=index_street%len(list_coord) if index_street>=0 else random.randint(0,len(list_coord))
    list_road_test=request_vicinity(key=key,adcode_city=adcode_city,coordinate=list_coord[idx],poi_type="190301|190306|190307|190310")
    json.dump(
        obj=list_road_test,
        fp=open(file=f"./Data_Test_{adcode_city}#{idx}.json",mode="w",encoding="utf-8"),
        indent=4,
        skipkeys=False,
        ensure_ascii=False,
        check_circular=True,
        allow_nan=True,
        cls=None,
        separators=(",", ":"),
        default=None,
        sort_keys=False)
    count_omission=0
    for dict_road_test in list_road_test:
        df_match=df_road[df_road["id"]==dict_road_test["id"]]
        if df_match.shape[0]<=0:
            print(f"Missed Road:\t{dict_road_test}\n")
            count_omission+=1
        else:
            print(f"Existed Road:\t{df_match}\n")
    print(f"Test Result:{adcode_city}#{idx},Count Missed:{count_omission}\n")
# 将dataframe数据结构以超级表形式写入保存至Excel的.xlsx文件
def output_excel(df_list:list,sheet_list:list,file_path:str): # 传入列表参数df_list指定待写入xlsx文件的dataframe表格列表、列表参数sheet_list指定每个dataframe写入excel工作表的表名、字符串参数file_path指定写入文件的完整名称（包含路径和后缀名）
    if len(df_list)<=0 or len(df_list)!=len(sheet_list): return
    excel_writer=pd.ExcelWriter(
        path=file_path,
        mode="w",
        engine="xlsxwriter",
        date_format="YYYY/MM/DD",
        datetime_format="YYYY/MM/DD#HH:MM:SS",
        storage_options=None,
        if_sheet_exists=None,
        engine_kwargs=None) # 定义excel文件写入流
    for idx in range(0,len(df_list),1):
        df=df_list[idx]
        sheet_name=sheet_list[idx]
        df.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            na_rep="#",
            float_format="%.2f",
            columns=df.columns,
            header=True,
            index=False,
            index_label=None,
            startrow=0,
            startcol=0,
            engine="xlsxwriter",
            merge_cells=True,
            inf_rep="inf",
            freeze_panes=None,
            storage_options=None,
            engine_kwargs=None) # 每个dataframe表格数据以指定表名写入xlsx文件
        worksheet=excel_writer.sheets[sheet_name]
        worksheet.add_table(
            0,0,int(df.shape[0]),int(df.shape[1])-1,
            {
                "columns":[{"header":column} for column in df.columns], # 设置超级表表头列标签
                "style":"Table Style Medium 15",    # 设置超级表表格样式
                "autofilter":True
            })  # 定义超级表结构
        worksheet.autofit() # 设置excel文件内容为超级表结构
    excel_writer.close()    # 关闭excel文件写入流



# get_parse_ad_info(key=AMAP_KEY_ID,adcode_city=CITY)
# get_road_info(key=AMAP_KEY_ID,adcode_city=CITY)
# parse_road_info(adcode_city=CITY)
# add_road_info(key=AMAP_KEY_ID,adcode_city=CITY)
# add_other_info(key=AMAP_KEY_ID,adcode_city=CITY)
# parse_road_info(adcode_city=CITY)
# get_town_info(key=AMAP_KEY_ID,adcode_city=CITY)
# check_parse_town_info(key=AMAP_KEY_ID,adcode_city=CITY)
# classify_road_info(adcode_city=CITY)
# uniquify_road_info(adcode_city=CITY)

test_data_coverage(key=AMAP_KEY_ID,adcode_city=CITY,index_street=-1)

# df_road_info=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Road_Info#{CITY}.csv",sep="\t",dtype=str,encoding="utf-8")
# df_ad_info=pd.read_csv(filepath_or_buffer=f"{DATA_PATH}DF_Ad_Info#{CITY}.csv",sep="\t",dtype=str,encoding="utf-8")
# output_excel(df_list=[df_road_info,df_ad_info],sheet_list=[f"Road#{CITY}",f"AD#{CITY}"],file_path=f"{DATA_PATH}/Excel_Info#{CITY}.xlsx")
# df_excel=pd.read_excel(io=f"{DATA_PATH}/Excel_Info#{CITY}.xlsx",sheet_name=0)
# print(f"{df_excel}")