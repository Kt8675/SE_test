import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# 功能函数定义区域=========================================================================================================================================================================

# 从CSV文件载入数据并返回dataframe数据结构（传入参数字符串file指示包含路径的文件名称）（针对文件不存在错误返回空dataframe）
def load_df_csv(file:str):
    try:
        return pd.read_csv(filepath_or_buffer=file,sep="\t",dtype=str,encoding="utf-8")
    except FileNotFoundError:
        return pd.DataFrame(data=None,columns=None,index=None,dtype=str,copy=True)
# 获取dataframe数据结构的“列取值选择器”（返回{列名:dataframe在该列的全部不同可能取值列表}字典）
def get_column_selector(df:pd.DataFrame):
    return dict({column:sorted(list(set(df[column]))) for column in df.columns})
# 根据关键词筛选dataframe数据结构的指定行（传入参数df指示待筛选的dataframe、字符串column指示筛选依据列名、keyword指示筛选关键词且支持正则表达式格式输入）（针对列名错误返回原dataframe）
def filter_df_keyword(df:pd.DataFrame,column:str,keyword:str):
    try:
        return df[df[column].str.contains(keyword,case=False,na=False,regex=True)]
        
    except KeyError:
        return df.copy(deep=False)
# 根据行索引筛选dataframe数据结构的指定行（传入参数df指示待筛选的dataframe、整型值start和stop分别指示筛选行索引的起始值和结束值，左闭右开）（针对索引参数超限返回空dataframe）
def filter_df_index(df:pd.DataFrame,start:int,stop:int):
    return df.copy(deep=False).iloc[start:stop,:]
# 根据列名筛选dataframe数据结构的指定列（传入参数df指示待筛选的dataframe、列表数据结构columns指示筛选需要保留列名）（针对列名错误返回原dataframe）
def filter_df_column(df:pd.DataFrame,columns:list):
    try:
        return df.copy(deep=False)[columns]
    except KeyError:
        return df.copy(deep=False)
# （SQL的左外连接）拼接两个dataframe数据结构（传入参数df1和df2分别指示待拼接的两个dataframe、字符串column指示拼接依据的唯一公共列）（针对列名错误返回两个dataframe按照共有列名默认拼接的dataframe）
def concat_df_left(df_left:pd.DataFrame,df_right:pd.DataFrame,column:str):
    try:
        return pd.merge(left=df_left,right=df_right,how="left",on=column,
                        left_on=None,right_on=None,left_index=False,right_index=False,
                        sort=False,suffixes=("","#AD"),copy=False,indicator=False)
    except KeyError:
        return pd.merge(left=df_left,right=df_right,how="left",on=None,
                        left_on=None,right_on=None,left_index=False,right_index=False,
                        sort=False,suffixes=("","#AD"),copy=False,indicator=False)
# 根据指定列排序dataframe数据结构（传入参数df指示待排序的dataframe、列表数据结构columns按照优先级顺序指示排序依据列名、布尔值ascend指示是否升序）（针对列名错误返回原dataframe）
def sort_df_value(df:pd.DataFrame,columns:list,ascend:bool=True):
    try:
        return df.sort_values(by=columns,inplace=False,ascending=ascend,ignore_index=True)
    except KeyError:
        return df.copy(deep=False)
# 根据道路与指定坐标的距离排序道路信息表格（传入参数df_road为道路信息表格的dataframe，字符串location以“xxx.xxx,yyy.yyy”格式传入排序依据的中心坐标）
def sort_road_location(df_road:pd.DataFrame,location:str):
    x0=None
    y0=None
    df_new=df_road.copy(deep=True)
    try:    # 尝试解析传入参数location表示的中心坐标，若解析失败则直接返回原dataframe
        x0=float(location.split(",")[0])
        y0=float(location.split(",")[1])
    except ValueError:
        return df_new
    dict_location=dict({df_new.loc[i,"id"]:df_new.loc[i,"location_road"] for i in range(0,int(df_new.shape[0]),1)}) # 借用道路信息表格的location_road列存放道路到中心坐标的距离，需要先行转存其原本数据
    for id_road in dict_location.keys():    # 计算每条道路到中心坐标的距离并存入道路信息表格的location_road列
        x1=float(dict_location[id_road].split(",")[0])
        y1=float(dict_location[id_road].split(",")[1])
        df_new.loc[df_new["id"]==id_road,"location_road"]=(x1-x0)**2+(y1-y0)**2
    df_new.sort_values(by=["location_road","towncode","id"],inplace=True,ascending=True,ignore_index=True)  # 根据距离由近及远的顺序排序道路信息表格的数据行
    for id_road in dict_location.keys():    # 将道路信息表格location_road列原本每条道路的坐标数据转存回表格本体
        df_new.loc[df_road["id"]==id_road,"location_road"]=dict_location[id_road]
    del dict_location   # 清除临时转存数据的字典数据结构，及时释放内存空间
    return df_new   # 返回排序完成的道路信息表格副本

