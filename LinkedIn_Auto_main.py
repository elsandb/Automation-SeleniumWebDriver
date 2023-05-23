from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import os

# "no:" = Norwegian (in the #comments).

# CONSTANTS
MY_EMAIL = os.environ['MY_EMAIL']
MY_PASSWORD = os.environ['MY_PASS']
CHROME_DRIVER_PATH = 'C:/Development/chromedriver.exe'
JOB_SEARCH_URL = 'https://www.linkedin.com/jobs/search/?currentJobId=3431673965&f_AL=true&f_E=1%2C2%2C3&f_PP=10421626' \
                 '4&geoId=103819153&keywords=Python&location=Norge&refresh=true&sortBy=DD'

# OBJECTS
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.maximize_window()    # Maximize browser window
wait = WebDriverWait(driver, 10)


def check_toast_item():
    """If there are any 'toast-items', they will be closed. (Toast-item: The confirmation message
    that show up in the lower left corner when you click 'save' or 'follow'.)"""
    toast_exist = True
    while toast_exist:
        try:
            dismiss_toast_button = driver.find_element(By.CSS_SELECTOR, 'button.artdeco-toast-item__dismiss')
        except NoSuchElementException:
            # print('---- No toasts.')
            toast_exist = False
        else:
            dismiss_toast_button.click()
            # print('---- Toast was eaten.')
            sleep(3)


# -------------- START ----------------------------------#
# ----- Get PAGE 1 --> Says "you have to log in." ----- #
driver.get(JOB_SEARCH_URL)      # Open URL.
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                       'div.artdeco-global-alert-action__wrapper '
                                       '> button:nth-child(2)'))).click()   # Decline cookies.
driver.find_element(By.LINK_TEXT, 'Logg på').click()   # Click "log in" (no: "Logg på").


# ----- PAGE 2 --> Input email, password ----- #
driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(MY_EMAIL)
driver.find_element(By.CSS_SELECTOR, 'input#password').\
    send_keys(MY_PASSWORD, Keys.ENTER)  # Enter password + press 'ENTER'.
print('Log in done')
sleep(4)


# ----- PAGE 3 --> LinkedIn's job search page ----- #
driver.find_element(By.CSS_SELECTOR, '#ember116').click()   # Minimize messages.

# Save all job announcements and follow the companies:
search_results = driver.find_elements(By.CSS_SELECTOR, 'div > ul.scaffold-layout__list-container > li')

for result in search_results[:5]:   # Here I only go through the first 5 postings (index 0 - 4 (incl. 4)).
    # Get job announcement title:
    result_id = result.get_attribute('id')
    result_title = driver.find_element(By.CSS_SELECTOR, f'li#{result_id} a').text
    print(f"\n* {result_title} *")

    result.click()      # Click on job announcement
    sleep(1)

    # Save job posting (if not already saved).
    save_job_button = driver.find_element(By.CSS_SELECTOR, 'button.jobs-save-button > span:nth-child(1)')
    if save_job_button.text == 'Lagret':    # no: "Lagret" = "Saved"
        print('Already saved.')
    else:
        save_job_button.click()
        print('Job posting saved.')
        sleep(3)
        check_toast_item()

    # Follow company (if not already followed).
    follow_button = driver.find_element(By.CSS_SELECTOR, 'button.follow')
    if follow_button.text == "Følger":  # no: "Følger" = "Following"
        print('Already following.')
    else:
        follow_button.send_keys('')
        follow_button.click()
        print('Clicked on follow.')
        sleep(3)
        check_toast_item()

    sleep(3)
# -------------------- Done ---------------------- #

# # # Console output:
# Log in done
#
# * Frontend Developer *
# Job posting saved.
# Clicked on follow.
#
# * Enterprise Architect (f/m/d) *
# Already saved.
# Clicked on follow.
#
# * Dataingeniør *
# Already saved.
# Already following.
#
# * Maskinsyn og automasjonsingeniør *
# Job posting saved.
# Clicked on follow.
#
# * Database developer, Oslo *
# Job posting saved.
# Clicked on follow.
#
# Process finished with exit code 0
