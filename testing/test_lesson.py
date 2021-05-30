import time
from selenium.webdriver import Firefox
from selenium.webdriver.support.select import Select
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class LessonTest(unittest.TestCase):

    def setUp(self):
        self.SPEED_READ_COUNT = 0
        self.TITLE_TEXT_COUNT =0
        self.PROMPT_TEXT_INPUT = 0
        self.IFRAME_LINK_COUNT =0
        self.TITLE_TEXTAREA_COUNT=0
        self.VERIFY_PHONE_COUNT=0
        self.SIGNATURE_IMAGE_COUNT=0
        self.USER_GPS_COUNT=0
        self.browser = Firefox() # Using Firefox browser, you need to have geckodriver installed for this to work!
        self.flashcard_select=0

    def login(self):
        try:
            self.browser.get("http://localhost:8086/") 
            WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.ID, "username")))
            username= self.browser.find_element_by_id("username") # Username element
            password = self.browser.find_element_by_id("pwd") # Password Element 
            login_button = self.browser.find_element_by_class_name("login-button") # Login button element
            username.send_keys("bot@dreampotential.org") # Enter the username
            password.send_keys("iamnotbot") # Enter the password
            login_button.click() #Click the login button
            WebDriverWait(self.browser,20).until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard_title")))
        except:
            self.browser.quit()
            
    def submit(self):
        submit_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_button.click()
        time.sleep(1)

    def go_to_lesson_builder(self):
        self.browser.get("http://localhost:8086/lesson.html") # Goto Login builder, used it directly.
        self.flashcard_select=Select(self.browser.find_element_by_id("selectsegment"))
    def clean_up(self):
        self.browser.quit()
    # Edit Lesson Name Edits the lesson name of the segment builder
    def edit_lesson_name(self,name):
        name_input = self.browser.find_element_by_id("lesson_name")
        name_input.send_keys(name)
        
    def speed_read(self,text):
        self.flashcard_select.select_by_value("speed_read")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        speed_read_textbox = self.browser.find_element_by_name("speed_read_"+str(self.SPEED_READ_COUNT))
        speed_read_textbox.send_keys(text)
        self.SPEED_READ_COUNT +=1 

    def title_text(self,title, text):
        self.flashcard_select.select_by_value("title_text")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        title_text_title =self. browser.find_element_by_name("title_"+str(self.TITLE_TEXT_COUNT))
        title_text_text = self.browser.find_element_by_name("text_"+str(self.TITLE_TEXT_COUNT))
        title_text_title.send_keys(title)
        title_text_text.send_keys(text)
        self.TITLE_TEXT_COUNT +=1 


    # Add Prompt Text Input flashcard - Also called Title Input
    def prompt_text_input(self,text):
        self.flashcard_select.select_by_value("title_input")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        prompt_text_input_textbox = self.browser.find_element_by_name("title_input_textarea_"+str(self.PROMPT_TEXT_INPUT))
        prompt_text_input_textbox.send_keys(text)
        self.PROMPT_TEXT_INPUT +=1 

    # Add Iframe Link with title
    def iframe_link(self,title,link):
        self.flashcard_select.select_by_value("iframe_link")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        iframe_title = self.browser.find_element_by_name("question_"+str(self.TITLE_TEXT_COUNT))
        iframe_link = self.browser.find_element_by_name("link_"+str(self.TITLE_TEXT_COUNT))
        iframe_title.send_keys(title)
        iframe_link.send_keys(link)
        self.IFRAME_LINK_COUNT +=1 

    # Add Spead Read function adds a speed read flashcard
    def title_textarea(self,text):
        self.flashcard_select.select_by_value("title_textarea")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        title_textarea_textarea = self.browser.find_element_by_name("title_textarea_"+str(self.TITLE_TEXTAREA_COUNT))
        title_textarea_textarea.send_keys(text)
        self.TITLE_TEXTAREA_COUNT +=1 

    def verify_phone(self):
        self.flashcard_select.select_by_value("verify_phone")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        self.VERIFY_PHONE_COUNT +=1

    def signature_image(self):
        self.flashcard_select.select_by_value("sign_b64")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        self.SIGNATURE_IMAGE_COUNT +=1

    def user_gps(self):
        self.flashcard_select.select_by_value("user_gps")
        add_button = self.browser.find_element_by_id("add")
        add_button.click()
        self.USER_GPS_COUNT +=1

    def test_speed_read(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("Speed Read Test By Bot")
        self.speed_read("Hello There")
        self.submit()
        self.clean_up()

    def test_title_text(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("Title Test Test By Bot")
        self.title_text("Test Title","Test TExt")
        self.submit()
        self.clean_up()

    def test_prompt_text_input(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("Prompt Test Input By Bot")
        self.prompt_text_input("Enter Text")
        self.submit()
        self.clean_up()

    def test_iframe_link(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("Iframe Link By Bot")
        self.iframe_link("Iframe Title","https://swornim.me")
        self.submit()
        self.clean_up()

    def test_title_text_area(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("Title Textarea Test By Bot")
        self.title_textarea("Test Title")
        self.submit()
        self.clean_up()
    
    def test_verify_phone(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("Verify Phone Test By Bot")
        self.verify_phone()
        self.submit()
        self.clean_up()

    def test_signature(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("Signature Test By Bot")
        self.signature_image()
        self.submit()
        self.clean_up()

    def test_user_gps(self):
        self.login()
        self.go_to_lesson_builder()
        self.edit_lesson_name("User GPS Test By Bot")
        self.signature_image()
        self.submit()
        self.clean_up()

if __name__ == '__main__':
    unittest.main()