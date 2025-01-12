from PyQt6 import QtCore, QtGui, QtWidgets

class VisualizationSort(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(860, 230, 1100, 900)
        self.setWindowTitle("Sắp Xếp Trực Quan")
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 540, 420)
        self.buttonResume = QtWidgets.QPushButton("Dừng", self)
        self.buttonResume.setGeometry(70, 360, 100, 30)
        self.buttonResume.clicked.connect(self.resume)
        self.buttonPrevious = QtWidgets.QPushButton("Bước trước", self)
        self.buttonPrevious.setGeometry(220, 360, 100, 30)
        self.buttonPrevious.clicked.connect(self.previous_step)
        self.buttonNext = QtWidgets.QPushButton("Bước sau", self)
        self.buttonNext.setGeometry(370, 360, 100, 30)
        self.buttonNext.clicked.connect(self.next_step)
        self.cbSpeed = QtWidgets.QComboBox(self)
        self.cbSpeed.setGeometry(414, 40, 113, 30)
        self.cbSpeed.addItem("Chậm")
        self.cbSpeed.addItem("Vừa")
        self.cbSpeed.addItem("Nhanh")
        self.cbSpeed.addItem("Rất Nhanh")
        self.cbSpeed.setCurrentIndex(1)  # Mặc định là Vừa
        self.cbSpeed.currentIndexChanged.connect(self.change_speed)
        self.editComparison_Count = QtWidgets.QLineEdit("0", self)
        self.editComparison_Count.setGeometry(QtCore.QRect(140, 40, 60, 30))
        self.editComparison_Count.setReadOnly(True)
        self.editSwap_Count = QtWidgets.QLineEdit("0", self)
        self.editSwap_Count.setGeometry(QtCore.QRect(337, 40, 60, 30))
        self.editSwap_Count.setReadOnly(True)
        self.labelComparison_Count = QtWidgets.QLabel("Số lần so sánh:", self)
        self.labelComparison_Count.setGeometry(20, 40, 113, 30)
        self.labelSwap_Count = QtWidgets.QLabel("Số lần sắp xếp:", self)
        self.labelSwap_Count.setGeometry(217, 40, 113, 30)
        self.labelVisualization = QtWidgets.QLabel("SẮP XẾP TRỰC QUAN", self)
        self.labelVisualization.setGeometry(QtCore.QRect(180, 0, 260, 30))
        self.labelVisualization.setObjectName("labelVisualization")
        self.paused = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.process_step)
        self.data = []
        self.steps = []  
        self.current_step = -1
        self.comparisons = 0
        self.swaps = 0
        self.animation_speed = 600  
        self.buttonResume.setVisible(False)
        self.buttonPrevious.setVisible(False)
        self.buttonNext.setVisible(False)
        self.cbSpeed.setVisible(False)
        
    def draw_data(self, data, color_array):
        self.buttonResume.setVisible(True)
        self.buttonPrevious.setVisible(True)
        self.buttonNext.setVisible(True)
        self.cbSpeed.setVisible(True)
        self.scene.clear()
        c_height = 280
        c_width = 480
        x_width = c_width / (len(data) + 1)
        offset = 20
        spacing = 5
        max_value = max(map(abs, data))  # Tìm giá trị lớn nhất
        zero_line = c_height / 2  # Đường trung tâm
        for i, value in enumerate(data):
            normalized_height = abs(value) / max_value  # Tính chiều cao cột
            height = normalized_height * (c_height / 2 - 10)  # Chiều cao của cột
            if value >= 0:
                y0 = zero_line - height
            else:
                y0 = zero_line
            x0 = i * x_width + offset + spacing
            x1 = x_width - spacing
            y1 = height  
            rect = QtWidgets.QGraphicsRectItem(x0, y0, x1, y1)
            rect.setBrush(QtGui.QColor(color_array[i]))
            self.scene.addItem(rect)
            text = QtWidgets.QGraphicsTextItem(str(value))
            if value >= 0:
                text.setPos(x0 + spacing, y0 - 20)
            else:
                text.setPos(x0 + spacing, y0 + height + 5)
            self.scene.addItem(text)
        zero_line_pen = QtGui.QPen(QtGui.QColor("black"), 2) # Vẽ đường 0 (line)
        self.scene.addLine(offset, zero_line, c_width, zero_line, zero_line_pen)
        self.editComparison_Count.setText(str(self.comparisons)) #Cập nhật số lần so sánh và sắp xếp
        self.editSwap_Count.setText(str(self.swaps))

    def change_speed(self):
        speed = self.cbSpeed.currentText()
        if speed == "Chậm":
            self.animation_speed = 850
        elif speed == "Vừa":
            self.animation_speed = 450
        elif speed == "Nhanh":
            self.animation_speed = 225
        elif speed == "Rất Nhanh":
            self.animation_speed = 1
        if not self.paused:
            self.timer.stop()
            self.timer.start(self.animation_speed)
            
    def resume(self):
        self.paused = not self.paused
        if not self.paused:
            self.buttonResume.setText("Dừng")
            self.timer.start(self.animation_speed)
        else:
            self.buttonResume.setText("Tiếp tục")
            self.timer.stop()

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.comparisons, self.swaps, data, color_array = self.steps[self.current_step]
            self.draw_data(data, color_array)

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.comparisons, self.swaps, data, color_array = self.steps[self.current_step]
            self.draw_data(data, color_array)
        else:
            self.draw_data(self.data, ['green'] * len(self.data))

    def bubble_sort_visualization(self, data, ascending=True):
        self.data = data[:]
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
        self.current_step = -1
        self.step_generator = self.bubble_sort_steps(self.data, ascending)
        self.timer.start(self.animation_speed)

    def process_step(self):
        try:
            next(self.step_generator)
        except StopIteration:
            self.timer.stop()
            self.draw_data(self.data, ['green' for _ in range(len(self.data))])

    def bubble_sort_steps(self, data, ascending=True):
        n = len(data)
        sorted_flags = [False] * n
        for i in range(n - 1):
            swapped = False
            for j in range(n - i - 1):
                self.comparisons += 1
                color_array = [
                    'green' if sorted_flags[k] else
                    'yellow' if k == j or k == j + 1 else
                    'red' for k in range(n)
                ]
                self.steps.append((self.comparisons, self.swaps, data[:], color_array[:]))
                self.current_step += 1
                self.draw_data(data, color_array)
                yield
                if (ascending and data[j] > data[j + 1]) or (not ascending and data[j] < data[j + 1]):
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
                    self.swaps += 1
                    color_array = [
                        'green' if sorted_flags[k] else
                        'orange' if k == j or k == j + 1 else
                        'red' for k in range(n)
                    ]
                    self.steps.append((self.comparisons, self.swaps, data[:], color_array[:]))
                    self.current_step += 1
                    self.draw_data(data, color_array)
                    yield
            sorted_flags[n - i - 1] = True
            if not swapped:
                break
            yield

    def merge_sort_visualization(self, data, ascending=True):
        self.data = data[:]
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
        self.current_step = -1
        self.step_generator = self.merge_sort_steps(self.data, ascending)
        self.timer.start(self.animation_speed)

    def merge_sort_steps(self, data, ascending=True):
        def merge(left, mid, right):
            left_copy = data[left:mid + 1]
            right_copy = data[mid + 1:right + 1]
            i = j = 0
            k = left
            color_array = ['red'] * len(data)
            while i < len(left_copy) and j < len(right_copy):
                self.comparisons += 1
                color_array_copy = color_array[:]
                color_array_copy[left + i] = 'yellow'
                color_array_copy[mid + 1 + j] = 'yellow'
                self.draw_data(data, color_array_copy) 
                self.steps.append((self.comparisons, self.swaps, data[:], color_array_copy[:]))
                self.current_step += 1
                yield
                if (ascending and left_copy[i] <= right_copy[j]) or (not ascending and left_copy[i] >= right_copy[j]):
                    data[k] = left_copy[i]
                    i += 1
                else:
                    data[k] = right_copy[j]
                    j += 1
                    self.swaps += 1
                k += 1
            while i < len(left_copy):
                data[k] = left_copy[i]
                k += 1
                i += 1
                self.draw_data(data, color_array)
                yield
            while j < len(right_copy):
                data[k] = right_copy[j]
                k += 1
                j += 1
                self.swaps += 1
                self.draw_data(data, color_array)
                yield
                
        def merge_sort(left, right):
            if left < right:
                mid = (left + right) // 2
                yield from merge_sort(left, mid)
                yield from merge_sort(mid + 1, right)
                yield from merge(left, mid, right)
        yield from merge_sort(0, len(data) - 1)

