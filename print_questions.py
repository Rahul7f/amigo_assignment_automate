from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# Replace with your actual Amity credentials
USERNAME = "rahulsingh5@amityonline.com"
PASSWORD = "AU05212000"
ASSIGNMENT_URL = "https://amigo.amityonline.com/mod/quiz/attempt.php?attempt=57329023&cmid=143340"

# Start the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 1. Go to login page
driver.get("https://amigo.amityonline.com/login/index.php")
time.sleep(3)

# 2. Fill in username and password
driver.find_element(By.ID, "username").send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)

# 3. Click the login button
driver.find_element(By.ID, "loginbtn").click()
time.sleep(5)  # Wait for redirect after login

# 4. Go to the assignments section directly
driver.get(ASSIGNMENT_URL)
time.sleep(5)  # Wait for the page to load

# 5. Scraping the quiz page directly
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract the questions and options
questions = []
question_elements = soup.select('div.que')

for question in question_elements:
    question_data = {}

    # Extract the question number (h3 element inside each question wrapper)
    question_number = question.select_one('h3')
    question_data['question_number'] = question_number.text.strip() if question_number else 'N/A'

    # Extract the question text (div.qtext)
    question_text = question.select_one('div.qtext')
    question_data['question_text'] = question_text.text.strip() if question_text else 'N/A'

    # Extract the options (fieldset inside each question wrapper)
    options = []
    option_elements = question.select('fieldset')
    for option in option_elements:
        options.append(option.text.strip())

    question_data['options'] = options

    # Append the extracted data to the questions list
    questions.append(question_data)

# 6. Print the extracted data
for question in questions:
    print(f"Question Number: {question['question_number']}")
    print(f"Question Text: {question['question_text']}")
    print("Options:")
    for option in question['options']:
        print(f" - {option}")
    print("\n")

# 7. Close the browser
driver.quit()
