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
        # 页面 LLM
        self.page_llm = QWidget()
        self.page_llm.setObjectName(u"page_llm")
        self.page_llm.setStyleSheet(u"""
            QFrame {
                font-size: 16pt;
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
        self.pages.addWidget(self.page_llm)

        self.main_pages_layout.addWidget(self.pages)

        # self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)

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
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Welcome To PyOneDark GUI", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Custom Widgets Page", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Here will be all the custom widgets, they will be added over time on this page.\n"
"I will try to always record a new tutorial when adding a new Widget and updating the project on Patreon before launching on GitHub and GitHub after the public release.", None))
        self.empty_page_label.setText(QCoreApplication.translate("MainPages", u"Empty Page", None))
    # retranslateUi

