# 城市地址路名库

## 介绍
该工作为SCUT 2024-2025学年度下学期《软件工程课程设计》提交项目。项目成员：陈嘉宇、蒋韧翔、金约汗、黄麒嘉。


### 题干信息
目前随着互联网及通信技术的发展，各类数据极具膨胀，为了准确对文本信息进行分析，需要依托中文词库进行分词解析，以提升语义识别的准确率，其中地名是很重要的词库来源，在地址路名中，包含路、大道、巷、街等后缀。
以某城市为例，可以通过官方网站访问获取，也可以通过地图API方式调用访问，或者通过第三方平台获取后，形成道路名称，所属街道，所属行政区，所在城市的格式文件。

### 参考资料
网络爬虫、自然语言处理

### 硬件要求：
PC机：4C8GB内存50GB硬盘

### 数据要求：
无

### 测试环境：
连接互联网

### 参考
前端可视化界面参考开源项目[PyOneDark](https://github.com/Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI)。


## 使用说明

### 环境

- Python 3.9+

进入指定环境后，执行以下指令：
```
pip install -r requirements.txt
```
随后，下载程序核心可执行文件`GetRoadPOI.exe`（[百度网盘链接](https://pan.baidu.com/s/1xsCe3NT_0iaMhTRC78w8lA?pwd=y7gm)），并将其放在主文件夹`SE_test/`中。

### 进入可视化界面

命令行进入主文件夹，执行以下指令：
```
python main.py
```

### 原始道路数据获取

点击左侧导航栏第四个界面，选择高德API，输入目标城市的行政区划代码（[行政区划代码查询](http://xzqh.mca.gov.cn/map)，或者询问软件内集成的大模型助手）、数据保存路径、高德API key（[申请高德API key](https://lbs.amap.com/)），点击按钮“获取POI数据”即可。以深圳市为例，数据获取时间在6小时左右，需要的高德API请求次数约为33000次。
![](figs\DataAccess.png)

### 道路信息展示与导出
使用这一功能前，请将上一步获取的数据移动到`SE_test/data`文件夹中，命名格式保持为`DF_行政区划代码`，比如`DF_440100`。随后，点击左侧导航栏第二个界面：
![](figs\DataPlaylist.png)
按照提示选择需要的城市的数据，点击`Output`可以导出。
![](figs\DataPlaylist2.png)
其中，`Output All`代表输出所有文件；`Select All`代表选择当前所有道路；`Previous`和`Next`分别代表上一页和下一页。

如果想要快速复现，可以使用提前获取好的道路数据（深圳市+广州市+东莞市，[百度网盘链接](https://pan.baidu.com/s/1mdl-E7cWW1IUCsICAtp8pA?pwd=7h9e)）放入`SE_test/data`文件夹中，以取代原始数据获取的步骤。

### 大模型助手
可配置DeepSeek和ModelScope的API，提供辅助，包括模糊搜索、行政区划查询等。点击左侧导航栏第二个界面，选择`DeepSeek`或者`ModelScope`，输入对应的`API Key`，在聊天框输入对话内容，点击`发送`。
![](figs\LLM.png)






