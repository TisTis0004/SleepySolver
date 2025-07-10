import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

ANSWER_MAP = {chr(ord("A") + i): i for i in range(10)}


def run_automation(email_input, password_input, status_label):
    try:
        status_label.config(text="Starting Chrome...")
        root.update()

        options = Options()
        # options.add_argument("--headless")  # Optional for GUI-less operation

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)

        status_label.config(text="Logging in to AMBOSS...")
        root.update()

        driver.get("https://next.amboss.com/us/login")
        driver.maximize_window()

        email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password = driver.find_element(By.NAME, "password")
        login_btn = driver.find_elements(By.TAG_NAME, "button")[1]

        email.send_keys(email_input)
        password.send_keys(password_input)
        login_btn.click()

        wait.until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "_4cc9ddf83d96bbf8--header"))
            == 8
        )
        assignments = driver.find_elements(By.CLASS_NAME, "_4cc9ddf83d96bbf8--header")[
            1
        ]
        assignments.click()

        resume_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1vafa9z-StyledButton"))
        )
        resume_btn.click()

        with open("answers.pkl", "rb") as file:
            answers = pickle.load(file)

        url = driver.current_url
        start = int(url[48 : url.index("?")])
        end = 1205

        wait.until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "ed71ad0ad070e9f8--item")) > 0
        )
        tabs = driver.find_elements(By.CLASS_NAME, "ed71ad0ad070e9f8--item")
        tabs[start - 1].click()

        question_id = start
        for tab in tabs[start : end + 1]:
            answer_letter = (
                answers[question_id - 1][1]
                if question_id < 1001 or question_id > 1036
                else "A"
            )
            answer_index = ANSWER_MAP.get(answer_letter, 0)

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

        driver.quit()
        status_label.config(text="✅ Automation completed successfully!")

    except Exception as e:
        status_label.config(text=f"❌ Error: {e}")


# GUI
root = tk.Tk()
root.title("AMBOSS Automation")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack()

status_label = tk.Label(root, text="", fg="green", wraplength=380, justify="left")
status_label.pack(pady=20)


def on_click():
    email = email_entry.get()
    password = password_entry.get()
    if not email or not password:
        messagebox.showwarning(
            "Input Required", "Please enter both email and password."
        )
        return
    run_automation(email, password, status_label)


tk.Button(root, text="Run Automation", command=on_click).pack(pady=10)
tk.Label(root, text="Made with 💚 by Fares", fg="gray").pack(pady=(10, 5))

root.mainloop()
