import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from PIL import Image
from io import BytesIO

page_source = None


class Hsr_Component:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument("--disable-blink-features")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("https://irs.thsrc.com.tw/IMINT/")
        if self.driver.page_source.__contains__("台灣高鐵網路訂票系統 個人資料使用說明"):
            self.driver.find_element(by=By.ID, value="cookieAccpetBtn").click()
        if self.driver.find_element(by=By.ID, value="ShowNews").is_displayed():
            self.driver.find_element(by=By.XPATH, value="//*[@id='divNews']/a").click()

    def select_start_station(self, value):
        try:
            start_element = Select(self.driver.find_element(by=By.NAME, value="selectStartStation"))
            start_element.select_by_value(f"{value}")
        except Exception as e:
            print("Select Start Station Error=> ", str(e))
            raise e

    def select_end_station(self, value):
        try:
            end_element = Select(self.driver.find_element(by=By.NAME, value="selectDestinationStation"))
            end_element.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def select_date(self, value):
        try:
            date_element = self.driver.find_element(by=By.NAME, value="toTimeInputField")
            self.driver.execute_script("arguments[0].type = 'text';", date_element)
            self.driver.execute_script(f"arguments[0].value = '{value}';", date_element)
        except Exception as e:
            raise e

    def select_time(self, value):
        try:
            time_element = Select(self.driver.find_element(by=By.NAME, value="toTimeTable"))
            time_element.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def select_adult_ticket(self, value):
        try:
            adults_ticket_element = Select(
                self.driver.find_element(by=By.NAME, value="ticketPanel:rows:0:ticketAmount"))
            adults_ticket_element.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def select_children_ticket(self, value):
        try:
            children_ticket_element = Select(
                self.driver.find_element(by=By.NAME, value="ticketPanel:rows:1:ticketAmount"))
            children_ticket_element.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def select_love_ticket(self, value):
        try:
            love_ticket_element = Select(self.driver.find_element(by=By.NAME, value="ticketPanel:rows:2:ticketAmount"))
            love_ticket_element.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def select_priority_ticket(self, value):
        try:
            priority_ticket_element = Select(
                self.driver.find_element(by=By.NAME, value="ticketPanel:rows:3:ticketAmount"))
            priority_ticket_element.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def select_student_ticket(self, value):
        try:
            college_ticket_element = Select(
                self.driver.find_element(by=By.NAME, value="ticketPanel:rows:4:ticketAmount"))
            college_ticket_element.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def select_business_class(self, value):
        try:
            car_type = Select(self.driver.find_element(by=By.NAME, value="trainCon:trainRadioGroup"))
            car_type.select_by_value(f"{value}")
        except Exception as e:
            raise e

    def fill_out_captcha(self, captcha):
        try:
            captcha_element = self.driver.find_element(by=By.ID, value="securityCode")
            captcha_element.clear()
            captcha_element.send_keys(captcha)
        except Exception as e:
            raise e

    def select_nearby_window(self):
        try:
            seat_pref = Select(self.driver.find_element(by=By.NAME, value="seatCon:seatRadioGroup"))
            seat_pref.select_by_value("1")
        except Exception as e:
            raise e

    def submit_first_page_or_error(self):
        try:
            print("Click first page submit...")
            self.driver.find_element(by=By.ID, value="SubmitButton").click()
            global page_source
            page_source = self.driver.page_source
            if "feedbackPanelERROR" in page_source:
                if self.driver.find_element(by=By.CLASS_NAME, value="feedbackPanelERROR").is_displayed():
                    err_msg = ""
                    error_elements = self.driver.find_elements(by=By.XPATH, value="//*[@id='feedMSG']/span/ul/li")
                    for element in error_elements:
                        err_msg += element.text + "\n"
                    return err_msg
            else:
                return True
            time.sleep(0.5)
        except Exception as e:
            print(str(e))
            raise e

    def submit_second_page_or_error(self):
        try:
            print("Click second page submit...")
            self.driver.find_element(by=By.NAME, value="SubmitButton").click()
            global page_source
            page_source = self.driver.page_source

            if "feedbackPanelERROR" in page_source:
                if self.driver.find_element(by=By.CLASS_NAME, value="feedbackPanelERROR").is_displayed():
                    err_msg = ""
                    error_elements = self.driver.find_elements(by=By.XPATH, value="//*[@id='feedMSG']/span/ul/li")
                    for element in error_elements:
                        err_msg += element.text + "\n"
                    return err_msg
            else:
                return True
        except Exception as e:
            raise e

    def submit_third_page_or_error(self, id_text=None, email=None, phone=None, member_id=None, member_options=0,
                                   love_id_values=None, priority_id_values=None):
        try:
            print("Click third page submit...")

            if (id_text, email, phone) is not None:
                id_number = self.driver.find_element(by=By.ID, value="idNumber")
                mobile_phone = self.driver.find_element(by=By.ID, value="mobilePhone")
                email_element = self.driver.find_element(by=By.ID, value="email")
                if (id_number.text, mobile_phone.text, email_element.text) != "":
                    id_number.clear()
                    mobile_phone.clear()
                    email_element.clear()
                id_number.send_keys(id_text)
                mobile_phone.send_keys(phone)
                email_element.send_keys(email)

            if member_options == 1:
                self.driver.find_element(by=By.ID, value="memberSystemRadio1").click()
                ms_number = self.driver.find_element(by=By.ID, value="msNumber")
                ms_number.clear()
                ms_number.send_keys(id_text)
                self.driver.find_element(by=By.ID, value="memberShipCheckBox").click()

            if member_options == 2 and member_id is not None:
                self.driver.find_element(by=By.ID, value="memberSystemRadio1").click()
                ms_number = self.driver.find_element(by=By.ID, value="msNumber")
                ms_number.clear()
                ms_number.send_keys(member_id)

            if member_options == 3 and member_id is not None:
                self.driver.find_element(by=By.ID, value="memberSystemRadio2").click()
                gu_number = self.driver.find_element(by=By.ID, value="guNumber")
                gu_number.clear()
                gu_number.send_keys(member_id)

            if (love_id_values, priority_id_values) is not None:
                self.passenger_info(love_id_values, priority_id_values)

            self.driver.find_element(by=By.NAME, value="agree").click()
            self.driver.find_element(by=By.ID, value="isSubmit").click()
            time.sleep(0.5)

            global page_source
            page_source = self.driver.page_source

            if "btn-custom2" in page_source:
                member_confirm = self.driver.find_element(by=By.ID, value="btn-custom2")
                if member_confirm.is_displayed():
                    member_confirm.click()

            page_source = self.driver.page_source

            if "您已完成訂位" in page_source:
                return "訂位完成! 請記得在限期內付款完畢。\n詳細資料還請參考台灣高鐵官方網站資料，謝謝。";

            if "feedbackPanelERROR" in page_source:
                print("Third Page Error...")
                if self.driver.find_element(by=By.CLASS_NAME, value="feedbackPanelERROR").is_displayed():
                    err_msg = ""
                    error_elements = self.driver.find_elements(by=By.XPATH, value="//*[@id='feedMSG']/span/ul/li")
                    for element in error_elements:
                        err_msg += element.text + "\n"
                    return err_msg

        except Exception as e:
            print(str(e))
            raise e

    def reload_web(self):
        self.driver.get("https://irs.thsrc.com.tw/IMINT/")

    def catch_captcha(self):
        try:
            if self.driver.find_element(by=By.ID, value="BookingS1Form_homeCaptcha_passCode").is_displayed():
                # 全屏截圖
                screenshot = self.driver.get_screenshot_as_png()
                # 将字节数据转换为图像对象
                image = Image.open(BytesIO(screenshot))
                captcha_element = self.driver.find_element(by=By.ID, value="BookingS1Form_homeCaptcha_passCode")
                left = captcha_element.location['x']
                right = captcha_element.location['x'] + captcha_element.size['width']
                top = captcha_element.location['y']
                bottom = captcha_element.location['y'] + captcha_element.size['height']
                # 裁剪图像
                cropped_image = image.crop((left, top, right, bottom))
                # 將裁剪後的圖像另存為檔案
                cropped_image.save('captcha.png')
                return True
        except Exception as e:
            raise e

    def refresh_captcha(self):
        try:
            if "BookingS1Form_homeCaptcha_passCode" in self.driver.page_source:
                self.driver.find_element(by=By.ID, value="BookingS1Form_homeCaptcha_reCodeLink").click()
            else:
                return "發生錯誤，請點選【重新訂票】。"
        except Exception as e:
            raise e

    def passenger_info(self, love_id_value=None, priority_id_value=None):
        try:
            love_dict = []
            priority_dict = []
            print("===Passenger Information===")
            passenger_info = self.driver.find_elements(by=By.XPATH,
                                                       value="//*[@id='BookingS3FormSP']/section[2]/div[2]/div[2]/div")

            for element in passenger_info:
                element_text = element.find_element(by=By.XPATH, value=".//label/span[2]").text

                if element_text == "愛心票":
                    element_id = element.find_element(by=By.XPATH, value=".//div/input[3]").get_attribute("id")
                    love_dict.append(element_id)
                if element_text == "敬老票":
                    element_id = element.find_element(by=By.XPATH, value=".//div/input[3]").get_attribute("id")
                    priority_dict.append(element_id)

            for i in range(0, len(love_dict)):
                self.driver.find_element(by=By.ID, value=love_dict[i]).send_keys(love_id_value[i])

            for i in range(0, len(priority_dict)):
                self.driver.find_element(by=By.ID, value=priority_dict[i]).send_keys(priority_id_value[i])
        except Exception as e:
            raise e
