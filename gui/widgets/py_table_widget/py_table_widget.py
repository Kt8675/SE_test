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

import csv
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT STYLE
# ///////////////////////////////////////////////////////////////
from . style import *

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////
class PyTableWidget(QTableWidget):
    def __init__(
        self, 
        radius = 8,
        color = "#FFF",
        bg_color = "#444",
        selection_color = "#FFF",
        header_horizontal_color = "#333",
        header_vertical_color = "#444",
        bottom_line_color = "#555",
        grid_line_color = "#555",
        scroll_bar_bg_color = "#FFF",
        scroll_bar_btn_color = "#3333",
        context_color = "#00ABE8"
    ):
        super().__init__()
       # Columns / Header
        self.column_0 = QTableWidgetItem()
        self.column_0.setTextAlignment(Qt.AlignCenter)
        
        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("省")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("市")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("区/县")

        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignCenter)
        self.column_4.setText("街/巷/路/道")

        # Set column
        self.setHorizontalHeaderItem(0, self.column_0)
        self.setHorizontalHeaderItem(1, self.column_1)
        self.setHorizontalHeaderItem(2, self.column_2)
        self.setHorizontalHeaderItem(3, self.column_3)
        self.setHorizontalHeaderItem(4, self.column_4)
        self.setColumnWidth(0, 10)
        self.turn = False   # 记录是否全部勾选（有小bug，但只要操作范围局限在手动勾选checkbox或selectall就没问题）

        # PARAMETERS

        # SET STYLESHEET
        self.set_stylesheet(
            radius,
            color,
            bg_color,
            header_horizontal_color,
            header_vertical_color,
            selection_color,
            bottom_line_color,
            grid_line_color,
            scroll_bar_bg_color,
            scroll_bar_btn_color,
            context_color
        )

    # SET STYLESHEET
    def set_stylesheet(
        self,
        radius,
        color,
        bg_color,
        header_horizontal_color,
        header_vertical_color,
        selection_color,
        bottom_line_color,
        grid_line_color,
        scroll_bar_bg_color,
        scroll_bar_btn_color,
        context_color
    ):
        # APPLY STYLESHEET
        style_format = style.format(
            _radius = radius,          
            _color = color,
            _bg_color = bg_color,
            _header_horizontal_color = header_horizontal_color,
            _header_vertical_color = header_vertical_color,
            _selection_color = selection_color,
            _bottom_line_color = bottom_line_color,
            _grid_line_color = grid_line_color,
            _scroll_bar_bg_color = scroll_bar_bg_color,
            _scroll_bar_btn_color = scroll_bar_btn_color,
            _context_color = context_color
        )
        self.setStyleSheet(style_format)

    def checkbox_clicked(self):
        # 打印出当前勾选框的状态
        sender = self.sender()
        if sender.isChecked():
            # print("Checked")
            pass
        else:
            # print("Unchecked")
            self.turn = False

    
    def select_all(self):
        # 在有勾选框未被勾选时，按下按钮设置所有勾选框为选中状态
        if not self.turn:
            for row in range(self.rowCount()):
                checkbox = self.cellWidget(row, 0)
                checkbox.setChecked(True)
                self.turn = True
        # 在有勾选框被勾选时，按下按钮设置所有勾选框为未选中状态
        else:
            for row in range(self.rowCount()):
                checkbox = self.cellWidget(row, 0)
                checkbox.setChecked(False)
                self.turn = False

    # def set_data(self, filter_data):
        
    def get_data(self):
        # 将勾选的数据保存为csv文件
        data = []
        i = 0
        
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        # print('file_path:' + dir_path)
        if dir_path:
            for row in range(self.rowCount()):
                if self.cellWidget(row, 0).isChecked():
                    data.append([])
                    for j in range(1, 5):
                        data[i].append(self.item(row, j).text())
                    
                    i += 1
                else:
                    pass
            with open(os.path.join(dir_path, 'data.csv'), 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            
            # print("data saved")
        # return data
    

    def set_data(self, data_list:list):
        self.clear()
        self.setRowCount(0) 
        # print(data_list)
        # print('set data')
        # print(data_list)
        if len(data_list)==0 or data_list[0]==[]:
            return
        for data in data_list:
            row_number = self.rowCount()
            self.insertRow(row_number) # Insert row
            checkbox = QCheckBox()
            self.setCellWidget(row_number, 0, checkbox)
            checkbox.clicked.connect(self.checkbox_clicked)
            # print(data)
            self.setItem(row_number, 1, QTableWidgetItem(data[0]))
            self.setItem(row_number, 2, QTableWidgetItem(data[1]))
            self.setItem(row_number, 3, QTableWidgetItem(data[2]))
            self.setItem(row_number, 4, QTableWidgetItem(data[3]))
            if self.rowCount() >= 100:  # 目前只允许最多显示1000条数据，后面有时间再整多页面显示
                break
        self.viewport().update()  # 强制更新表格显示
        return