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
            }
        """)
        self.page_3_layout = QVBoxLayout(self.page_llm)
        self.page_3_layout.setObjectName(u"page_3_layout")

        # ModelScope API Key 设置区域
        self.api_frame = QFrame(self.page_llm)
        self.api_frame.setFrameShape(QFrame.StyledPanel)
        self.api_frame.setFrameShadow(QFrame.Raised)
        self.api_layout = QHBoxLayout(self.api_frame)

        self.api_label = QLabel("ModelScope API Key:")
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("请输入 API Key")
        self.api_input.setMinimumHeight(30)
        self.api_input.setStyleSheet("font-size: 14px; padding: 4px;")
        self.api_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.api_save_btn = QPushButton("保存")
        self.api_save_btn.setMinimumWidth(80)

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
        self.prompt_hint_label.setStyleSheet("font-size: 14px;")
        self.prompt_hint = QComboBox()
        self.prompt_hint.setMinimumHeight(32)
        self.prompt_hint.setStyleSheet("font-size: 14px;")
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
        self.chat_input.setStyleSheet("font-size: 14px; padding: 6px;")

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
        self.page_fetch_data = QWidget()
        self.page_fetch_data.setObjectName(u"page_fetch_data")
        self.page_fetch_data.setStyleSheet(u"""
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
            }
        """)
        self.page_fetch_data_layout = QVBoxLayout(self.page_fetch_data)

        # 配置区域 Frame
        self.config_frame = QFrame(self.page_fetch_data)
        self.config_frame.setFrameShape(QFrame.StyledPanel)
        self.config_frame.setFrameShadow(QFrame.Raised)
        self.config_layout_GD = QVBoxLayout(self.config_frame)
        self.config_layout_GD.setSpacing(8)
        
        # 行政区划代码输入
        self.city_code_layout = QHBoxLayout()
        self.city_code_label = QLabel("行政区划代码:")
        self.city_code_input = QLineEdit()
        self.city_code_input.setPlaceholderText("例如: 110000 (北京)")
        self.city_code_layout.addWidget(self.city_code_label)
        self.city_code_layout.addWidget(self.city_code_input)
        
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
        
        # 输出日志区域
        self.log_frame = QFrame(self.page_fetch_data)
        self.log_frame.setFrameShape(QFrame.StyledPanel)
        self.log_layout = QVBoxLayout(self.log_frame)
        
        self.log_label = QLabel("执行日志:")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        # 为日志区域添加特定样式
        self.log_output.setStyleSheet("""
            font-family: 'Courier New'; 
            font-size: 12px;
            background-color: #1e2229;  # 添加背景色
            border: 1px solid #444;    # 保持边框一致
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

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Welcome To PyOneDark GUI", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Custom Widgets Page", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Here will be all the custom widgets, they will be added over time on this page.\n"
"I will try to always record a new tutorial when adding a new Widget and updating the project on Patreon before launching on GitHub and GitHub after the public release.", None))
        self.empty_page_label.setText(QCoreApplication.translate("MainPages", u"Empty Page", None))
    # retranslateUi

