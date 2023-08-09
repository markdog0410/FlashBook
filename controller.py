import time
from datetime import date

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QLabel, QDialogButtonBox, QDialog, QApplication, QWidget, \
    QMessageBox
from dateutil.parser import parse
from selenium.common import NoSuchElementException

from UI import Ui_MainWindow
from hsr_web_driver import Hsr_Component

member_text = None
love_id_values = []
priority_id_values = []


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hsr_web_driver = Hsr_Component()
        self.setup_control()
        self.show_captcha()

    def setup_control(self):
        self.ui.confirm_btn.clicked.connect(self.onConfirmBtnClicked)
        self.ui.clean_btn.clicked.connect(self.onCleanBtnClicked)
        self.ui.member_id_select.currentIndexChanged.connect(self.on_member_id_select_changed)
        self.ui.refresh_page_btn.clicked.connect(self.reload_web)
        self.ui.refresh_btn.clicked.connect(self.refresh_captcha)
        self.ui.love_ticket_select.currentIndexChanged.connect(self.show_input_id_fields_dialog)
        self.ui.priority_ticket_select.currentIndexChanged.connect(self.show_input_id_fields_dialog)
        self.ui.love_id_check_btn.clicked.connect(self.show_input_id_dialog_detail)
        self.ui.priority_id_check_btn.clicked.connect(self.show_input_id_dialog_detail)

    def onConfirmBtnClicked(self):
        try:
            self.show_error_on_ui("")
            car_type = self.ui.train_car_type_select.currentIndex()
            start_station = self.ui.start_station_select.currentIndex()
            end_station = self.ui.end_station_select.currentIndex()
            time_select = self.ui.start_time_select.currentIndex()
            date_select = self.ui.start_date_select.date().toString("yyyy/MM/dd")
            adult_ticket_count = self.ui.adult_ticket_select.currentIndex()
            children_ticket_count = self.ui.children_ticket_select.currentIndex()
            love_ticket_count = self.ui.love_ticket_select.currentIndex()
            priority_ticket_count = self.ui.priority_ticket_select.currentIndex()
            student_ticket_count = self.ui.student_ticket_select.currentIndex()
            id_text = self.ui.id_lineEdit.text()
            phone_text = self.ui.phone_lineEdit.text()
            email_text = self.ui.email_lineEdit.text()
            captcha_text = self.ui.captcha_img_lineEdit.text()
            member_id = self.ui.member_id_select.currentIndex()
            nearby_window: bool = self.ui.window_first_checkbox.isChecked()

            self.search_train_schedules(car_type, start_station, end_station, time_select, date_select,
                                        adult_ticket_count, children_ticket_count, love_ticket_count,
                                        priority_ticket_count,
                                        student_ticket_count, id_text, phone_text, email_text, captcha_text, member_id,
                                        nearby_window)

        except NoSuchElementException as e:
            self.show_error_on_ui("請點【重新訂票】再試一次，若仍有問題麻煩來信，謝謝。")
        except Exception as e:
            print(e)

    def onCleanBtnClicked(self):
        try:
            self.show_error_on_ui("")
            self.ui.start_station_select.setCurrentIndex(0)
            self.ui.end_station_select.setCurrentIndex(0)
            self.ui.start_time_select.setCurrentIndex(0)
            self.ui.start_date_select.setDate(date.today())
            self.ui.adult_ticket_select.setCurrentIndex(0)
            self.ui.love_ticket_select.setCurrentIndex(0)
            global love_id_values
            love_id_values.clear()
            self.ui.student_ticket_select.setCurrentIndex(0)
            self.ui.children_ticket_select.setCurrentIndex(0)
            self.ui.priority_ticket_select.setCurrentIndex(0)
            global priority_id_values
            priority_id_values.clear()
            self.ui.id_lineEdit.setText("")
            self.ui.phone_lineEdit.setText("")
            self.ui.email_lineEdit.setText("")
            self.ui.window_first_checkbox.setChecked(False)
            self.ui.member_id_select.setCurrentIndex(0)
            self.ui.member_id_text.setText("")
            self.ui.captcha_img_lineEdit.setText("")

        except Exception as e:
            print(str(e))

    def reload_web(self):
        self.show_error_on_ui("")
        self.hsr_web_driver.reload_web()
        self.show_captcha()

    def get_adult_mapping_value(self):
        try:
            adult_ticket_mapping = {
                0: "0F",
                1: "1F",
                2: "2F",
                3: "3F",
                4: "4F",
                5: "5F",
                6: "6F",
                7: "7F",
                8: "8F",
                9: "9F",
                10: "10F"
            }
            adult_tickets = self.ui.adult_ticket_select.currentIndex()
            adult_ticket_mapping = adult_ticket_mapping[adult_tickets]
            return adult_ticket_mapping
        except Exception as e:
            raise e

    def get_children_mapping_value(self):
        try:
            children_ticket_mapping = {
                0: "0H",
                1: "1H",
                2: "2H",
                3: "3H",
                4: "4H",
                5: "5H",
                6: "6H",
                7: "7H",
                8: "8H",
                9: "9H",
                10: "10H"
            }
            children_tickets = self.ui.children_ticket_select.currentIndex()
            children_ticket_mapping = children_ticket_mapping[children_tickets]
            return children_ticket_mapping
        except Exception as e:
            raise e

    def get_love_mapping_value(self):
        try:
            love_ticket_mapping = {
                0: "0W",
                1: "1W",
                2: "2W",
                3: "3W",
                4: "4W",
                5: "5W",
                6: "6W",
                7: "7W",
                8: "8W",
                9: "9W",
                10: "10W"
            }
            love_tickets = self.ui.love_ticket_select.currentIndex()
            love_ticket_mapping = love_ticket_mapping[love_tickets]
            return love_ticket_mapping
        except Exception as e:
            raise e

    def get_priority_mapping_value(self):
        try:
            priority_ticket_mapping = {
                0: "0E",
                1: "1E",
                2: "2E",
                3: "3E",
                4: "4E",
                5: "5E",
                6: "6E",
                7: "7E",
                8: "8E",
                9: "9E",
                10: "10E"
            }
            priority_tickets = self.ui.priority_ticket_select.currentIndex()
            priority_ticket_mapping = priority_ticket_mapping[priority_tickets]
            return priority_ticket_mapping
        except Exception as e:
            raise e

    def get_student_mapping_value(self):
        try:
            student_ticket_mapping = {
                0: "0P",
                1: "1P",
                2: "2P",
                3: "3P",
                4: "4P",
                5: "5P",
                6: "6P",
                7: "7P",
                8: "8P",
                9: "9P",
                10: "10P"
            }
            student_tickets = self.ui.student_ticket_select.currentIndex()
            student_ticket_mapping = student_ticket_mapping[student_tickets]
            return student_ticket_mapping
        except Exception as e:
            raise e

    def get_time_mapping_values(self):
        try:
            time_mapping = {
                1: "600A",
                2: "630A",
                3: "700A",
                4: "730A",
                5: "800A",
                6: "830A",
                7: "900A",
                8: "930A",
                9: "1000A",
                10: "1030A",
                11: "1100A",
                12: "1130A",
                13: "1200N",
                14: "1230P",
                15: "100P",
                16: "130P",
                17: "200P",
                18: "230P",
                19: "300P",
                20: "330P",
                21: "400P",
                22: "430P",
                23: "500P",
                24: "530P",
                25: "600P",
                26: "630P",
                27: "700P",
                28: "730P",
                29: "800P",
                30: "830P",
                31: "900P",
                32: "930P",
                33: "1000P",
                34: "1030P",
                35: "1100P",
                36: "1130P"
            }
            time_select = self.ui.start_time_select.currentIndex()
            time_select_mapping = time_mapping[time_select]
            return time_select_mapping
        except Exception as e:
            raise e

    def show_error_on_ui(self, error_message):
        self.ui.scroll_error_label.setText(error_message)

    def on_member_id_select_changed(self, index):
        if index in [2, 3]:
            self.ui.member_id_text.setVisible(True)
        else:
            self.ui.member_id_text.setVisible(False)

    def check_all_selections(self, start_station, end_station, time_select, date_select, adult_ticket_count,
                             children_ticket_count, love_ticket_count, priority_ticket_count, student_ticket_count,
                             id_text, captcha_text, member_id):
        try:
            total_tickets = adult_ticket_count + children_ticket_count + love_ticket_count + priority_ticket_count + student_ticket_count
            date_format = parse(date_select).date()
            if any(var == 0 for var in [start_station, end_station, time_select]) or date_format < date.today():
                self.show_error_on_ui("請檢查出發站、終點站、出發時間及日期")
                return False
            elif total_tickets > 10 or total_tickets == 0:
                self.show_error_on_ui("請檢查票券數量，不得為0或超過10張")
                return False
            elif id_text == "" or len(id_text) < 10:
                self.show_error_on_ui("請輸入正確身分證字號")
                return False
            elif captcha_text == "":
                self.show_error_on_ui("請輸入正確驗證碼")
                return False
            elif member_id in [2, 3]:
                global member_text
                member_text = self.ui.member_id_text.text()
                if member_text == "":
                    self.show_error_on_ui("請輸入高鐵會員")
                    return False
                elif member_id == 2 and len(member_text) != 10:
                    self.show_error_on_ui("請輸入正確長度身分證字號")
                    return False
                elif member_id == 3 and len(member_text) != 8:
                    self.show_error_on_ui("請輸入正確長度企業編號")
                    return False
                else:
                    self.show_error_on_ui("")
                    return True
            else:
                self.show_error_on_ui("")
                return True
        except Exception as e:
            print(str(e))

    def search_train_schedules(self, car_type, start_station, end_station, time_select, date_select, adult_ticket_count,
                               children_ticket_count, love_ticket_count, priority_ticket_count, student_ticket_count,
                               id_text, phone_text, email_text, captcha_text, member_id, nearby_window):
        try:
            if self.check_all_selections(start_station, end_station, time_select, date_select, adult_ticket_count,
                                         children_ticket_count, love_ticket_count, priority_ticket_count,
                                         student_ticket_count, id_text, captcha_text, member_id):
                if nearby_window:
                    self.hsr_web_driver.select_nearby_window()
                self.hsr_web_driver.select_business_class(car_type)
                self.hsr_web_driver.select_start_station(start_station)
                self.hsr_web_driver.select_end_station(end_station)
                self.hsr_web_driver.select_date(date_select)
                self.hsr_web_driver.select_time(self.get_time_mapping_values())
                self.hsr_web_driver.select_adult_ticket(self.get_adult_mapping_value())
                self.hsr_web_driver.select_children_ticket(self.get_children_mapping_value())
                self.hsr_web_driver.select_love_ticket(self.get_love_mapping_value())
                self.hsr_web_driver.select_priority_ticket(self.get_priority_mapping_value())
                self.hsr_web_driver.select_student_ticket(self.get_student_mapping_value())
                self.hsr_web_driver.fill_out_captcha(captcha_text)

                first_page = self.hsr_web_driver.submit_first_page_or_error()
                print(f"First page = {first_page}")
                if isinstance(first_page, str):
                    self.show_error_on_ui(first_page)
                    self.refresh_captcha()
                    self.ui.captcha_img_lineEdit.setText("")
                elif first_page:
                    second_page = self.hsr_web_driver.submit_second_page_or_error()
                    print(f"Second page = {second_page}")
                    if isinstance(second_page, str):
                        self.show_error_on_ui(second_page)
                    elif second_page:
                        third_page = self.hsr_web_driver.submit_third_page_or_error(id_text, email_text, phone_text,
                                                                                    member_text, member_id,
                                                                                    love_id_values, priority_id_values)
                        print(f"Third Page = {third_page}")
                        print(f"IDs == >> {love_id_values}, {priority_id_values}")
                        if isinstance(third_page, str):
                            self.show_error_on_ui(third_page)

        except Exception as e:
            raise e

    def show_captcha(self):
        try:
            time.sleep(0.3)
            self.hsr_web_driver.catch_captcha()
            self.ui.captcha_img_label.setPixmap(QtGui.QPixmap("captcha.png"))
        except Exception as e:
            print(str(e))

    def refresh_captcha(self):
        try:
            refresh_rs = self.hsr_web_driver.refresh_captcha()
            if isinstance(refresh_rs, str):
                self.show_error_on_ui(refresh_rs)
            else:
                self.hsr_web_driver.refresh_captcha()
                self.show_captcha()
        except Exception as e:
            self.show_error_on_ui("請點【重新訂票】再試一次，若仍有問題麻煩來信，謝謝。")
            print(str(e))

    def show_input_id_fields_dialog(self, index):
        dialog = InputIdFieldsDialog(index, self)
        global love_id_values, priority_id_values

        if self.sender() == self.ui.love_ticket_select and index != 0:
            if dialog.exec_():
                love_id_values = dialog.getEnteredValues()
                print('Love ID:', love_id_values)
            else:
                self.ui.love_ticket_select.setCurrentIndex(0)
                love_id_values.clear()
        elif self.sender() == self.ui.love_ticket_select and index == 0:
            love_id_values.clear()

        if self.sender() == self.ui.priority_ticket_select and index != 0:
            if dialog.exec_():
                priority_id_values = dialog.getEnteredValues()
                print("Priority ID:", priority_id_values)
            else:
                self.ui.priority_ticket_select.setCurrentIndex(0)
                priority_id_values.clear()
        elif self.sender() == self.ui.priority_ticket_select and index == 0:
            priority_id_values.clear()

    def id_warning_message(self):
        message = "您尚未輸入搭乘者身分證資料。"
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowTitle("注意!!")
        messageBox.setText(message)
        messageBox.addButton("確認", QMessageBox.AcceptRole)
        messageBox.exec_()

    def show_input_id_dialog_detail(self):
        global love_id_values, priority_id_values
        print(f'Love => {love_id_values}, Priority => {priority_id_values}')
        if self.sender().objectName() == "love_id_check_btn" and not love_id_values:
            self.id_warning_message()
        elif self.sender().objectName() == "priority_id_check_btn" and not priority_id_values:
            self.id_warning_message()
        else:
            print("Click Details...")
            show_list = []
            if self.sender().objectName() == "love_id_check_btn":
                show_list = love_id_values
            if self.sender().objectName() == "priority_id_check_btn":
                show_list = priority_id_values
            dialog = QDialog()
            dialog.setWindowTitle("乘客資料")
            layout = QVBoxLayout()
            dialog_width = 220
            dialog.setFixedWidth(dialog_width)
            content = QLabel("如欲修改人數請重新選擇!")
            content.setStyleSheet("color: red")
            layout.addWidget(content)

            labels = [f'ID:{i + 1}' for i in range(len(show_list))]
            line_edits = [QLineEdit() for _ in range(len(show_list))]
            for label, line_edit, love_id in zip(labels, line_edits, show_list):
                print(f'Label ==>> {label}')
                print(f'Love id ==>> {love_id}')
                label_widget = QLabel(label)
                layout.addWidget(label_widget)
                line_edit.setText(love_id)
                line_edit.setReadOnly(True)
                line_edit.setStyleSheet("background-color: #D0D0D0;")
                layout.addWidget(line_edit)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok)
            button_box.accepted.connect(dialog.accept)
            layout.addWidget(button_box)

            dialog.setLayout(layout)
            dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
            dialog.exec_()


class InputIdFieldsDialog(QDialog):
    def __init__(self, count, parent=None):
        super().__init__(parent)
        self.initUI(count)

    def initUI(self, count):
        self.labels = [f'ID:{i + 1}' for i in range(count)]
        self.line_edits = [QLineEdit() for _ in range(count)]

        layout = QVBoxLayout()
        content = QLabel("訂位完成後無法修改證號，請謹慎填寫!")
        content.setStyleSheet("color: red")
        layout.addWidget(content)

        for label, line_edit in zip(self.labels, self.line_edits):
            label_widget = QLabel(label)
            layout.addWidget(label_widget)
            layout.addWidget(line_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        if self.sender().objectName() == "priority_ticket_select":
            self.setWindowTitle('敬老票身分資料')
        if self.sender().objectName() == "love_ticket_select":
            self.setWindowTitle('愛心票身分資料')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def getEnteredValues(self):
        global love_id_values, priority_id_values
        if self.sender().objectName() == "love_ticket_select":
            love_id_values = [line_edit.text() for line_edit in self.line_edits]
            return love_id_values
        if self.sender().objectName() == "priority_ticket_select":
            priority_id_values = [line_edit.text() for line_edit in self.line_edits]
            return priority_id_values
