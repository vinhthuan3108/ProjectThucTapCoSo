from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog
import requests, csv, timeit
from sorts import Sort
from visualsorts import VisualizationSort
class Input:
    def __init__(self):
        self.editNhietDo = 0
        self.editTocDoGio = 0
        self.editDoAm = 0
    def enable_manual_input(self, checked):
        if checked:  # Nếu chọn nhập tay
            self.editNhietDo.setReadOnly(False)
            self.editTocDoGio.setReadOnly(False)
            self.editDoAm.setReadOnly(False)
        else:  # Nếu nhập tay đang không được chọn
            self.editNhietDo.setReadOnly(True)
            self.editTocDoGio.setReadOnly(True)
            self.editDoAm.setReadOnly(True)    
    def API_data(self, city):
        if not city:
            raise ValueError("Vui lòng nhập tên thành phố!")
        API_KEY = "bd64ba52f144248132813357b07e5338"  
        
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        try:
            url = BASE_URL + f"appid={API_KEY}&q={city}"
            response = requests.get(url).json()
            if response.get("cod") != 200:
                raise ValueError(f"Thành phố {city} không tìm thấy.")
            temp_kelvin = response["main"]["temp"]
            self.humidity = response["main"]["humidity"]
            self.wind_speed = response["wind"]["speed"]
            self.temp = temp_kelvin - 273.15  
        except Exception as e:
            raise ValueError(f"{e}")
        
    def load_csv_data(self, file_path):
        data = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) == 4:
                        city, temp, wind_speed, humidity = row
                        data.append([city, temp, wind_speed, humidity])
        except Exception as e:
            raise ValueError(f"Lỗi lấy file csv: {e}")
        return data
    
