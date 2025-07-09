# SleepySolver 💤

SleepySolver is a simple Streamlit web app that automates answering the **SCFHS R1 Required Learning FM [2024]** assignment on AMBOSS. It uses Selenium to log in, navigate, and answer 1205 questions using an answer key (`answers.pkl`).

## Features

- ✅ Auto-answers 1205 questions from the assignment
- 📂 Uses a preloaded answer file (`answers.pkl`)
- 💻 Requires Google Chrome installed
- 😴 Recommended to run before you sleep
- 🅰️ Questions 1001–1036 are answered with "A" by default (missing in answer file)

## Requirements

- Google Chrome
- Chromedriver installed and added to PATH
- `answers.pkl` in the same directory
- Python + dependencies (`streamlit`, `selenium`, etc.)

## Run the App

```bash
streamlit run app.py
```
