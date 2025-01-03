from PyQt6 import QtCore, QtGui, QtWidgets
import time
class SortVisualizationWidget(QtWidgets.QWidget):
    def __init__(self, data, sort_type="bubble", parent=None):
        super().__init__(parent)
        self.data = data
        self.sort_type = sort_type
        self.animation_speed = 1.6  # Tốc độ hoạt hình
        self.setWindowTitle("Sắp Xếp Trực Quan")
        self.resize(700, 400)
        # Scene và View để vẽ biểu đồ
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 680, 380)
        # Các nút để chọn thuật toán và bắt đầu
        self.sort_ascending_button = QtWidgets.QPushButton("Sắp Xếp Tăng Dần", self)
        self.sort_ascending_button.setGeometry(10, 360, 200, 30)
        self.sort_ascending_button.clicked.connect(self.sort_ascending)
        self.sort_descending_button = QtWidgets.QPushButton("Sắp Xếp Giảm Dần", self)
        self.sort_descending_button.setGeometry(220, 360, 200, 30)
        self.sort_descending_button.clicked.connect(self.sort_descending)
        self.draw_data(self.data, ['red' for _ in range(len(self.data))])
    def draw_data(self, data, color_array):
        self.scene.clear()
        c_height = 360
        c_width = 680
        x_width = c_width / (len(data) + 1)
        offset = 20
        spacing = 5
        max_value = max(map(abs, data))  # Lấy giá trị tuyệt đối lớn nhất
        zero_line = c_height / 2  # Đường trung tâm cho giá trị 0
        for i, value in enumerate(data):
            normalized_height = abs(value) / max_value  # Chiều cao chuẩn hóa
            height = normalized_height * (c_height / 2 - 10)  # Chiều cao cột
            # Tính tọa độ Y cho cột
            if value >= 0:
                y0 = zero_line - height
            else:
                y0 = zero_line
            # Vị trí X và kích thước cột
            x0 = i * x_width + offset + spacing
            x1 = x_width - spacing
            y1 = height
            # Vẽ cột và tô màu
            rect = QtWidgets.QGraphicsRectItem(x0, y0, x1, y1)
            rect.setBrush(QtGui.QColor(color_array[i]))
            self.scene.addItem(rect)
            text = QtWidgets.QGraphicsTextItem(str(value))
            if value >= 0:
                text.setPos(x0 + spacing, y0 - 20)
            else:
                text.setPos(x0 + spacing, y0 + height + 5)
            self.scene.addItem(text)
        zero_line_pen = QtGui.QPen(QtGui.QColor("black"), 2)
        self.scene.addLine(offset, zero_line, c_width, zero_line, zero_line_pen)
        
    def bubble_sort_visualization(self, data, ascending=True):
        n = len(data)
        sorted_flags = [False] * n  # Đánh dấu phần tử đã sắp xếp
        for i in range(n - 1):
            swapped = False
            for j in range(n - i - 1):
                if (ascending and data[j] > data[j + 1]) or (not ascending and data[j] < data[j + 1]):
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
                # Vẽ lại biểu đồ sau mỗi lần so sánh
                color_array = [
                    'green' if sorted_flags[k] else
                    'yellow' if k == j or k == j + 1 else 'red'
                    for k in range(n)
                ]
                self.draw_data(data, color_array)
                QtCore.QCoreApplication.processEvents()
                time.sleep(self.animation_speed)
            # Đánh dấu phần tử cuối cùng là đã sắp xếp
            sorted_flags[n - i - 1] = True
            if not swapped:  
                break
        self.draw_data(data, ['green' for _ in range(len(data))])

    
    def merge(self, data, left, mid, right, color_array, ascending):
        left_copy = data[left:mid + 1]
        right_copy = data[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_copy) and j < len(right_copy):
            color_array_copy = color_array[:]
            color_array_copy[left + i] = 'yellow'  # Đánh dấu phần tử đang được so sánh từ mảng trái
            color_array_copy[mid + 1 + j] = 'yellow'  # Đánh dấu phần tử đang được so sánh từ mảng phải
            self.draw_data(data, color_array_copy)
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed)
            if (ascending and left_copy[i] <= right_copy[j]) or (not ascending and left_copy[i] >= right_copy[j]):
                data[k] = left_copy[i]
                i += 1
            else:
                data[k] = right_copy[j]
                j += 1
            k += 1
        # Hợp nhất phần còn lại của mảng trái hoặc phải
        while i < len(left_copy):
            data[k] = left_copy[i]
            k += 1
            i += 1
        while j < len(right_copy):
            data[k] = right_copy[j]
            k += 1
            j += 1
        self.draw_data(data, color_array)
        QtCore.QCoreApplication.processEvents()
        time.sleep(self.animation_speed)
    
    def merge_sort_step(self, data, left, right, color_array, ascending):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort_step(data, left, mid, color_array, ascending)  # Sắp xếp phần bên trái
            self.merge_sort_step(data, mid + 1, right, color_array, ascending)  # Sắp xếp phần bên phải
            self.merge(data, left, mid, right, color_array, ascending)  # Hợp nhất hai mảng
            
    def merge_sort_visualization(self, data, ascending=True):
        self.merge_sort_step(data, 0, len(data) - 1, ['red' for _ in range(len(data))], ascending)
        
    def sort_ascending(self):
        if self.sort_type == "bubble":
            self.bubble_sort_visualization(self.data, ascending=True)
        elif self.sort_type == "merge":
            self.merge_sort_visualization(self.data, ascending=True)

    def sort_descending(self):
        if self.sort_type == "bubble":
            self.bubble_sort_visualization(self.data, ascending=False)
        elif self.sort_type == "merge":
            self.merge_sort_visualization(self.data, ascending=False)
