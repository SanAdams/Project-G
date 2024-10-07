from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
import DatingAppUser

def safe_get_element_text(by:By, value:str):
    try:
        element = driver.find_element(by, value)
        return element.text.strip()
    except NoSuchElementException:
        return ""

def safe_get_element(by:By, value:str):
    try:
        element = driver.find_element(by, value)
        return element
    except NoSuchElementException:
        return None

def open_profile():
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.ARROW_UP)
    return

def scrape_name():
    name = driver.find_element(By.XPATH, '//span[@class="Pend(8px)"]').text
    return name

def scrape_age():
    age = driver.find_element(By.XPATH, '//span[@class="Whs(nw) Typs(display-2-strong)"]').text
    return int(age)

def next_profile():
    pass_button = driver.find_element(By.XPATH, '//div[@class="gamepad-button-wrapper Mx(a) Fxs(0) Sq(70px) Sq(60px)--s"][1]')
    pass_button.click()
    return

def scrape_relationship_type():
    relationship_type = safe_get_element_text(By.XPATH, '//div[@class="Typs(subheading-1) CenterAlign"]')
    return relationship_type

def scrape_lifestyle():
    basics_container = safe_get_element(By.XPATH, '//h2[text()="Basics"]/following-sibling::div[1]')
    return

def scrape_basics():    
    pass

def scrape_interests():
    pass

def scrape_top_spotify_artists():
    pass

def scrape_anthem():
    pass

def scrape_languages():
    pass

if __name__ == '__main__':
    NUM_PROFILES = 1

    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Path to chromedriver.exe
    service = Service("D:/FUNSIES/Project G/chromedriver-win64/chromedriver.exe")

    # Initialize WebDriver with Service and ChromeOptions
    driver = webdriver.Chrome(service=service, options=options)

    user = DatingAppUser.DatingAppUser()

    open_profile()
    time.sleep(1)
    print(scrape_relationship_type())
    