# （使用道路坐标近似表示道路的位置）绘制散点图显示指定城市获取得到的全部道路和行政区划位置
def plot_road_info(df_road:pd.DataFrame,df_ad:pd.DataFrame):    # dataframe传入参数df_road和df_ad分别指定待绘图城市的格式化道路信息表格和行政区划信息表格
    COLOR_LIST=["#ff0000","#ff7f00","#efef00","#00ff00","#00ffff","#007fff","#0000ff","#7f00ff","#ff00ff"]  # 绘制不同区县级行政区道路散点使用的颜色参数字符串列表
    x=list()    # 散点图绘制使用的全局横坐标列表（实际并不用于散点图绘制，仅用于统计整个散点图中横坐标的极值）
    y=list()    # 散点图绘制使用的全局纵坐标列表（实际并不用于散点图绘制，仅用于统计整个散点图中纵坐标的极值）
    plt.figure(figsize=(5,3),dpi=800)   # 指定散点图图片尺寸
    plt.rcParams["font.size"]=4 # 指定散点图标注文本全局字体尺寸
    for idx,town in enumerate(set(df_road["towncode"])):    # 遍历格式化道路信息表格，为每一个街道级行政区下辖的道路绘制相同颜色（不同街道不同颜色）的散点图
        df_district=df_road[df_road["towncode"]==town] # 筛选得到格式化道路信息表格中属于当前街道的全部道路对应的数据行
        x1=list(float(location.split(",")[0]) for location in list(df_district["location_road"]))   # 计算统计得到上述街道下辖道路的横坐标列表
        y1=list(float(location.split(",")[1]) for location in list(df_district["location_road"]))   # 计算统计得到上述街道下辖道路的纵坐标列表
        plt.scatter(x=x1,y=y1,s=0.01,c=COLOR_LIST[idx%len(COLOR_LIST)],marker="*",alpha=1,label=f"{town}:{df_district.shape[0]}")   # 绘制当前街道下辖道路的散点图，指定散点的尺寸、颜色、透明度以及所属标签（其中标签用于后续图例绘制）
        x.extend(x1)    # 将当前街道下辖道路的横坐标列表添加进入全局横坐标列表
        y.extend(y1)    # 将当前街道下辖道路的纵坐标列表添加进入全局纵坐标列表
    df_source=df_road[df_road["source"]=="0"] # 筛选得到格式化道路信息表格中最初由get_road函数通过关键词搜索得到的全部道路对应的数据行
    x0=list(float(location.split(",")[0]) for location in list(df_source["location_road"])) # 计算统计得到上述“关键词搜索”道路的横坐标列表
    y0=list(float(location.split(",")[1]) for location in list(df_source["location_road"])) # 计算统计得到上述“关键词搜索”道路的纵坐标列表
    plt.scatter(x=x0,y=y0,s=0.03,c=f"#7f7f7f",marker="o",alpha=1,label=f"primary:{df_source.shape[0]}") # 绘制“关键词搜索”道路对应的散点图
    x0=list(float(location.split(",")[0]) for location in list(df_ad["location_town"]))    # 计算统计得到指定城市全部街道级行政区的中心横坐标列表
    y0=list(float(location.split(",")[1]) for location in list(df_ad["location_town"]))    # 计算统计得到指定城市全部街道级行政区的中心纵坐标列表
    plt.scatter(x=x0,y=y0,s=0.03,c=f"#000000",marker="*",alpha=1,label=f"town:{df_ad.shape[0]}") # 绘制指定城市全部街道级行政区中心对应的散点图
    margin=0.01 # 指定散点图坐标极值距离散点图边缘的留空距离
    plt.xlim(min(x)-margin,max(x)+margin)   # 设置散点图的X轴显示范围
    plt.ylim(min(y)-margin,max(y)+margin)   # 设置散点图的Y轴显示范围
    bar_tick_list=np.arange(start=min(x)-margin,stop=max(x)+margin,step=0.1,dtype=float)
    plt.xticks(ticks=bar_tick_list,labels=[f"{tick:.2f}" for tick in bar_tick_list])    # 设置散点图的横坐标坐标轴标签
    bar_tick_list=np.arange(start=min(y)-margin,stop=max(y)+margin,step=0.1,dtype=float)
    plt.yticks(ticks=bar_tick_list, labels=[f"{tick:.2f}" for tick in bar_tick_list])   # 设置散点图的纵坐标坐标轴标签
    plt.gca().set_aspect("equal",adjustable="box")  # 设置散点图横坐标和纵坐标的比例尺相等
    plt.legend(loc="upper right",fontsize=3,framealpha=0,title="AdCode")   # 设置散点图的图例
    plt.show()  # 显示绘制完成的散点图
# 将dataframe数据结构以超级表形式写入保存至Excel的.xlsx文件
def output_df_excel(df_list:list,sheet_list:list,file_path:str): # 传入列表参数df_list指定待写入xlsx文件的dataframe表格列表、列表参数sheet_list指定每个dataframe写入excel工作表的表名、字符串参数file_path指定写入文件的完整名称（包含路径和后缀名）
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


