from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

    open_profile()
    time.sleep(1)
    print(scrape_relationship_type())
