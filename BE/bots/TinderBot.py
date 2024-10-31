from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
import os
import time
import DatingAppUser
from dotenv import load_dotenv

def safe_get_element_text(by: By, value: str):
    try:
        element = driver.find_element(by, value)
        return element.text.strip()
    except NoSuchElementException:
        return ""


def safe_get_element(by: By, value: str):
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
    age = driver.find_element(
        By.XPATH, '//span[@class="Whs(nw) Typs(display-2-strong)"]').text
    return int(age)


def next_profile():
    pass_button = driver.find_element(
        By.XPATH, '//div[@class="gamepad-button-wrapper Mx(a) Fxs(0) Sq(70px) Sq(60px)--s"][1]')
    pass_button.click()
    return


def scrape_relationship_type():
    relationship_type = safe_get_element_text(
        By.XPATH, '//div[@class="Typs(subheading-1) CenterAlign"]')
    return relationship_type


def scrape_basics():
    basic_attributes = defaultdict(lambda: "")

    try:
        # Wait for the "Basics" section to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2[text()="Basics"]'))
        )

        # Locate the Basics section
        basics_section = driver.find_element(
            By.XPATH, '//h2[text()="Basics"]/following-sibling::div'
        )

        # Find all child div elements inside the Basics section
        basics_divs = basics_section.find_elements(By.XPATH, './div')

        for div in basics_divs:
            try:
                script = """
                            let texts = [];
                            let children = arguments[0].childNodes;
                            for (let i = 0; i < children.length; i++) {
                                if (children[i].nodeType === Node.TEXT_NODE || children[i].nodeType === Node.ELEMENT_NODE) {
                                    texts.push(children[i].textContent.trim());
                                }
                            }
                            return texts;
                        """

                attribute_value = driver.execute_script(
                    script, div)

                # Store the attribute and its value in the dictionary
                basic_attributes[attribute_value[0]
                                 ] = attribute_value[2]

            except NoSuchElementException:
                # Debugging
                print(
                    f"Couldn't find expected elements inside this div: {div.get_attribute('outerHTML')}")
                continue

    except NoSuchElementException:
        print("No elements found for basics.")

    return basic_attributes


def scrape_lifestyle():
    lifestyle_attributes = defaultdict(lambda: "")
    try:
        # Wait for the "lifestyle" section to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//h2[text()="Lifestyle"]'))
        )

        # Locate the lifestyle section
        lifestyle_section = driver.find_element(
            By.XPATH, '//h2[text()="Lifestyle"]/following-sibling::div'
        )

        # Find all child div elements inside the lifestyle section
        lifestyle_divs = lifestyle_section.find_elements(By.XPATH, './div')

        for div in lifestyle_divs:
            try:
                script = """
                            let texts = [];
                            let children = arguments[0].childNodes;
                            for (let i = 0; i < children.length; i++) {
                                if (children[i].nodeType === Node.TEXT_NODE || children[i].nodeType === Node.ELEMENT_NODE) {
                                    texts.push(children[i].textContent.trim());
                                }
                            }
                            return texts;
                        """

                attribute_value = driver.execute_script(
                    script, div)

                # Store the attribute and its value in the dictionary
                lifestyle_attributes[attribute_value[0]
                                     ] = attribute_value[2]

            except NoSuchElementException:
                # Debugging
                print(
                    f"Couldn't find expected elements inside this div: {div.get_attribute('outerHTML')}")
                continue

    except NoSuchElementException:
        print("No elements found for lifestyle.")

    return lifestyle_attributes


def scrape_interests():
    pass


def scrape_top_spotify_artists():
    pass


def scrape_anthem():
    pass


def scrape_languages():
    pass

# TODO: Change the time.sleep waits into explicit waits from selenium


if __name__ == '__main__':
    load_dotenv()
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
    basics = scrape_basics()
    pizza = scrape_lifestyle()
    for key, value in pizza.items():
        print(f"{key}: {value}")
for key, value in basics.items():
        print(f"{key}: {value}")