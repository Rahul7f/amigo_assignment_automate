from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def startQuiz(driver):
    attemptQuizButton = driver.find_element(
        By.XPATH,
        '//input[@value="Attempt quiz" or @value="Continue attempt"] | //button[text()="Attempt quiz" or text()="Continue your attempt"]'
    )
    attemptQuizButton.click()

def selectRandomOption(driver):
    question_div = driver.find_element(By.XPATH, '//*[starts-with(@id, "question-")]')
    answer_div = question_div.find_element(By.CLASS_NAME, "answer")
    option_divs = answer_div.find_elements(By.CSS_SELECTOR, 'div')
    random.choice(option_divs).click()


def processAssignment(driver):
    while True:
        selectRandomOption(driver)
        time.sleep(1)
        try:
            next_button = driver.find_element(By.XPATH, '//input[@value="Next page"]')
            next_button.click()
            time.sleep(2)
        except:
            try:
                finish_button = driver.find_element(By.XPATH, '//input[@value="Finish attempt ..."]')
                finish_button.click()
                time.sleep(2)

                driver.find_element(By.XPATH, '//button[text()="Submit all and finish"]').click()
                time.sleep(2)
                # Click popup "Submit all and finish" button
                popup_submit = driver.find_element(By.XPATH,
                                                   '//*[@id="page-mod-quiz-summary"]/div[6]/div[2]/div/div/div[3]/button[2]')
                popup_submit.click()
                time.sleep(2)
                break
            except:
                break


USERNAME = "rahulsingh5@amityonline.com"
PASSWORD = "AU05212000"
assignmentLink = "https://amigo.amityonline.com/mod/quiz/view.php?id=325810"

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

# 4. Go to the assignments section
driver.get(assignmentLink)
time.sleep(5)
# 5. Click on the assignment link
startQuiz(driver)
time.sleep(2)
processAssignment(driver)

# 7. Close the browser
driver.quit()
