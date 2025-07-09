from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time


driver = webdriver.Chrome()
driver.get("https://next.amboss.com/us/login")
email = driver.find_element(By.NAME, "email")
password = driver.find_element(By.NAME, "password")
login_btn = driver.find_elements(By.TAG_NAME, "button")[1]

email.send_keys("njoudalabdullatif@gmail.com")
password.send_keys("OhDarling7!")
login_btn.click()
time.sleep(5)
import pickle

with open("answers.pkl", "rb") as file:
    answers = pickle.load(file)
dictionary = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
}
start = 1
end = 1205

driver.get(
    f"https://next.amboss.com/us/questions/eMqo0xn_1S/{start}?fromUrl=%2Fus%2Feducator-tools%2Fuser-assignments%2FUfbblG"
)
tabs = driver.find_elements(By.CLASS_NAME, "ed71ad0ad070e9f8--item")
len(tabs)
question_id = start
for tab in tabs[start : end + 1]:
    answer_index = dictionary[answers[question_id - 1][1]]
    options = driver.find_elements(By.CLASS_NAME, "_981f8b48b6542a07--letterAndText")
    target_option = options[answer_index]

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", target_option
    )
    time.sleep(1)

    target_option.click()
    tab.click()
    question_id += 1
