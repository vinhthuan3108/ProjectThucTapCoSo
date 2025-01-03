from PyQt6 import QtCore, QtWidgets
from VisualizationSort import *
import requests, csv, timeit
from SortingAlgorithm import *
class InputData:
    def __init__(self, rbTrucTiep, rbNhapTay, inputThanhPho, editNhietDo, editTocDoGio, editDoAm):
        self.rbTrucTiep = rbTrucTiep
        self.rbNhapTay = rbNhapTay
        self.inputThanhPho = inputThanhPho
        self.editNhietDo = editNhietDo
        self.editTocDoGio = editTocDoGio
        self.editDoAm = editDoAm
        self.csv_data = None  
    def _set_editable(self, editable):
        self.editNhietDo.setReadOnly(not editable)
        self.editTocDoGio.setReadOnly(not editable)
        self.editDoAm.setReadOnly(not editable)    
    def enable_manual_input(self, checked):
        if checked:  
            self._set_editable(True)
            self.csv_data = None
        else:  
            self._set_editable(False)
    def load_csv_data(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                self.csv_data = []
                for row in data:
                    if len(row) >= 4:
                        city, temp, wind_speed, humidity = row[0], row[1], row[2], row[3]
                        try:
                            temp_value = float(temp)
                            wind_speed_value = float(wind_speed)
                            humidity_value = float(humidity)
                            if not (-70 <= temp_value <= 70):
                                raise ValueError(f"Nhiệt độ của thành phố {city} không hợp lệ. Nhiệt độ cần trong khoảng -70°C đến 70°C.")
                            if not (0 <= wind_speed_value <= 70):
                                raise ValueError(f"Tốc độ gió của thành phố {city} không hợp lệ. Tốc độ gió cần trong khoảng 0 m/s đến 70 m/s.")
                            if not (0 <= humidity_value <= 100):
                                raise ValueError(f"Độ ẩm của thành phố {city} không hợp lệ. Độ ẩm cần trong khoảng 0% đến 100%.")
                            self.csv_data.append({"city": city, "temp": temp, "wind_speed": wind_speed, "humidity": humidity})
                        except ValueError as e:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"{str(e)}. Dòng lỗi sẽ tự động bị xóa.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Error reading CSV file: {str(e)}")
    def fetch_data(self):
        if self.rbTrucTiep.isChecked():
            self.csv_data = None
            return self.fetch_data_from_api()
        elif self.rbNhapTay.isChecked():
            return self.fetch_data_from_manual_input()
        else:
            return None
    def fetch_data_from_api(self):
        city = self.inputThanhPho.text()
        if not city:
            QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng nhập tên thành phố!")
            return None
        API_KEY = "bd64ba52f144248132813357b07e5338"
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        try:
            url = BASE_URL + f"appid={API_KEY}&q={city}"
            response = requests.get(url).json()
            if response.get("cod") != 200:
                QtWidgets.QMessageBox.warning(None, "Warning", "Không tìm thấy thành phố!")
                return None
            temp_kelvin = response["main"]["temp"]
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]
            temp_celsius = temp_kelvin - 273.15
            return {"city": city, "temp": f"{temp_celsius:.2f} °C", "wind_speed": f"{wind_speed} m/s", "humidity": f"{humidity} %"}
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", "Đã xảy ra lỗi!")
            return None  
    def fetch_data_from_manual_input(self):
        temp = self.editNhietDo.text()
        wind_speed = self.editTocDoGio.text()
        humidity = self.editDoAm.text()
        if not temp or not wind_speed or not humidity:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã xảy ra lỗi")
            return None
        city = self.inputThanhPho.text()
        return {"city": city, "temp": temp, "wind_speed": wind_speed, "humidity": humidity}
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 680) #1920,1080
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonDeleteRow = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteRow.setGeometry(QtCore.QRect(200, 550, 131, 28))
        self.buttonDeleteRow.setObjectName("buttonDeleteRow")
        self.buttonDeleteAll = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteAll.setGeometry(QtCore.QRect(360, 550, 111, 28))
        self.buttonDeleteAll.setObjectName("buttonDeleteAll")
        self.buttonSort = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonSort.setGeometry(QtCore.QRect(500, 550, 93, 28))
        self.buttonSort.setObjectName("buttonSort")
        self.cbTieuChi = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbTieuChi.setGeometry(QtCore.QRect(20, 310, 101, 22))
        self.cbTieuChi.setObjectName("cbTieuChi")
        self.cbTieuChi.addItem("")
        self.cbTieuChi.addItem("")
        self.cbTieuChi.addItem("")
        self.cbLoaiSapXep = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbLoaiSapXep.setGeometry(QtCore.QRect(20, 360, 101, 22))
        self.cbLoaiSapXep.setObjectName("cbLoaiSapXep")
        self.cbLoaiSapXep.addItem("")
        self.cbLoaiSapXep.addItem("")
        self.cbThuTuSapXep = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbThuTuSapXep.setGeometry(QtCore.QRect(20, 410, 101, 22))
        self.cbThuTuSapXep.setObjectName("cbThuTuSapXep")
        self.cbThuTuSapXep.addItem("")
        self.cbThuTuSapXep.addItem("")
        self.rbTrucTiep = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.rbTrucTiep.setGeometry(QtCore.QRect(60, 50, 151, 20))
        self.rbTrucTiep.setObjectName("rbTrucTiep")
        self.rbNhapTay = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.rbNhapTay.setGeometry(QtCore.QRect(220, 50, 171, 20))
        self.rbNhapTay.setObjectName("rbNhapTay")
        self.browseButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(330, 46, 141, 30))
        self.browseButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, 105, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 145, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(340, 185, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_thoigian = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_thoigian.setGeometry(QtCore.QRect(250, 510, 113, 22))
        self.label_thoigian.setObjectName("label_thoigian")
        self.editNhietDo = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editNhietDo.setGeometry(QtCore.QRect(420, 100, 113, 22))
        self.editNhietDo.setReadOnly(True)
        self.editNhietDo.setObjectName("editNhietDo")
        self.editTocDoGio = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editTocDoGio.setGeometry(QtCore.QRect(420, 140, 113, 22))
        self.editTocDoGio.setReadOnly(True)
        self.editTocDoGio.setObjectName("editTocDoGio")
        self.editDoAm = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editDoAm.setGeometry(QtCore.QRect(420, 180, 113, 22))
        self.editDoAm.setReadOnly(True)
        self.editDoAm.setObjectName("editDoAm")
        self.editThoiGian = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editThoiGian.setGeometry(QtCore.QRect(360, 510, 113, 22))
        self.editThoiGian.setReadOnly(True)
        self.editThoiGian.setObjectName("editDoAm")
        self.inputThanhPho = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.inputThanhPho.setGeometry(QtCore.QRect(20, 90, 113, 22))
        self.inputThanhPho.setObjectName("inputThanhPho")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 90, 111, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 230, 141, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(180, 300, 440, 201))
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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.browseButton.clicked.connect(self.browseFile)
        self.pushButton.clicked.connect(self.fetch_weather_data)
        self.pushButton_2.clicked.connect(self.show_data_on_table)
        self.buttonDeleteRow.clicked.connect(self.delete_selected_row)
        self.buttonDeleteAll.clicked.connect(self.delete_all_rows)
        self.buttonSort.clicked.connect(self.visualization_sort_window)
        self.buttonSort.clicked.connect(self.sort_table)
        self.input_data_handler = InputData(self.rbTrucTiep, self.rbNhapTay, self.inputThanhPho, 
                                            self.editNhietDo, self.editTocDoGio, self.editDoAm,)
        self.rbNhapTay.toggled.connect(self.input_data_handler.enable_manual_input)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sắp xếp thời tiết - Vĩnh Thuận - 64132409"))
        self.buttonDeleteRow.setText(_translate("MainWindow", "Xóa hàng đang chọn"))
        self.buttonDeleteAll.setText(_translate("MainWindow", "Xóa tất cả hàng"))
        self.buttonSort.setText(_translate("MainWindow", "Sắp xếp"))
        self.cbTieuChi.setItemText(0, _translate("MainWindow", "Nhiệt độ"))
        self.cbTieuChi.setItemText(1, _translate("MainWindow", "Tốc độ gió"))
        self.cbTieuChi.setItemText(2, _translate("MainWindow", "Độ ẩm"))
        self.cbLoaiSapXep.setItemText(0, _translate("MainWindow", "Bubble Sort"))
        self.cbLoaiSapXep.setItemText(1, _translate("MainWindow", "Merge Sort"))
        self.cbThuTuSapXep.setItemText(0, _translate("MainWindow", "Tăng dần"))
        self.cbThuTuSapXep.setItemText(1, _translate("MainWindow", "Giảm dần"))
        self.rbTrucTiep.setText(_translate("MainWindow", "Lấy dữ liệu trực tiếp"))
        self.rbNhapTay.setText(_translate("MainWindow", "Nhập tay"))
        self.browseButton.setText(_translate("MainWindow", "Chọn file CSV"))
        self.label.setText(_translate("MainWindow", "Nhiệt độ"))
        self.label_2.setText(_translate("MainWindow", "Tốc độ gió"))
        self.label_3.setText(_translate("MainWindow", "Độ ẩm"))
        self.label_thoigian.setText(_translate("MainWindow", "Thời gian sắp xếp"))
        self.pushButton.setText(_translate("MainWindow", "Nhập Thành Phố"))
        self.pushButton_2.setText(_translate("MainWindow", "Hiện Kết Quả Lên Bảng"))
    def browseFile(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.input_data_handler.load_csv_data(file_path)
            self.show_data_on_table()
    def fetch_weather_data(self):
        data = self.input_data_handler.fetch_data()
        if data:
            if isinstance(data, dict):  
                self.editNhietDo.setText(data['temp'])
                self.editTocDoGio.setText(data['wind_speed'])
                self.editDoAm.setText(data['humidity'])
            elif isinstance(data, list): 
                for item in data:
                    city = item.get("name")
                    temp_kelvin = item.get("main", {}).get("temp")
                    wind_speed = item.get("wind", {}).get("speed")
                    humidity = item.get("main", {}).get("humidity")

                    if city and temp_kelvin is not None and wind_speed is not None and humidity is not None:
                        temp_celsius = temp_kelvin - 273.15
                        self.add_row_to_table(city, f"{temp_celsius:.2f} °C", f"{wind_speed} m/s", f"{humidity} %")
    def show_data_on_table(self):
        if self.input_data_handler.csv_data:
            for item in self.input_data_handler.csv_data:
                city = item["city"]
                temp = item["temp"]
                wind_speed = item["wind_speed"]
                humidity = item["humidity"]
                self.add_row_to_table(city, temp, wind_speed, humidity)
        else:
            data = self.input_data_handler.fetch_data()
            if data:
                self.add_row_to_table(data["city"], data["temp"], data["wind_speed"], data["humidity"])
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
        
    def visualization_sort_window(self):
        criteria = self.cbTieuChi.currentText()  # "Nhiệt độ", "Tốc độ gió", "Độ ẩm"
        sort_method = self.cbLoaiSapXep.currentText()  # "Bubble Sort" or "Merge Sort"
        rows = []
        for row in range(self.tableWidget.rowCount()):
            city = self.tableWidget.item(row, 0).text()
            temp = float(self.tableWidget.item(row, 1).text().split()[0])  
            wind_speed = float(self.tableWidget.item(row, 2).text().split()[0])  
            humidity = float(self.tableWidget.item(row, 3).text().split()[0])  
            rows.append([city, temp, wind_speed, humidity])
        if criteria == "Nhiệt độ":
            key_index = 1 
        elif criteria == "Tốc độ gió":
            key_index = 2  
        elif criteria == "Độ ẩm":
            key_index = 3  
            return
        try:
            if sort_method == "Bubble Sort":
                values = [row[key_index] for row in rows]  
                self.visualization_widget = SortVisualizationWidget(values, sort_type="bubble")
                self.visualization_widget.show()
            else:
                values = [row[key_index] for row in rows]  
                self.visualization_widget = SortVisualizationWidget(values, sort_type="merge")
                self.visualization_widget.show() 
                return
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã có lỗi xảy ra: {str(e)}")
            return
        
    def sort_table(self):
        criteria = self.cbTieuChi.currentText()  # "Nhiệt độ", "Tốc độ gió", "Độ ẩm"
        sort_method = self.cbLoaiSapXep.currentText()  # "Bubble Sort" or "Merge Sort"
        sort_order = self.cbThuTuSapXep.currentText()  # "Tăng dần" or "Giảm dần"
        if sort_order == "Tăng dần":
            order = 'asc'
        elif sort_order == "Giảm dần":
            order = 'desc'
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Phương thức sắp xếp không hợp lệ!")
            return
        rows = []
        for row in range(self.tableWidget.rowCount()):
            city = self.tableWidget.item(row, 0).text()
            temp = float(self.tableWidget.item(row, 1).text().split()[0])  
            wind_speed = float(self.tableWidget.item(row, 2).text().split()[0])  
            humidity = float(self.tableWidget.item(row, 3).text().split()[0])  
            rows.append([city, temp, wind_speed, humidity])
        if criteria == "Nhiệt độ":
            key_index = 1 
        elif criteria == "Tốc độ gió":
            key_index = 2  
        elif criteria == "Độ ẩm":
            key_index = 3  
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Tiêu chí không hợp lệ!")
            return
        start_time = timeit.default_timer()
        try:
            sorter = Sort(rows, key_index, order, self.rbTrucTiep, self.rbNhapTay, self.inputThanhPho, self.editNhietDo, self.editTocDoGio, self.editDoAm)
            sorted_rows = sorter.sort(algorithm="bubble" if sort_method == "Bubble Sort" else "merge")
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã có lỗi xảy ra: {str(e)}")
            return
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        self.editThoiGian.setText(f"{elapsed_time:.6f} giây")
        
        self.tableWidget.setRowCount(0)
        for row in sorted_rows:
            self.add_row_to_table(row[0], f"{row[1]:.2f} °C", f"{row[2]} m/s", f"{row[3]} %")
            
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
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
