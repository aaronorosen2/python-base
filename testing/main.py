from time import time
from selenium.webdriver import Firefox
from selenium.webdriver.support.select import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SPEED_READ_COUNT = 0
TITLE_TEXT_COUNT =0
PROMPT_TEXT_INPUT = 0
IFRAME_LINK_COUNT =0
TITLE_TEXTAREA_COUNT=0
VERIFY_PHONE_COUNT=0
SIGNATURE_IMAGE_COUNT=0
# Login action will get the username element, password element and login button element.
# Then it fills up the elements and clicks the login button
def loginAction(browser):
    username= browser.find_element_by_id("username") # Username element
    password = browser.find_element_by_id("pwd") # Password Element 
    login_button = browser.find_element_by_class_name("login-button") # Login button element

    username.send_keys("bot@dreampotential.org") # Enter the username
    password.send_keys("iamnotbot") # Enter the password
    login_button.click() #Click the login button

# Edit Lesson Name Edits the lesson name of the segment builder
def edit_lesson_name(browser,name):
    name_input = browser.find_element_by_id("lesson_name")
    name_input.send_keys(name)

# Add Spead Read function adds a speed read flashcard
def speed_read(browser,flashcard_select,text):
    global SPEED_READ_COUNT
    flashcard_select.select_by_value("speed_read")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    speed_read_textbox = browser.find_element_by_name("speed_read_"+str(SPEED_READ_COUNT))
    speed_read_textbox.send_keys(text)
    SPEED_READ_COUNT +=1 

# Add Title text function adds title text flashcard
def title_text(browser,flascard_select,title, text):
    global TITLE_TEXT_COUNT
    flashcard_select.select_by_value("title_text")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    title_text_title = browser.find_element_by_name("title_"+str(TITLE_TEXT_COUNT))
    title_text_text = browser.find_element_by_name("text_"+str(TITLE_TEXT_COUNT))
    title_text_title.send_keys(title)
    title_text_text.send_keys(text)
    TITLE_TEXT_COUNT +=1

# Add Prompt Text Input flashcard - Also called Title Input
def prompt_text_input(browser,flashcard_select,text):
    global PROMPT_TEXT_INPUT
    flashcard_select.select_by_value("title_input")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    prompt_text_input_textbox = browser.find_element_by_name("title_input_textarea_"+str(PROMPT_TEXT_INPUT))
    prompt_text_input_textbox.send_keys(text)
    PROMPT_TEXT_INPUT +=1 

# Add Iframe Link with title
def iframe_link(browser,flashcard_select,title,link):
    global IFRAME_LINK_COUNT
    flashcard_select.select_by_value("iframe_link")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    iframe_title = browser.find_element_by_name("question_"+str(TITLE_TEXT_COUNT))
    iframe_link = browser.find_element_by_name("link_"+str(TITLE_TEXT_COUNT))
    iframe_title.send_keys(title)
    iframe_link.send_keys(link)
    IFRAME_LINK_COUNT +=1 

# Add Spead Read function adds a speed read flashcard
def title_textarea(browser,flashcard_select,text):
    global TITLE_TEXTAREA_COUNT
    flashcard_select.select_by_value("title_textarea")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    title_textarea_textarea = browser.find_element_by_name("title_textarea_"+str(TITLE_TEXTAREA_COUNT))
    title_textarea_textarea.send_keys(text)
    TITLE_TEXTAREA_COUNT +=1 

def verify_phone(browser,flashcard_select):
    global VERIFY_PHONE_COUNT
    flashcard_select.select_by_value("verify_phone")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    VERIFY_PHONE_COUNT +=1

def signature_image(browser,flashcard_select):
    global SIGNATURE_IMAGE_COUNT
    flashcard_select.select_by_value("sign_b64")
    add_button = browser.find_element_by_id("add")
    add_button.click()
    SIGNATURE_IMAGE_COUNT +=1

browser = Firefox() # Using Firefox browser, you need to have geckodriver installed for this to work!

browser.get("localhost:8086") 
try:
    #wait till the title appears
    WebDriverWait(browser,20).until(EC.title_contains("Teacher Portal"))
    loginAction(browser)
except:
    print("[*] Error Opening the login page")
    browser.quit()

try:
    #after the title appears login and wait until the dashboard shows up.
    # had to wait till the dashboard_title appeared because otherwise the teacher ui takes time to store the token
    WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard_title")))
    browser.get("localhost:8086/lesson.html") # Goto Login builder, used it directly.
except:
    print("[*] Error Opening the dashboard")
    browser.quit()

WebDriverWait(browser,20).until(EC.presence_of_element_located((By.ID, "selectsegment")))
flashcard_select =Select(browser.find_element_by_id("selectsegment"))

edit_lesson_name(browser,"Test 1")
iframe_link(browser,flashcard_select,"Iframe","swornim.me")
speed_read(browser,flashcard_select,"Hello") #user this function to add speed read
prompt_text_input(browser,flashcard_select,"Hello 2") #user this function to add speed read
title_text(browser,flashcard_select,"This is title","This is Text")
title_textarea(browser,flashcard_select,"Title Textarea")
verify_phone(browser,flashcard_select)
signature_image(browser,flashcard_select)
time.sleep(10)

browser.quit()
