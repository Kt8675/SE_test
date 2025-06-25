# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *
from gui.widgets import *
from gui.core.json_themes import Themes
from gui.uis.windows.main_window.fetch_roads_data import get_road_poi, get_road_tian
import threading

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.welcome_base = QFrame(self.page_1)
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setMinimumSize(QSize(300, 150))
        self.welcome_base.setMaximumSize(QSize(300, 150))
        self.welcome_base.setFrameShape(QFrame.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Raised)
        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName(u"center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QFrame(self.welcome_base)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(300, 120))
        self.logo.setMaximumSize(QSize(300, 120))
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Raised)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.center_page_layout.addWidget(self.logo)

        self.label = QLabel(self.welcome_base)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.center_page_layout.addWidget(self.label)


        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignHCenter)

        self.pages.addWidget(self.page_1)

        # ============================================
        # 页面2内容 - 数据展示
        # ============================================
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        # self.row_1_layout = QHBoxLayout()
        # self.row_1_layout.setObjectName(u"row_1_layout")

        # self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
#         self.page_3 = QWidget()
#         self.page_3.setObjectName(u"page_3")
#         self.page_3.setStyleSheet(u"QFrame {\n"
# "	font-size: 16pt;\n"
# "}")
#         self.page_3_layout = QVBoxLayout(self.page_3)
#         self.page_3_layout.setObjectName(u"page_3_layout")
#         self.empty_page_label = QLabel(self.page_3)
#         self.empty_page_label.setObjectName(u"empty_page_label")
#         self.empty_page_label.setFont(font)
#         self.empty_page_label.setAlignment(Qt.AlignCenter)

#         self.page_3_layout.addWidget(self.empty_page_label)