class Ui_MainWindow():
    def setupUi(self, MainWindow):
        stylesheet = """
            QWidget {
                color: black;  
            }
            QPushButton, QComboBox, QRadioButton, QLabel, QTextEdit {
                font: 12pt;  
            }
            QLabel#labelTitle {
                font: bold 21pt "Segoe Fluent Icons";  
                color: #0066CC;  
            }
            QLabel#labelNote {
                font: bold 11pt "Segoe Fluent Icons";  
                color: grey;  
            }
            QLabel#labelVisualization {
                font: bold 16pt "Segoe Fluent Icons";  
                color: red;  
            }
            QPushButton {
                color: black;  
            }
        """
        MainWindow.setStyleSheet(stylesheet)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonBrowse = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonBrowse.setGeometry(QtCore.QRect(480, 100, 123, 30))
        self.buttonBrowse.setObjectName("buttonBrowse")
        self.buttonDisplay = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDisplay.setGeometry(QtCore.QRect(320, 300, 250, 30))
        self.buttonDisplay.setObjectName("buttonDisplay")
        self.buttonDeleteRow = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteRow.setGeometry(QtCore.QRect(305, 700, 160, 30))
        self.buttonDeleteRow.setObjectName("buttonDeleteRow")
        self.buttonDeleteAll = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteAll.setGeometry(QtCore.QRect(490, 700, 130, 30))
        self.buttonDeleteAll.setObjectName("buttonDeleteAll")
        self.buttonExport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonExport.setGeometry(QtCore.QRect(140, 700, 140, 30))
        self.buttonExport.setObjectName("buttonExport")
        self.buttonSort = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonSort.setGeometry(QtCore.QRect(645, 700, 93, 30))
        self.buttonSort.setObjectName("buttonSort")
        self.buttonThanhPho = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonThanhPho.setGeometry(QtCore.QRect(300, 160, 141, 30))
        self.buttonThanhPho.setObjectName("buttonThanhPho")
        self.cbTieuChi = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbTieuChi.setGeometry(QtCore.QRect(110, 360, 118, 30))
        self.cbTieuChi.setObjectName("cbTieuChi")
        self.cbTieuChi.addItem("Nhiệt độ")
        self.cbTieuChi.addItem("Tốc độ gió")
        self.cbTieuChi.addItem("Độ ẩm")
        self.cbLoaiSapXep = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbLoaiSapXep.setGeometry(QtCore.QRect(110, 430, 118, 30))
        self.cbLoaiSapXep.setObjectName("cbLoaiSapXep")
        self.cbLoaiSapXep.addItem("Bubble Sort")
        self.cbLoaiSapXep.addItem("Merge Sort")
        self.cbThuTuSapXep = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbThuTuSapXep.setGeometry(QtCore.QRect(110, 500, 118, 30))
        self.cbThuTuSapXep.setObjectName("cbThuTuSapXep")
        self.cbThuTuSapXep.addItem("Tăng dần")
        self.cbThuTuSapXep.addItem("Giảm dần")
        self.editNhietDo = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editNhietDo.setGeometry(QtCore.QRect(610, 160, 113, 26))
        self.editNhietDo.setReadOnly(True)
        self.editNhietDo.setObjectName("editNhietDo")
        self.editTocDoGio = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editTocDoGio.setGeometry(QtCore.QRect(610, 210, 113, 26))
        self.editTocDoGio.setReadOnly(True)
        self.editTocDoGio.setObjectName("editTocDoGio")
        self.editDoAm = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editDoAm.setGeometry(QtCore.QRect(610, 260, 113, 26))
        self.editDoAm.setReadOnly(True)
        self.editDoAm.setObjectName("editDoAm")
        self.editThoiGian = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editThoiGian.setGeometry(QtCore.QRect(510, 628, 133, 26))
        self.editThoiGian.setReadOnly(True)
        self.editThoiGian.setObjectName("editThoiGian")
        self.editThanhPho = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.editThanhPho.setGeometry(QtCore.QRect(110, 162, 148, 106))
        self.editThanhPho.setObjectName("editThanhPho")
        self.labelTitle = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelTitle.setGeometry(QtCore.QRect(500, 5, 600, 80))
        self.labelTitle.setObjectName("labelTitle")
        self.labelNote = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelNote.setGeometry(QtCore.QRect(50, 40, 700, 80))
        self.labelNote.setObjectName("labelNote")
        self.labelNhietDo = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelNhietDo.setGeometry(QtCore.QRect(524, 165, 71, 22))
        self.labelNhietDo.setObjectName("labelNhietDo")
        self.labelTocDoGio = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelTocDoGio.setGeometry(QtCore.QRect(510, 215, 81, 22))
        self.labelTocDoGio.setObjectName("labelTocDoGio")
        self.labelDoAm = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelDoAm.setGeometry(QtCore.QRect(537, 265, 71, 22))
        self.labelDoAm.setObjectName("labelDoAm")
        self.labelThoiGian = QtWidgets.QLabel(parent=self.centralwidget)
        self.labelThoiGian.setGeometry(QtCore.QRect(350, 630, 133, 22))
        self.labelThoiGian.setObjectName("labelThoiGian")
        self.rbTrucTiep = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.rbTrucTiep.setGeometry(QtCore.QRect(110, 100, 161, 30))
        self.rbTrucTiep.setObjectName("rbTrucTiep")
        self.rbNhapTay = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.rbNhapTay.setGeometry(QtCore.QRect(330, 100, 95, 30))
        self.rbNhapTay.setObjectName("rbNhapTay")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(270, 360, 440, 251))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Thành Phố", "Nhiệt Độ (°C)", "Tốc Độ Gió (m/s)", "Độ Ẩm (%)"])
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar) 
        self.retranslateUi(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ứng dụng sắp xếp dữ liệu thời tiết-Vĩnh Thuận-64132409"))
        self.buttonDeleteRow.setText(_translate("MainWindow", "Xóa hàng đang chọn"))
        self.buttonDeleteAll.setText(_translate("MainWindow", "Xóa tất cả hàng"))
        self.buttonExport.setText(_translate("MainWindow", "Xuất file từ bảng"))
        self.buttonSort.setText(_translate("MainWindow", "Sắp xếp"))
        self.buttonThanhPho.setText(_translate("MainWindow", "Nhập Thành Phố"))
        self.buttonBrowse.setText(_translate("MainWindow", "Chọn file CSV"))
        self.cbTieuChi.setItemText(0, _translate("MainWindow", "Nhiệt độ"))
        self.cbTieuChi.setItemText(1, _translate("MainWindow", "Tốc độ gió"))
        self.cbTieuChi.setItemText(2, _translate("MainWindow", "Độ ẩm"))
        self.cbLoaiSapXep.setItemText(0, _translate("MainWindow", "Bubble Sort"))
        self.cbLoaiSapXep.setItemText(1, _translate("MainWindow", "Merge Sort"))
        self.cbThuTuSapXep.setItemText(0, _translate("MainWindow", "Tăng dần"))
        self.cbThuTuSapXep.setItemText(1, _translate("MainWindow", "Giảm dần"))
        self.labelTitle.setText(_translate("MainWindow", "ỨNG DỤNG SẮP XẾP DỮ LIỆU THỜI TIẾT"))
        self.labelNote.setText(_translate("MainWindow", "Khi chọn lấy dữ liệu trực tiếp có thể nhập nhiều thành phố, ngăn cách nhau bằng dấu phẩy"))
        self.labelNhietDo.setText(_translate("MainWindow", "Nhiệt độ"))
        self.labelTocDoGio.setText(_translate("MainWindow", "Tốc độ gió"))
        self.labelDoAm.setText(_translate("MainWindow", "Độ ẩm"))
        self.labelThoiGian.setText(_translate("MainWindow", "Thời gian sắp xếp"))
        self.rbTrucTiep.setText(_translate("MainWindow", "Lấy dữ liệu trực tiếp"))
        self.rbNhapTay.setText(_translate("MainWindow", "Nhập tay"))
        self.buttonDisplay.setText(_translate("MainWindow", "Hiện Dữ Liệu Nhập Tay Lên Bảng"))
class WeatherApp(QtWidgets.QMainWindow, Ui_MainWindow, Input):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sorter = Sort()
        self.visual_sorter = VisualizationSort(self)
        self.rbNhapTay.toggled.connect(self.enable_manual_input)
        self.buttonThanhPho.clicked.connect(self.fetch_weather_data)
        self.buttonDisplay.clicked.connect(self.show_data_on_table)
        self.buttonBrowse.clicked.connect(self.load_csv_from_file)
        self.buttonSort.clicked.connect(self.sort_and_visualize)  
        self.buttonDeleteRow.clicked.connect(self.delete_selected_row)
        self.buttonDeleteAll.clicked.connect(self.delete_all_rows)
        self.buttonExport.clicked.connect(self.export_to_csv)

    def load_csv_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                data = self.load_csv_data(file_path)  
                for row in data:
                    city, temp, wind_speed, humidity = row
                    self.add_row_to_table(city, temp, wind_speed, humidity)
            except ValueError as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def export_to_csv(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Thành Phố", "Nhiệt Độ (°C)", "Tốc Độ Gió (m/s)", "Độ Ẩm (%)"])
                    for row in range(self.tableWidget.rowCount()):
                        city = self.tableWidget.item(row, 0).text()
                        temp = self.tableWidget.item(row, 1).text()
                        wind_speed = self.tableWidget.item(row, 2).text()
                        humidity = self.tableWidget.item(row, 3).text()
                        writer.writerow([city, temp, wind_speed, humidity])
                QtWidgets.QMessageBox.information(self, "Success", "Xuất dữ liệu thành công!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))
    def fetch_weather_data(self):
        cities = self.editThanhPho.toPlainText().split(',')  
        if self.rbTrucTiep.isChecked():
            for city in cities:
                city = city.strip()  
                try:
                    self.API_data(city)  # Giả sử API trả về giá trị nhiệt độ, tốc độ gió và độ ẩm
                    self.editNhietDo.setText(f"{self.temp:.2f} °C")
                    self.editTocDoGio.setText(f"{self.wind_speed} m/s")
                    self.editDoAm.setText(f"{self.humidity} %")
                    # Gọi trực tiếp add_row_to_table sau khi có dữ liệu
                    self.add_row_to_table(city, f"{self.temp:.2f} °C", f"{self.wind_speed} m/s", f"{self.humidity} %")
                except ValueError as e:
                    QtWidgets.QMessageBox.critical(None, "Error", str(e))

    def show_data_on_table(self, city):
        if self.rbNhapTay.isChecked():
            city = self.editThanhPho.toPlainText()
            temp = self.editNhietDo.text()
            wind_speed = self.editTocDoGio.text()
            humidity = self.editDoAm.text()
            if not temp or not wind_speed or not humidity:
                QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng nhập đầy đủ dữ liệu!")
                return
        else:
            temp = self.editNhietDo.text()
            wind_speed = self.editTocDoGio.text()
            humidity = self.editDoAm.text()
        self.add_row_to_table(city, temp, wind_speed, humidity)
    def add_row_to_table(self, city, temp, wind_speed, humidity):
        try:
            temp_value = float(temp.split()[0])  
            if temp_value < -70.0 or temp_value > 70.0:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Nhiệt độ của thành phố {city} không hợp lệ: {temp}. Nhiệt độ cần trong khoảng -70°C đến 70°C.")
                return  
            wind_speed_value = float(wind_speed.split()[0])  
            if wind_speed_value < 0 or wind_speed_value > 70:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Tốc độ gió của thành phố {city} không hợp lệ: {wind_speed}. Tốc độ gió cần trong khoảng 0 m/s đến 70 m/s.")
                return  
            humidity_value = float(humidity.split()[0])  
            if humidity_value < 0 or humidity_value > 100:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Độ ẩm của thành phố {city} không hợp lệ: {humidity}. Độ ẩm cần trong khoảng 0% đến 100%.")
                return  
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Error", f"Dữ liệu của thành phố {city} không hợp lệ. Vui lòng nhập lại!")
            return  
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(city))
        self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(temp))
        self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(wind_speed))
        self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(humidity))
    def sort_and_visualize(self):
        if self.tableWidget.rowCount() == 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "Bảng không có dữ liệu để sắp xếp!")
            return
        criteria = self.cbTieuChi.currentText()  # "Nhiệt độ", "Tốc độ gió", "Độ ẩm"
        sort_method = self.cbLoaiSapXep.currentText()  # "Bubble Sort" hoặc "Merge Sort"
        sort_order = self.cbThuTuSapXep.currentText()  # "Tăng dần" hoặc "Giảm dần"
        ascending = sort_order == "Tăng dần"  
        key_index = {"Nhiệt độ": 1, "Tốc độ gió": 2, "Độ ẩm": 3}.get(criteria, 1)
        data = []
        for row in range(self.tableWidget.rowCount()):
            city = self.tableWidget.item(row, 0).text()
            temp = float(self.tableWidget.item(row, 1).text().split()[0])  # Loại bỏ đơn vị
            wind_speed = float(self.tableWidget.item(row, 2).text().split()[0])
            humidity = float(self.tableWidget.item(row, 3).text().split()[0])
            data.append([city, temp, wind_speed, humidity])
        start_time = timeit.default_timer()
        sorted_data = self.sorter.sort_data(data[:], key_index, sort_method, 'asc' if ascending else 'desc')
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        self.editThoiGian.setText(f"{elapsed_time:.6f} giây")
        self.tableWidget.setRowCount(0)  # Xóa tất cả các dòng cũ
        for row in sorted_data:  # Cập nhật bảng với dữ liệu đã sắp xếp
            self.add_row_to_table(row[0], f"{row[1]:.2f} °C", f"{row[2]} m/s", f"{row[3]} %")
        data_to_visualize = [row[key_index] for row in data]  # Sử dụng key_index để lấy dữ liệu cần trực quan hóa
        if sort_method == "Bubble Sort":
            self.visual_sorter.bubble_sort_visualization(data_to_visualize, ascending=ascending)
        elif sort_method == "Merge Sort":
            self.visual_sorter.merge_sort_visualization(data_to_visualize, ascending=ascending)
        self.visual_sorter.show()
        
    def delete_selected_row(self):
        row = self.tableWidget.currentRow()
        if row >= 0:  
            self.tableWidget.removeRow(row)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng chọn hàng để xóa!")
    def delete_all_rows(self):
        row_count = self.tableWidget.rowCount()
        if row_count > 0:
            self.tableWidget.setRowCount(0)  
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Bảng không có dữ liệu để xóa!")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = WeatherApp()  
    MainWindow.show()
    sys.exit(app.exec())
