import csv
import os
from data.data import province_list, city_dict, region_dict

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////

class ComboBox(QWidget):
    def __init__(self, /, parent = ..., f = ..., *, modal = ..., windowModality = ..., enabled = ..., geometry = ..., frameGeometry = ..., normalGeometry = ..., x = ..., y = ..., pos = ..., frameSize = ..., size = ..., width = ..., height = ..., rect = ..., childrenRect = ..., childrenRegion = ..., sizePolicy = ..., minimumSize = ..., maximumSize = ..., minimumWidth = ..., minimumHeight = ..., maximumWidth = ..., maximumHeight = ..., sizeIncrement = ..., baseSize = ..., palette = ..., font = ..., cursor = ..., mouseTracking = ..., tabletTracking = ..., isActiveWindow = ..., focusPolicy = ..., focus = ..., contextMenuPolicy = ..., updatesEnabled = ..., visible = ..., minimized = ..., maximized = ..., fullScreen = ..., sizeHint = ..., minimumSizeHint = ..., acceptDrops = ..., windowTitle = ..., windowIcon = ..., windowIconText = ..., windowOpacity = ..., windowModified = ..., toolTip = ..., toolTipDuration = ..., statusTip = ..., whatsThis = ..., accessibleName = ..., accessibleDescription = ..., accessibleIdentifier = ..., layoutDirection = ..., autoFillBackground = ..., styleSheet = ..., locale = ..., windowFilePath = ..., inputMethodHints = ...):
        super().__init__()
        # 下拉框
        self.province_combo = QComboBox(self)
        self.city_combo = QComboBox(self)
        self.region_combo = QComboBox(self)
        self.province_combo.currentTextChanged.connect(self.init_city_combo)
        self.city_combo.currentTextChanged.connect(self.init_region_combo)

      
        self.init_privince_combo()
    
    def init_privince_combo(self):
        self.province_combo.addItem("选择省份")
        for prov in province_list:
            self.province_combo.addItem(prov)
    
    def init_city_combo(self, province):
        print('update city combo')
        self.city_combo.clear()
        if province == "选择省份" or province == " ":
            self.city_combo.addItem("选择城市")
            return
        if '市' in province or '行政区' in province:
            self.city_combo.addItem(province)
            # self.init_region_combo(province)
            # print('from province to region')
            return 
        city_list = city_dict[province]
        for city in city_list:
            self.city_combo.addItem(city)
    
    def init_region_combo(self, city):
        # print('update region combo, city  is ' + city)
        self.region_combo.clear()
        if city == "选择城市" or city == " ":
            # self.region_combo.clear()
            self.region_combo.addItem("选择区县")
            return
        region_list = region_dict[city]
        for region in region_list:
            self.region_combo.addItem(region)
            