#         self.pages.addWidget(self.page_3)
        # ============================================
        # 页面3内容 - Modelscope模型对话
        # ============================================
        self.page_llm = QWidget()
        self.page_llm.setObjectName(u"page_llm")
        self.page_llm.setStyleSheet(u"""
            QFrame {
                font-size: 20pt;
            }
            QLabel, QLineEdit, QPushButton, QTextEdit {
                color: #f0f0f0;
                background-color: #2a2d35;
            }
            QTextEdit {
                border: 1px solid #444;
                padding: 6px;
            }
            QLineEdit {
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #3b7cff;
                color: white;
                border-radius: 4px;
                padding: 6px;
                font-size: 20px;              
            }
        """)
        self.page_3_layout = QVBoxLayout(self.page_llm)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.page_3_font_str = "20px"

        # ModelScope API Key 设置区域
        self.api_frame = QFrame(self.page_llm)
        self.api_frame.setFrameShape(QFrame.StyledPanel)
        self.api_frame.setFrameShadow(QFrame.Raised)
        self.api_layout = QHBoxLayout(self.api_frame)

        self.model_selcet = QComboBox()
        self.model_selcet.setMinimumHeight(32)
        self.model_selcet.setStyleSheet(f"font-size: {self.page_3_font_str};")
        self.model_selcet.addItems([
            "ModelScope",
            "DeepSeek"
        ])
        self.api_label = QLabel("API Key:")

        themes = Themes()
        self.themes = themes.items
        self.api_input = PyLineEdit(
            text = "",
            place_holder_text = "请输入 API Key:",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.api_input.setMinimumHeight(30)
        self.api_input.setStyleSheet(f"font-size: {self.page_3_font_str}; padding: 4px;")
        self.api_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.api_save_btn = QPushButton("保存")
        self.api_save_btn.setMinimumWidth(80)

        self.api_layout.addWidget(self.model_selcet)
        self.api_layout.addWidget(self.api_label)
        self.api_layout.addWidget(self.api_input)
        self.api_layout.addWidget(self.api_save_btn)

        # 聊天区域 Frame
        self.chat_frame = QFrame(self.page_llm)
        self.chat_frame.setFrameShape(QFrame.StyledPanel)
        self.chat_frame.setFrameShadow(QFrame.Raised)
        self.chat_layout = QVBoxLayout(self.chat_frame)

        # 聊天显示区域（可滚动）
        self.chat_display_scroll = QScrollArea()
        self.chat_display_scroll.setWidgetResizable(True)
        self.chat_display_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.chat_display_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.chat_display_container = QWidget()
        self.chat_display_layout = QVBoxLayout(self.chat_display_container)
        self.chat_display_layout.setAlignment(Qt.AlignTop)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_display_layout.addWidget(self.chat_display)
        self.chat_display_scroll.setWidget(self.chat_display_container)

        # 提示词选择区域
        self.prompt_hint_frame = QFrame(self.page_llm)
        self.prompt_hint_layout = QHBoxLayout(self.prompt_hint_frame)

        self.prompt_hint_label = QLabel("提示词选择：")
        self.prompt_hint_label.setStyleSheet(f"font-size: {self.page_3_font_str};")
        self.prompt_hint = QComboBox()
        self.prompt_hint.setMinimumHeight(32)
        self.prompt_hint.setStyleSheet(f"font-size: {self.page_3_font_str};")
        self.prompt_hint.addItems([
            "",
            "现在请你根据我的输入，获取所有可能的街道信息，输入其规范名称。输入：",
            "请标准化以下地址格式：",
            "下面这条路有没有别的叫法？",
            "在深圳市内，下面这几条路属于哪个区？"
        ])

        self.prompt_hint_layout.addWidget(self.prompt_hint_label)
        self.prompt_hint_layout.addWidget(self.prompt_hint)

        # 输入区域
        self.chat_input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("请输入你的问题...")
        self.chat_input.setMinimumHeight(36)
        self.chat_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chat_input.setStyleSheet(f"font-size: {self.page_3_font_str}; padding: 6px;")

        self.send_btn = QPushButton("发送")
        self.send_btn.setMinimumWidth(80)

        self.chat_input_layout.addWidget(self.chat_input, 8)
        self.chat_input_layout.addWidget(self.send_btn, 2)

        # 添加至聊天布局
        self.chat_layout.addWidget(self.prompt_hint_frame)
        self.chat_layout.addWidget(self.chat_display_scroll, 7)
        self.chat_layout.addLayout(self.chat_input_layout, 1)

        # 布局整合
        self.page_3_layout.addWidget(self.api_frame)
        self.page_3_layout.addWidget(self.chat_frame)

        self.pages.addWidget(self.page_llm)

        # ============================================
        # 页面4内容 - POI数据获取工具
        # ============================================
        
        # 页面4Widget与layout的定义：
        self.page_4_font_str = "20px"
        self.page_fetch_data = QWidget()
        self.page_fetch_data.setObjectName(u"page_fetch_data")
        self.page_fetch_data.setStyleSheet(u"""
            QFrame {
                font-size: 20px;
            }
            QLabel, QLineEdit, QPushButton, QTextEdit {
                color: #f0f0f0;
                background-color: #2a2d35;
            }
            QTextEdit {
                border: 1px solid #444;
                padding: 6px;
            }
            QLineEdit {
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #3b7cff;
                color: white;
                border-radius: 4px;
                padding: 6px;
                font-size: 20px;
            }
        """)
        self.page_fetch_data_layout = QVBoxLayout(self.page_fetch_data)

        # 配置区域 Frame
        self.config_frame = QFrame(self.page_fetch_data)
        self.config_frame.setFrameShape(QFrame.StyledPanel)
        self.config_frame.setFrameShadow(QFrame.Raised)
        self.config_layout_GD = QVBoxLayout(self.config_frame)
        self.config_layout_GD.setSpacing(8)
        
        # api工具切换
        self.fetch_tool_combox = QComboBox()
        self.fetch_tool_combox.addItem("高德API")
        self.fetch_tool_combox.addItem("天地图API")
        self.fetch_tool_combox.currentTextChanged.connect(self.change_fetch_tool)
        
        # 行政区划代码输入
        self.city_code_layout = QHBoxLayout()
        self.city_code_label = QLabel("行政区划代码:")
        self.city_code_input = QLineEdit()
        self.city_code_input.setPlaceholderText("例如: 110000 (北京)")
        self.city_code_layout.addWidget(self.city_code_label)
        self.city_code_layout.addWidget(self.city_code_input)
        self.city_code_layout.addWidget(self.fetch_tool_combox)
        
        # 输出路径选择
        self.output_path_layout = QHBoxLayout()
        self.output_path_label = QLabel("输出路径:")
        self.output_path_input = QLineEdit()
        self.output_path_input.setPlaceholderText("留空使用默认路径")
        # self.output_path_btn = QPushButton("浏览...")
        # self.output_path_btn.setFixedWidth(80)
        self.output_path_layout.addWidget(self.output_path_label)
        self.output_path_layout.addWidget(self.output_path_input)
        # self.output_path_layout.addWidget(self.output_path_btn)
        
        # 高德API Key，相关组件后加上`_GD`后缀用于标识
        self.api_key_layout_GD = QHBoxLayout()
        self.api_key_label_GD= QLabel("高德API Key:")
        self.api_key_input_GD = QLineEdit()
        self.api_key_input_GD.setPlaceholderText("留空使用默认Key")
        self.api_key_layout_GD.addWidget(self.api_key_label_GD)
        self.api_key_layout_GD.addWidget(self.api_key_input_GD)
        
        # 添加到配置区域
        self.config_layout_GD.addLayout(self.city_code_layout)
        self.config_layout_GD.addLayout(self.output_path_layout)
        self.config_layout_GD.addLayout(self.api_key_layout_GD)
        
        # 执行按钮区域
        self.execute_frame_GD = QFrame(self.page_fetch_data)
        self.execute_layout_GD = QHBoxLayout(self.execute_frame_GD)
        self.execute_layout_GD.setContentsMargins(0, 0, 0, 0)
        
        self.execute_btn_GD = QPushButton("获取POI数据")
        self.execute_btn_GD.setFixedHeight(40)
        self.execute_layout_GD.addWidget(self.execute_btn_GD)
        self.execute_btn_GD.clicked.connect(self.fetch_roads_data)
        # 天地图api
        # self.api_key_layout_TM = QHBoxLayout()
        # self.api_key_label_TM= QLabel("天地图API 查询条件:")
        # self.api_key_input_TM = QLineEdit()
        # self.api_key_input_TM.setPlaceholderText("留空使用默认Key")
        # self.api_key_layout_TM.addWidget(self.api_key_label_GD)
        # self.api_key_layout_TM.addWidget(self.api_key_input_GD)
        # self.api_key_input_TM.setVisible(False)
        
        # 执行按钮区域
        # self.execute_frame_TM = QFrame(self.page_fetch_data)
        # self.execute_layout_TM = QHBoxLayout(self.execute_frame_TM)
        # self.execute_layout_TM.setContentsMargins(0, 0, 0, 0)
        
        # self.execute_btn_TM = QPushButton("获取数据")
        # self.execute_btn_TM.setFixedHeight(40)
        # self.execute_layout_TM.addWidget(self.execute_btn_GD)
        # self.execute_layout_TM.setVisible(False)

        # 输出日志区域
        self.log_frame = QFrame(self.page_fetch_data)
        self.log_frame.setFrameShape(QFrame.StyledPanel)
        self.log_layout = QVBoxLayout(self.log_frame)
        
        self.log_label = QLabel("执行日志:")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        # 为所有控件动态设置字体
        self.city_code_label.setStyleSheet(f"font-size: {self.page_4_font_str};")
        self.city_code_input.setStyleSheet(f"font-size: {self.page_4_font_str}; padding: 4px;")
        self.output_path_label.setStyleSheet(f"font-size: {self.page_4_font_str};")
        self.output_path_input.setStyleSheet(f"font-size: {self.page_4_font_str}; padding: 4px;")
        self.api_key_label_GD.setStyleSheet(f"font-size: {self.page_4_font_str};")
        self.api_key_input_GD.setStyleSheet(f"font-size: {self.page_4_font_str}; padding: 4px;")
        self.log_label.setStyleSheet(f"font-size: {self.page_4_font_str};")
        self.log_output.setStyleSheet(f"""
            font-family: 'Courier New';
            font-size: {self.page_4_font_str};
            background-color: #1e2229;
            border: 1px solid #444;
        """)
        
        self.log_layout.addWidget(self.log_label)
        self.log_layout.addWidget(self.log_output)
        
        # 将页面四添加到主布局，命名为page_fetch_data
        self.page_fetch_data_layout.addWidget(self.config_frame)
        self.page_fetch_data_layout.addWidget(self.execute_frame_GD)
        self.page_fetch_data_layout.addWidget(self.log_frame, 1)  # 日志区域占据剩余空间

        self.pages.addWidget(self.page_fetch_data)

        # 
        QMetaObject.connectSlotsByName(MainPages)

        # 定义整个页面
        self.main_pages_layout.addWidget(self.pages)

        # self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)
    # setupUi

    def fetch_roads_data(self): 
        self.road_poi_process = None  # 存储进程对象
        self.road_poi_timer = None     # 存储定时器对象
        self.thread = None          # 存储线程对象

        self.execute_btn_GD.setEnabled(False)
        self.city_code_input.setEnabled(False)
        self.output_path_input.setEnabled(False)
        self.api_key_input_GD.setEnabled(False)
        # 显示正在读取的状态
        self.log_output.append("正在获取道路数据，请稍候...获取数据期间不能修改参数信息")
        code = self.city_code_input.text()
        data_path = self.output_path_input.text()
        apikey = self.api_key_input_GD.text()
        try:
            def run_fetch_task():
                self.road_poi_process = get_road_poi(code, data_path, apikey)
                stdout, stderr = self.road_poi_process.communicate()
            # 显示结果
                self.log_output.append(f"标准流输出：\n{stdout}\n错误流输出：\n{stderr}")
            # 采用线程启动
            thread = threading.Thread(target=run_fetch_task)
            thread.start()
            self.execute_btn_GD.setText("终止数据获取")
            self.execute_btn_GD.clicked.disconnect()
            self.execute_btn_GD.clicked.connect(self.close_thread)
            self.enable_inputs()
            # 设置定时器检查进程状态
            # self.road_poi_timer = QTimer()
            # self.road_poi_timer.timeout.connect(self.check_road_poi_process)
            # self.road_poi_timer.start(500)  # 每500ms检查一次
            # 采用定时器会导致进程阻塞（不清楚原因）

            
        except Exception as e:
            self.log_output.append(f"启动进程失败: {str(e)}")
            self.enable_inputs()

    def close_thread(self):
        self.road_poi_process.terminate()
        # print('closed')
        self.execute_btn_GD.setText("获取POI数据")
        self.execute_btn_GD.clicked.disconnect()
        self.execute_btn_GD.clicked.connect(self.fetch_roads_data)

    # def check_road_poi_process(self):
    #     """检查非阻塞进程状态的定时器回调"""
    #     print("进程状态检查")
    #     print(self.road_poi_process.poll())
    #     if self.road_poi_process.poll() is not None:  # 进程已完成
    #         self.road_poi_timer.stop()
            
    #         # 获取进程输出
    #         stdout, stderr = self.road_poi_process.communicate()
    #         print(stdout)
    #         # 显示结果
    #         self.log_output.append(f"标准流输出：\n{stdout}\n错误流输出：\n{stderr}")
    #         # 恢复按钮状态
    #         self.enable_inputs()
    #     else:
    #         stdout, stderr = self.road_poi_process.communicate()
    #         print(stdout)
    #         print(stderr)

    def enable_inputs(self):
        """恢复输入控件和按钮的状态"""
        self.execute_btn_GD.setEnabled(True)
        self.city_code_input.setEnabled(True)
        self.output_path_input.setEnabled(True)
        self.api_key_input_GD.setEnabled(True)

    def closeEvent(self, event):
        if self.road_poi_process and self.road_poi_process.poll() is None:
            self.road_poi_process.terminate()
        if self.road_poi_timer and self.road_poi_timer.isActive():
            self.road_poi_timer.stop()
        event.accept()

    def fetch_roads_data_TM(self):
        # print("***************************")
        code = self.city_code_input.text()
        data_path = self.output_path_input.text()
        apikey = self.api_key_input_GD.text()
        stdout = get_road_tian(code, data_path, apikey) # 返回值为：（标准流输出，错误流输出）
        self.log_output.append(f"标准流输出：\n{stdout}")

    def change_fetch_tool(self, text):
        if text == "高德API":
            # self.api_key_layout_GD.setVisible(True)
            
            self.city_code_label.setText("行政区划代码:")
            self.city_code_input.setPlaceholderText("例如: 110000 (北京)")
            self.api_key_label_GD.setText("高德API Key:")
            self.api_key_input_GD.setPlaceholderText("留空使用默认Key")
            self.execute_btn_GD.clicked.disconnect()
            # print("**** changed to GD Map ****")
            self.execute_btn_GD.setText("获取POI数据")
            self.execute_btn_GD.clicked.connect(self.fetch_roads_data)
            # self.api_key_input_GD.setPlaceholderText("留空使用默认Key")
            None
        else:
            self.city_code_label.setText("城市编码:")
            self.city_code_input.setPlaceholderText("例如: 156440300(深圳)")
            self.api_key_label_GD.setText("筛选关键词:")
            self.execute_btn_GD.setText("获取天地图数据")
            self.api_key_input_GD.setPlaceholderText("")
            self.execute_btn_GD.clicked.disconnect()
            # print("**** changed to Tian Map ****")
            self.execute_btn_GD.setText("获取天地图数据")
            self.execute_btn_GD.clicked.connect(self.fetch_roads_data_TM)
            # self.api_key_input_GD.setPlaceholderText("留空使用默认Key")
            
    # change_fetch_tool
    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Welcome To PyOneDark GUI", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Custom Widgets Page", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Here will be all the custom widgets, they will be added over time on this page.\n"
"I will try to always record a new tutorial when adding a new Widget and updating the project on Patreon before launching on GitHub and GitHub after the public release.", None))
        self.empty_page_label.setText(QCoreApplication.translate("MainPages", u"Empty Page", None))
    # retranslateUi

