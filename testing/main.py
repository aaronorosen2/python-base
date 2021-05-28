from time import time
from selenium.webdriver import Firefox
from selenium.webdriver.support.select import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

SPEED_READ_COUNT = 0

# Login action will get the username element, password element and login button element.
# Then it fills up the elements and clicks the login button
def loginAction(browser):
    username= browser.find_element_by_id("username") # Username element
    password = browser.find_element_by_id("pwd") # Password Element 
    login_button = browser.find_element_by_class_name("login-button") # Login button element

    username.send_keys("bot@dreampotential.org") # Enter the username
    password.send_keys("iamnotbot") # Enter the password
    login_button.click() #Click the login button

def add_lesson_name(browser,name):
    name_input = browser.find_element_by_id("lesson_name")
    name_input.send_keys(name)

def add_speed_read(browser,flashcard_select,text):
    global SPEED_READ_COUNT
    flashcard_select.select_by_value("speed_read")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    speed_read_textbox = browser.find_element_by_name("speed_read_"+str(SPEED_READ_COUNT))
    speed_read_textbox.send_keys(text)
    SPEED_READ_COUNT +=1 

browser = Firefox() # Using Firefox browser, you need to have geckodriver installed for this to work!

browser.get("localhost:8086") 
try:
    #wait till the title appears
    WebDriverWait(browser,10).until(EC.title_contains("Teacher Portal"))
    loginAction(browser)
except:
    print("[*] Error Opening the login page")
    browser.quit()

try:
    #after the title appears login and wait until the dashboard shows up.
    # had to wait till the dashboard_title appeared because otherwise the teacher ui takes time to store the token
    WebDriverWait(browser,5).until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard_title")))
    browser.get("localhost:8086/lesson.html") # Goto Login builder, used it directly.
except:
    print("[*] Error Opening the dashboard")
    browser.quit()

WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID, "selectsegment")))
flashcard_select =Select(browser.find_element_by_id("selectsegment"))

add_lesson_name(browser,"Test 1")
add_speed_read(browser,flashcard_select,"Hello") #user this function to add speed read
add_speed_read(browser,flashcard_select,"Hello 2") #user this function to add speed read

time.sleep(10)

browser.quit()
