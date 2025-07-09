import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

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


def run_selenium(email_input, password_input):
    try:
        options = Options()
        # options.add_argument("--headless=new")  # Optional: run without opening browser window
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)

        driver.get("https://next.amboss.com/us/login")
        driver.maximize_window()

        email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password = driver.find_element(By.NAME, "password")
        login_btn = driver.find_elements(By.TAG_NAME, "button")[1]

        email.send_keys(email_input)
        password.send_keys(password_input)
        login_btn.click()

        # Wait for assignments section
        wait.until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "_4cc9ddf83d96bbf8--header"))
            == 8
        )
        assignments = driver.find_elements(By.CLASS_NAME, "_4cc9ddf83d96bbf8--header")[
            1
        ]
        assignments.click()

        # Wait and click resume
        resume_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1vafa9z-StyledButton"))
        )
        resume_btn.click()

        # Load answers
        with open("answers.pkl", "rb") as file:
            answers = pickle.load(file)

        # Get question range from URL
        url = driver.current_url
        start = int(url[48 : url.index("?")])
        end = 1205

        # Wait for tabs
        wait.until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "ed71ad0ad070e9f8--item")) > 0
        )
        tabs = driver.find_elements(By.CLASS_NAME, "ed71ad0ad070e9f8--item")

        # Start answering
        tabs[start - 1].click()
        question_id = start

        for tab in tabs[start : end + 1]:
            answer_index = dictionary[answers[question_id - 1][1]]
            wait.until(
                lambda d: len(
                    d.find_elements(By.CLASS_NAME, "_981f8b48b6542a07--letterAndText")
                )
                >= 2
            )
            options = driver.find_elements(
                By.CLASS_NAME, "_981f8b48b6542a07--letterAndText"
            )

            target_option = options[answer_index]
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", target_option
            )
            time.sleep(1)

            target_option.click()
            tab.click()
            question_id += 1

        st.success("✅ Automation completed successfully!")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
    finally:
        driver.quit()


# === Streamlit UI ===
st.title("AMBOSS Assignment Automation")
st.markdown(
    """
**What does this app do:**

It auto-answers the questions of **SCFHS R1 Required Learning FM [2024]** in AMBOSS (1205 total questions).  
All the answers are taken from the `answers.pkl` file which answers are extracted from the PDF file.

**Requirements & Notes:**  
- You must have **Google Chrome** installed.  
- **Do NOT minimize the browser** once the automation starts (recommended to run it before you sleep).  
- Questions **1001-1036** are auto-answered with **'A'** since they are not in the answers file.
"""
)

email_input = st.text_input("Email")
password_input = st.text_input("Password", type="password")

if st.button("Run Automation"):
    if email_input and password_input:
        run_selenium(email_input, password_input)
    else:
        st.warning("Please enter both email and password.")
st.markdown("Made with 💚 by Fares")
