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

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
from . functions_main_window import *
import sys
import os
# from gui.widgets.py_combox import ComboBox

from gui.uis.windows.main_window.llm_function import save_api_key, load_api_key, handle_llm_query


# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *

# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Home",
            "btn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon" : "icon_widgets.svg",
            "btn_id" : "btn_widgets",
            "btn_text" : "Display page",
            "btn_tooltip" : "Show custom widgets",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_modelscope.svg",
            "btn_id" : "btn_modelscope",
            "btn_text" : "ModelscopeConfig",
            "btn_tooltip" : "Modelscope page",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_file.svg",
            "btn_id" : "btn_fetch_data",
            "btn_text" : "Fetch Roads data",
            "btn_tooltip" : "Fetch Roads data",
            "show_top" : True,
            "is_active" : False
        },
        # {
        #     "btn_icon" : "icon_folder_open.svg",
        #     "btn_id" : "btn_open_file",
        #     "btn_text" : "Open File",
        #     "btn_tooltip" : "Open file",
        #     "show_top" : True,
        #     "is_active" : False
        # },
        # {
        #     "btn_icon" : "icon_save.svg",
        #     "btn_id" : "btn_save",
        #     "btn_text" : "Save File",
        #     "btn_tooltip" : "Save file",
        #     "show_top" : True,
        #     "is_active" : False
        # },
        # {
        #     "btn_icon" : "icon_info.svg",
        #     "btn_id" : "btn_info",
        #     "btn_text" : "Information",
        #     "btn_tooltip" : "Open informations",
        #     "show_top" : False,
        #     "is_active" : False
        # },
        # {
        #     "btn_icon" : "icon_settings.svg",
        #     "btn_id" : "btn_settings",
        #     "btn_text" : "Settings",
        #     "btn_tooltip" : "Open settings",
        #     "show_top" : False,
        #     "is_active" : False
        # }
    ]

     # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////w
    add_title_bar_menus = [
        {
            "btn_icon" : "icon_search.svg",
            "btn_id" : "btn_search",
            "btn_tooltip" : "Search",
            "is_active" : False
        },
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_top_settings",
            "btn_tooltip" : "Top settings",
            "is_active" : False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.menu_1,
            title = "Settings Left Column",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # PY LINE EDIT
        self.line_edit = PyLineEdit(
            text = "",
            place_holder_text = "输入关键词以筛选",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.line_edit.setMinimumHeight(30)
        self.line_edit.editingFinished.connect(self.line_edit_filter_data)
        # TOGGLE BUTTON
        # self.toggle_button = PyToggle(
        #     width = 50,
        #     bg_color = self.themes["app_color"]["dark_two"],
        #     circle_color = self.themes["app_color"]["icon_color"],
        #     active_color = self.themes["app_color"]["context_color"]
        # ) 


        # self.combo_view = ComboBox(self).combo_layout
        # self.combo = ComboBox(self)
        self.data = (None, None, None)
        self.data_list = []
        self.province_combo = QComboBox(self)
        self.city_combo = QComboBox(self)
        self.region_combo = QComboBox(self)
        self.province_combo.currentTextChanged.connect(self.init_city_combo)
        # self.province_combo.currentTextChanged.connect(self.select_and_filter_data)
        self.city_combo.currentTextChanged.connect(self.init_region_combo)
        # self.city_combo.currentTextChanged.connect(self.select_and_filter_data)
        self.region_combo.currentTextChanged.connect(self.pass_data)
        self.region_combo.currentTextChanged.connect(self.select_and_filter_data)
        # self.region_combo.currentTextChanged.connect(self.test)
        self.init_privince_combo()
        # self.province_combo, self.city_combo = self.combo.province_combo, combo.city_combo

        # TABLE WIDGETS
        self.table_widget = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.table_widget.setColumnCount(5)
        
        # self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # # Columns / Header
        # self.column_0 = QTableWidgetItem()
        # self.column_0.setTextAlignment(Qt.AlignCenter)
        
        # self.column_1 = QTableWidgetItem()
        # self.column_1.setTextAlignment(Qt.AlignCenter)
        # self.column_1.setText("省")

        # self.column_2 = QTableWidgetItem()
        # self.column_2.setTextAlignment(Qt.AlignCenter)
        # self.column_2.setText("市")

        # self.column_3 = QTableWidgetItem()
        # self.column_3.setTextAlignment(Qt.AlignCenter)
        # self.column_3.setText("区/县")

        # self.column_4 = QTableWidgetItem()
        # self.column_4.setTextAlignment(Qt.AlignCenter)
        # self.column_4.setText("街/巷/路/道")

        # # Set column
        # self.table_widget.setHorizontalHeaderItem(0, self.column_0)
        # self.table_widget.setHorizontalHeaderItem(1, self.column_1)
        # self.table_widget.setHorizontalHeaderItem(2, self.column_2)
        # self.table_widget.setHorizontalHeaderItem(3, self.column_3)
        # self.table_widget.setHorizontalHeaderItem(4, self.column_4)
        # self.table_widget.setColumnWidth(0, 10)

        # 控制表格列的宽度：第一列根据内容自动计算，1-4列平分剩余空间
        self.table_widget.horizontalHeader().setSectionResizeMode(0,  QHeaderView.ResizeToContents)
        for i in range(1, 5):
            self.table_widget.horizontalHeader().setSectionResizeMode(i,  QHeaderView.Stretch)

        # 设置内容
        # self.table_widget.setData(self.data)
        # data = []
        # for i in range(100):
        #     data.append(["广东省", "深圳市", "南山区", "南山大道"])
        
        # self.table_widget.set_data(data)

        # select_all_button = QPushButton("Select All", self)
        # select_all_button.clicked.connect(self.table_widget.select_all)

        # 全选/全不选 按钮
        self.select_all_button = QPushButton("Select All", self)
        self.select_all_button.clicked.connect(self.table_widget.select_all)

        # 获取数据，输出为csv文件
        self.output_button = QPushButton("Output", self)
        self.output_button.clicked.connect(self.table_widget.get_data)

        self.output_all_button = QPushButton("Output All", self)
        self.output_all_button.clicked.connect(self.table_widget.get_data_all)
        self.previous_button = QPushButton("Previous", self)
        self.previous_button.clicked.connect(self.table_widget.previous)
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.table_widget.next)
        self.previous_button.setText("Previous")
        self.next_button.setText("Next")

        column_names = ["ID", "省", "市", "区/县", "街道"]
        self.table_widget.setHorizontalHeaderLabels(column_names)
        # ADD WIDGETS

        self.ui.load_pages.row_3_layout.addWidget(self.province_combo)
        self.ui.load_pages.row_3_layout.addWidget(self.city_combo)
        self.ui.load_pages.row_3_layout.addWidget(self.region_combo)
        # self.ui.load_pages.row_3_layout.addWidget(self.combo_view)
        self.ui.load_pages.row_4_layout.addWidget(self.line_edit)
        self.ui.load_pages.row_4_layout.addWidget(self.output_button)
        self.ui.load_pages.row_4_layout.addWidget(self.output_all_button)
        self.ui.load_pages.row_5_layout.addWidget(self.select_all_button)
        self.ui.load_pages.row_5_layout.addWidget(self.table_widget)
        self.ui.load_pages.row_5_layout.addWidget(self.previous_button)
        self.ui.load_pages.row_5_layout.addWidget(self.next_button)
        
        # RIGHT COLUMN
        # ///////////////////////////////////////////////////////////////

        # BTN 1
        # self.right_btn_1 = PyPushButton(
        #     text="Show Menu 2",
        #     radius=8,
        #     color=self.themes["app_color"]["text_foreground"],
        #     bg_color=self.themes["app_color"]["dark_one"],
        #     bg_color_hover=self.themes["app_color"]["dark_three"],
        #     bg_color_pressed=self.themes["app_color"]["dark_four"]
        # )
        # self.icon_right = QIcon(Functions.set_svg_icon("icon_arrow_right.svg"))
        # self.right_btn_1.setIcon(self.icon_right)
        # self.right_btn_1.setMaximumHeight(40)
        # self.right_btn_1.clicked.connect(lambda: MainFunctions.set_right_column_menu(
        #     self,
        #     self.ui.right_column.menu_2
        # ))
        # self.ui.right_column.btn_1_layout.addWidget(self.right_btn_1)

        # BTN 2
        # self.right_btn_2 = PyPushButton(
        #     text="Show Menu 1",
        #     radius=8,
        #     color=self.themes["app_color"]["text_foreground"],
        #     bg_color=self.themes["app_color"]["dark_one"],
        #     bg_color_hover=self.themes["app_color"]["dark_three"],
        #     bg_color_pressed=self.themes["app_color"]["dark_four"]
        # )
        # self.icon_left = QIcon(Functions.set_svg_icon("icon_arrow_left.svg"))
        # self.right_btn_2.setIcon(self.icon_left)
        # self.right_btn_2.setMaximumHeight(40)
        # self.right_btn_2.clicked.connect(lambda: MainFunctions.set_right_column_menu(
        #     self,
        #     self.ui.right_column.menu_1
        # ))
        # self.ui.right_column.btn_2_layout.addWidget(self.right_btn_2)

        saved_key = load_api_key()
        self.ui.load_pages.api_input.setText(saved_key)
        # 连接按钮-Modelscope模型页（page_llm）
        self.ui.load_pages.send_btn.clicked.connect(self.on_send_clicked)
        self.ui.load_pages.api_save_btn.clicked.connect(self.on_save_api_key)

        # 连接按钮-获取数据页（page_fetch_data）
        self.ui.load_pages.execute_btn_GD.clicked.connect(self.fetch_roads_data)

        self.table_widget = self.table_widget  # 显式提醒自己这个组件已注册


        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////
    
    
    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)

    # def select_all(self):
    #     self.table_widget.select_all()

    