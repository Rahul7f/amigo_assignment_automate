from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# ================= CONFIG =================

USERNAME = "rahulsingh5@amityonline.com"
PASSWORD = "AU05212000"

ASSIGNEMT_URL = "https://amigo.amityonline.com/course/view.php?id=3194&section=8"
ul_element_tag = "courseindexcollapse8"

# ================= QUIZ FUNCTIONS (UNCHANGED) =================

def startQuiz(driver):
    attemptQuizButton = driver.find_element(
        By.XPATH,
        '//input[@value="Attempt quiz" or @value="Continue attempt"]'
        ' | //button[text()="Attempt quiz" or text()="Continue your attempt"]'
    )
    attemptQuizButton.click()


def selectRandomOption(driver):
    question_divs = driver.find_elements(By.XPATH, '//*[starts-with(@id, "question-")]')
    print(f"Total Questions: {len(question_divs)}")

    for i in range(len(question_divs)):
        question_div = question_divs[i]
        print(f"Processing Question {i + 1}")

        answer_div = question_div.find_element(By.CLASS_NAME, "answer")
        option_divs = answer_div.find_elements(By.CSS_SELECTOR, 'div.r0, div.r1')

        if not option_divs:
            continue

        random_div = random.choice(option_divs)

        try:
            label_div = random_div.find_element(By.CSS_SELECTOR, 'div.d-flex.w-auto')
            driver.execute_script("arguments[0].scrollIntoView(true);", label_div)
            driver.execute_script("arguments[0].click();", label_div)
        except Exception as e:
            print("Option click failed:", e)


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

                popup = driver.find_element(By.CSS_SELECTOR, '.modal-dialog')
                popup_submit = popup.find_element(
                    By.XPATH, './/button[text()="Submit all and finish"]'
                )
                driver.execute_script("arguments[0].click();", popup_submit)
                time.sleep(2)
                break
            except:
                break

# ================= MAIN SCRIPT =================

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 1. Login
driver.get("https://amigo.amityonline.com/login/index.php")
time.sleep(3)

driver.find_element(By.ID, "username").send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.ID, "loginbtn").click()
time.sleep(5)

# 2. Open assignment page
driver.get(ASSIGNEMT_URL)
time.sleep(5)

# 3. Click "Open course index" button
try:
    driver.find_element(
        By.XPATH, '//*[@id="topofscroll"]/div/div[1]/div[1]/button'
    ).click()
except Exception as e:
    print("Course index button not found:", e)

time.sleep(5)

# 4. Get course index UL
ul_element = driver.find_element(
    By.XPATH, f'//*[@id="{ul_element_tag}"]/ul'
)

li_elements = ul_element.find_elements(By.TAG_NAME, "li")
print(f"Total items: {len(li_elements)}")

# 5. Loop items
for index, li in enumerate(li_elements, start=1):

    a_tags = li.find_elements(By.TAG_NAME, "a")
    if not a_tags:
        continue

    a_tag = a_tags[0]
    link = a_tag.get_attribute("href")
    title = a_tag.text.strip()

    span_tags = li.find_elements(By.XPATH, './/span[@data-for="cm_completion"]')
    data_value = span_tags[0].get_attribute("data-value") if span_tags else None

    # Skip completed
    if data_value == "1":
        continue

    # Only quizzes
    if not title.startswith("Quiz"):
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)
        #close tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        continue

    print(f"[{index}] QUIZ FOUND")
    print("Title:", title)
    print("Link:", link)
    print("----")

    # Open quiz in new tab
    driver.execute_script("window.open(arguments[0]);", link)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)

    try:
        startQuiz(driver)
        time.sleep(2)
        processAssignment(driver)
    except Exception as e:
        print("Quiz error:", e)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)

# 6. Done
driver.quit()