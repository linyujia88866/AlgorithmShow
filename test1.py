import copy
import sys

from PyQt5 import QtChart
from PyQt5.QtChart import (QChartView, QChart, QBarSeries, QBarSet,
                           QValueAxis)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QPushButton


def gen_random():
    import random

    # 生成10个随机数
    random_numbers = [random.randint(2, 100) for _ in range(10)]

    return random_numbers


class DemoChartBarSeries(QDialog):
    def __init__(self, parent=None):
        super(DemoChartBarSeries, self).__init__(parent)
        self.lay = None
        self.temp_btn = None
        self.insert_btn = None
        self.make_data = None
        self.bubble_btn = None
        self.chart_view = None
        self.chart = None
        self.timer = None
        self.bar_series = None
        self.bar_set_0 = None
        self.data = []
        self.temp = []
        self.min = []
        self.init_arr = []
        self.count = 0
        # 设置窗口标题
        self.setWindowTitle('排序算法柱状图演示')
        # 设置窗口大小
        self.resize(880, 560)

        self.create_chart()
        self.sorting = False

    def create_chart(self):
        # 创建条状单元
        self.bar_set_0 = QBarSet('排序前')

        self.init_arr = gen_random()
        self.bar_set_0.append(self.init_arr)

        # 条状图
        self.bar_series = QBarSeries()
        self.bar_series.setLabelsVisible(True)
        self.bar_series.setLabelsPosition(QtChart.QAbstractBarSeries.LabelsPosition.LabelsInsideEnd)
        self.bar_series.append(self.bar_set_0)

        # 创建图表
        self.chart = QChart()
        self.chart.addSeries(self.bar_series)
        # self.chart.setTitle('暂存')
        # self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 设置成动画显示

        # 设置横向坐标(X轴)
        # categories = ['一月', '二月', '三月', '四月', '五月', '六月']
        # axisX = QBarCategoryAxis()
        # axisX.append(categories)
        # self.chart.addAxis(axisX, Qt.AlignBottom)
        # self.bar_series.attachAxis(axisX)

        # 设置纵向坐标(Y轴)
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(axis_y)

        # 图例属性
        self.chart.legend().setVisible(False)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # 图表视图
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.lay = QGridLayout()
        self.setLayout(self.lay)

        self.bubble_btn = QPushButton("冒泡排序")
        self.insert_btn = QPushButton("插入排序")
        self.select_btn = QPushButton("选择排序")
        self.temp_btn = QPushButton("缓冲区")
        self.temp_btn.setStyleSheet("background-color: red;")
        self.make_data = QPushButton("生成待排序数据")
        self.make_data.clicked.connect(self.init_data)
        self.lay.addWidget(self.make_data, 0, 0, 1, 1)
        self.lay.addWidget(self.bubble_btn, 0, 1, 1, 1)
        self.lay.addWidget(self.insert_btn, 0, 2, 1, 1)
        self.lay.addWidget(self.select_btn, 0, 3, 1, 1)
        # self.lay.addWidget(self.temp_btn, 0, 4, 1, 1)
        self.bubble_btn.clicked.connect(lambda: self.start_sort("bubble"))
        self.insert_btn.clicked.connect(lambda: self.start_sort("insert"))
        self.select_btn.clicked.connect(lambda: self.start_sort("select"))
        self.lay.addWidget(self.chart_view, 1, 0, 1, 4)
        self.timer = QTimer(self)

        self.timer.timeout.connect(self.reset)

        # self.setCentralWidget(self.chart_view)
        # sleep(2)

    def selection_sort(self, arr_init):
        arr = copy.deepcopy(arr_init)
        n = len(arr)
        for i in range(n - 1):
            min_idx = i
            self.min.append(arr[min_idx])
            self.data.append(copy.deepcopy(arr))
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    self.min.append(arr[min_idx])
                    self.data.append(copy.deepcopy(arr))
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            self.min.append(arr[min_idx])
            self.data.append(copy.deepcopy(arr))
        return arr

    def init_data(self):
        if self.sorting:
            print("当前有未完成的排序")
            return
        self.bar_series.clear()
        self.bar_set_0 = QBarSet('排序前')
        self.init_arr = gen_random()
        self.bar_set_0.append(self.init_arr)
        self.bar_series.append(self.bar_set_0)
        # self.bubble_btn.setEnabled(True)
        self.data = []
        self.temp = []
        self.min = []
        self.count = 0
        self.sorting = False

    def bubble_sort(self, arr_init):
        arr = copy.deepcopy(arr_init)
        n = len(arr)
        self.data.append(copy.deepcopy(arr))
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.data.append(copy.deepcopy(arr))
        return arr

    def insertion_sort(self, arr_init):
        arr = copy.deepcopy(arr_init)
        n = len(arr)
        self.data.append(copy.deepcopy(arr))
        self.temp.append('')
        for i in range(1, n):
            key = arr[i]
            self.temp.append(key)
            self.data.append(copy.deepcopy(arr))
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                self.temp.append(key)
                self.data.append(copy.deepcopy(arr))
            arr[j + 1] = key

        return arr

    def start_sort(self, text="bubble"):
        if self.sorting:
            print("当前有未完成的排序")
            return
        self.sorting = True
        self.data.clear()
        self.temp = []
        self.min = []
        if text == "insert":
            self.insertion_sort(self.init_arr)
            self.insert_btn.setText("正在排序")
        elif text == "select":
            self.selection_sort(self.init_arr)
            self.select_btn.setText("正在排序")
        else:
            self.bubble_sort(self.init_arr)
            self.bubble_btn.setText("正在排序")
        self.timer.start(300)

        # self.make_data.setEnabled(False)

    def reset(self):
        self.count += 1
        if self.count < self.data.__len__():
            bar_set = QBarSet('')
            bar_set.append(self.data[self.count])
            if self.temp:
                self.chart.setTitle("当前正在插入的数字是" + str(self.temp[self.count]))
                self.temp_btn.setText(str(self.temp[self.count]))
                # self.temp_btn.setText()
            if self.min:
                self.chart.setTitle("待排序部分发现的最小值是" + str(self.min[self.count]))
                self.temp_btn.setText(str(self.min[self.count]))
            self.bar_series.clear()
            self.bar_series.append(bar_set)
        else:
            self.bubble_btn.setText("冒泡排序")
            self.insert_btn.setText("插入排序")
            self.select_btn.setText("选择排序")
            self.count = 0
            self.timer.stop()
            # self.bubble_btn.setEnabled(False)
            # self.insert_btn.setEnabled(False)
            self.make_data.setEnabled(True)
            self.chart.setTitle("")
            self.sorting = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoChartBarSeries()
    window.show()
    sys.exit(app.exec())
