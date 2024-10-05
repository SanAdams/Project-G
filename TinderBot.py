from selenium import webdriver
from selenium.webdriver.common.by import By
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

# def safe_get_element(by:By, value:str):
#     try:
#         element = driver.find_element(by, value)
#         return element
#     except NoSuchElementException:
#         return None

def open_profile():
    open_profile_button = driver.find_element(By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div/div[1]/button')
    open_profile_button.click()
    return

def scrape_name():
    name = driver.find_element(By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/h1/span[1]')
    return name

def scrape_age():
    age = int(driver.find_element(By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/h1/span[2]'))
    return

def next_profile():
    pass_button = driver.find_element(By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/button')
    pass_button.click()
    return

def scrape_relationship_type():
    relationship_type = safe_get_element_text(By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[4]/div/div/div/div')
    return relationship_type

if __name__ == '__main__':
    NUM_PROFILES = 1

    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Path to chromedriver.exe
    service = Service("D:/FUNSIES/Project G/chromedriver-win64/chromedriver.exe")

    # Initialize WebDriver with Service and ChromeOptions
    driver = webdriver.Chrome(service=service, options=options)

    user = DatingAppUser.DatingAppUser()

    # for i in range(NUM_PROFILES):
    #     open_profile()
    #     pass