if __name__ == "__main__":
# 使用示例区域（按需修改文件路径！！！！！）==========================================================================

    CITY="440300"   # 待查询的城市行政区划代码（必须为市级行政区）
    DATA_PATH=f"./Data_Info#{CITY}/"    # 当前城市的道路和行政区划数据存储文件父级路径

    df_road_info=load_df_csv(file=f"{DATA_PATH}DF_Road_Info#{CITY}.csv")    # 载入道路信息表格
    df_ad_info=load_df_csv(file=f"{DATA_PATH}DF_Ad_Info#{CITY}.csv")    # 载入行政区划信息表格
    dict_selector=get_column_selector(df=df_road_info)  # 获取道路信息表格的列取值选择器

    df1=sort_road_location(df_road=df_road_info,location="113.897935,22.768109")    # 根据道路于指定坐标的距离由近及远排序
    df2=filter_df_keyword(df=df1,column="name_road",keyword=r"振兴路|红桂路")  # 字符串匹配查找指定名称的道路（传入关键词支持正则表达式格式输入）
    df3=concat_df_left(df_left=df2,df_right=df_ad_info,column="towncode")   # 根据所属街道的行政区划代码拼接筛选排序后的道路信息表格和行政区划表格，以获取所属街道的名称
    df4=filter_df_column(df=df3,columns=["name_road","township","name_district","name_city"])   # 筛选4个指定列（道路名称、所属街道名称、所属区县名称、所属城市名称）

    print(f"Selector:\n{dict_selector}\n\nDF_Road_Info:\n{df_road_info}\n\nDF_Ad_Info:\n{df_ad_info}\n\nDF_Result:\n{df4}\n\n")
    plot_road_info(df_road=df_road_info,df_ad=df_ad_info)   # 绘图显示道路分布
    output_df_excel(df_list=[df4,df3],sheet_list=["Result_Demo","Temp_Demo"],file_path=f"./Excel_Result_Demo#{CITY}.xlsx")
    df_excel=pd.read_excel(io=f"./Excel_Result_Demo#{CITY}.xlsx",sheet_name=0)
    print(f"{df_excel}")



    # 使用说明和注意事项区域===============================================================================================
    # 以上功能函数除sort_road_location和plot_road_info外均设计为针对dataframe数据结构的通用操作，可使用于道路信息表格和行政区划信息表格！！！
    # 以上功能函数除plot_road_info和output_df_excel外均返回经过处理的dataframe的副本，不修改传入参数指定的原始dataframe内容！！！
    # 绘图功能函数plot_road_info的传入参数仅支持从CSV文件读取的原始版本的道路信息表格和行政区划信息表格！！！
    # 针对道路信息表格（存储在DF_Road_Info#xxxxxx.csv文件中）和行政区划信息表格（存储在DF_AD_Info#xxxxxx.csv文件中）的列名解释（选题名称的列其含义完全相同）：
    dict_column_label_explanation={
        "id":"高德地图标识道路（一类地名）的唯一id",
        "name_road":"道路的规范名称",  # 经过处理，属于相同街道的同名道路以“#2”、“#3”等后缀添加在名称末尾用作区分
        "location_road":"道路的地理坐标（经纬度）", # 使用接近道路中段的某一地点的经纬度坐标近似表示道路的地理位置
        "typecode":"高德地图记录的道路类型代码", # 190301、190306、190307、190310分别表示道路、立交桥、桥梁、隧道（同一道路可能属于多种类型，对应多个类型代码使用“|”作为分隔符）
        "name_type":"道路所属类型的名称（亦可视作道路的规范化后缀）",  # 经过对道路规范化名称的字符串解析得到，含义相较于name_type更加细化
        "towncode":"（道路所属）街道级行政区的12位行政区划代码",    # 小概率异常：若该12位代码的后6位均为0，则表示对应道路或街道级行政区的12位行政区划代码暂时未知
        "township":"（道路所属）街道级行政区的规范化名称",
        "adcode_district":"（道路所属）区县级行政区的6位行政区划代码",
        "name_district":"（道路所属）区县级行政区的规范化名称",
        "address":"道路的详细地址",    # 对于道路而言该字段的取值绝大多数与其所属区县级行政区的规范化名称完全相同，但仍存在少数例外
        "count":"道路在调用高德地图API搜索过程中被发现的次数",  # 无效的闲置字段
        "source":"道路在调用高德地图API搜索过程中是否由关键词搜索得到", # 除绘图功能可能使用外无效的闲置字段
        "location_town":"街道级行政区的地理坐标（经纬度）",
        "location_district":"区县级行政区的地理坐标（经纬度）",
        "adcode_city":"城市级行政区的6位行政区划代码",
        "citycode":"城市级行政区的电话号码前缀",
        "name_city":"城市级行政区的规范化名称",
        "location_city":"城市级行政区的地理坐标（经纬度）",
    }