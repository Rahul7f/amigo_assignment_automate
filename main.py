from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Replace with your actual Amity credentials
USERNAME = "rahulsingh5@amityonline.com"
PASSWORD = "AU05212000"

ASSIGNEMT_URL = "https://amigo.amityonline.com/course/view.php?id=3194&section=5"
ul_element_tag = "coursecontentcollapse5"


def loopLiElement(driver):
    # Loop through LI elements
    for index, li in enumerate(li_elements, start=1):
        try:
            class_name = li.get_attribute("class")
            # get spain
            span = li.find_element(By.XPATH, './/span')
            title_text = span.text
            # get inner html of li
            button = li.find_element(By.XPATH, './/button[starts-with(@id, "dropwdownbutton_")]')
            button_text = button.text.strip()
            if button_text.lower() == "done":
                continue

            if "Module Assessment" in title_text:
                print(f"[{index}] Module Assessment → skipping")
                return

            if "modtype_page" in class_name or "modtype_quiz" in class_name:
                link_element = li.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute("href")

                # Open link in new tab
                driver.execute_script("window.open(arguments[0]);", href)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(5)

                if "modtype_page" in class_name:
                    print(f"[{index}] Visited PAGE → closing tab")
                    driver.close()

                elif "modtype_quiz" in class_name:
                    try:
                        # 5. Click on the assignment link
                        startQuiz(driver)
                        time.sleep(2)
                        processAssignment(driver)
                    except:
                        print(f"[{index}] QUIZ → Title not found or page load issue")
                    driver.close()

                # Switch back to main tab
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)

        except Exception as e:
            print(f"[{index}] Error: in loopLiElement function {e}")
            continue


def startQuiz(driver):
    attemptQuizButton = driver.find_element(
        By.XPATH,
        '//input[@value="Attempt quiz" or @value="Continue attempt"] | //button[text()="Attempt quiz" or text()="Continue your attempt"]'
    )
    attemptQuizButton.click()


# def selectRandomOption(driver):
#     question_div = driver.find_element(By.XPATH, '//*[starts-with(@id, "question-")]')
#     answer_div = question_div.find_element(By.CLASS_NAME, "answer")
#     option_divs = answer_div.find_elements(By.CSS_SELECTOR, 'div')
#     random.choice(option_divs).click()


def selectRandomOption(driver):
    question_divs = driver.find_elements(By.XPATH, '//*[starts-with(@id, "question-")]')
    print(f"Total Questions: {len(question_divs)}")

    for i in range(len(question_divs)):
        question_div = driver.find_elements(By.XPATH, '//*[starts-with(@id, "question-")]')[i]
        print(f"\nProcessing Question {i + 1}")

        answer_div = question_div.find_element(By.CLASS_NAME, "answer")
        option_divs = answer_div.find_elements(By.CSS_SELECTOR, 'div.r0, div.r1')
        random_div = random.choice(option_divs)

        try:
            # Scroll to input before clicking
            label_div = random_div.find_element(By.CSS_SELECTOR, 'div.d-flex.w-auto')
            driver.execute_script("arguments[0].scrollIntoView(true);", label_div)
            driver.execute_script("arguments[0].click();", label_div)
            print(f"✅ Selected option: {random_div.text.strip()}\n")
        except Exception as e:
            print(f"❌ Failed to click: {e}\n")


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

                popup = driver.find_element(By.CSS_SELECTOR, '.modal-dialog.modal-dialog-scrollable')
                popup_submit = popup.find_element(By.XPATH, './/button[text()="Submit all and finish"]')
                driver.execute_script("arguments[0].click();", popup_submit)
                time.sleep(2)
                break
            except:
                break


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
driver.get(ASSIGNEMT_URL)
time.sleep(5)

# 5. Extract all <ul> elements with specific class
# Find the <ul> element
# //*[@id="coursecontentcollapse5"]/ul
# ul_element = driver.find_element(By.XPATH, '//*[starts-with(@id, "coursecontentcollapse")]/ul')
ul_element = driver.find_element(By.XPATH, f'//*[@id="section-4"]/div[2]/ul')

# Find all <li> elements inside the <ul>
li_elements = ul_element.find_elements(By.TAG_NAME, "li")

# Loop through <li> elements and print their class names
# Loop through LI elements
loopLiElement(driver)

# 7. Close the browser
driver.quit()
