from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from collections import defaultdict
import time
import DatingAppUser


def safe_get_element_text(by: By, value: str):
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
    open_profile_button = driver.find_element(
        By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div/div[1]/button')
    open_profile_button.click()
    return


def scrape_name():
    name = driver.find_element(
        By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/h1/span[1]')
    return name


def scrape_age():
    age = int(driver.find_element(
        By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/h1/span[2]'))
    return


def next_profile():
    pass_button = driver.find_element(
        By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/button')
    pass_button.click()
    return


def scrape_relationship_type():
    relationship_type = safe_get_element_text(
        By.XPATH, '//*[@id="q1029118820"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[4]/div/div/div/div')
    return relationship_type

def scrape_basics():
    # Make default value of any key a ""
    basic_attributes = defaultdict(lambda: "")
    try:
        basics_spans = driver.find_elements(By.XPATH, '//h2[text()="Basics"]//following-sibling::div//div//span')
    except NoSuchElementException:
        return basic_attributes
    # Match the attribute text to the attribute
    if basics_spans:  
        for span in basics_spans:
            if span.text.strip() == "Education":
                basic_attributes['education_level'] = span.find_element(By.XPATH, './following-sibling::div').text
            if span.text.strip() == "Love Style":
                basic_attributes['love_language'] = span.find_element(By.XPATH, './following-sibling::div').text
            if span.text.strip() == "Communication Style":
                basic_attributes['communication_style'] = span.find_element(By.XPATH, './following-sibling::div').text
            if span.text.strip() == "Zodiac":
                basic_attributes['star_sign'] = span.find_element(By.XPATH, './following-sibling::div').text
            if span.text.strip() == "Family Plans":
                basic_attributes['family_plans'] = span.find_element(By.XPATH, './following-sibling::div').text
            if span.text.strip() == "COVID Vaccine":
                basic_attributes['vaccination_status'] = span.find_element(By.XPATH, './following-sibling::div').text
            if span.text.strip() == "Personality Type":
                basic_attributes['personality_type'] = span.find_element(By.XPATH, './following-sibling::div').text
    return basic_attributes

def scrape_lifestyle():
    lifestlye_attributed = {lambda: ""}
    
def scrape_interests():
    pass

def scrape_top_spotify_artists():
    pass

def scrape_anthem():
    pass

def scrape_languages():
    pass
#TODO: Change the time.sleep waits into explicit waits from selenium
if __name__ == '__main__':
    NUM_PROFILES = 1

    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Fetch the path from the environment variable
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')

    # Path to chromedriver.exe
    service = Service(chromedriver_path)

    # Initialize WebDriver with Service and ChromeOptions
    driver = webdriver.Chrome(service=service, options=options)

    user = DatingAppUser.DatingAppUser()

    # for i in range(NUM_PROFILES):
    #     open_profile()
    #     pass
