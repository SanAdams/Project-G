from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import re
import DatingAppUser
NUM_PROFILES_TO_SCRAPE = 1000

def safe_get_element(by:By, value:str):
    try:
        element = driver.find_element(by, value)
        return element
    except NoSuchElementException:
        return ""
    
def scrape_name_card():
    name = safe_get_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[1]').text.strip()
    age = safe_get_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[2]').text.strip().replace(",", "")
    profession = safe_get_element(By.CLASS_NAME, 'encounters-story-profile__occupation').text.strip()
    return (name, age, profession)

""" def scrape_bio_card():
    height =
    exercise =
    education_level = 
    drinking_frequency = 
    smoking_frequency = 
    weed_smoking_frequency = 
    relationship_type = 
    family_plans = 
    star_sign = 
    political_leaning = 
    religion =  """

def scrape_picture_card():
    pass

def determine_location_type(location: str):
    if "Lives in" in location:
        return "residential"
    else:
        return "home_town"

def clean_location_text(location: str):
    if determine_location_type(location) == 'home_town':
        cleaned_location_text = re.sub(r".*?\bFrom\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b.*", r"\1", location)
    else:
        cleaned_location_text = re.sub(r".*?\bLives in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b.*", r"\1", location)
    return cleaned_location_text.strip()

def scrape_location_card():
    current_location = safe_get_element(By.CLASS_NAME, 'location-widget__town').text.strip()
    location_widget_element = safe_get_element(By.CLASS_NAME, 'location-widget__info')
    home_town = ""
    residential_location = "" 

    if location_widget_element: 
        location_widget_pills= location_widget_element.find_elements(By.CLASS_NAME, 'location-widget__pill')
        if len(location_widget_pills) > 1:
            residential_location = clean_location_text(location_widget_pills[0].text)
            home_town = clean_location_text(location_widget_pills[1].text)
        elif len(location_widget_pills) == 1:
            if "Lives in" in location_widget_pills[0].text:
                residential_location = clean_location_text(location_widget_pills[0].text)
            else:
                home_town = clean_location_text(location_widget_pills[0].text)

    top_spotify_artists = []
    num_artists = 0
    try:
        top_spotify_artists_list = driver.find_elements(By.CLASS_NAME, 'spotify-widget__artist') 
        num_artists = len(top_spotify_artists_list)
    except NoSuchElementException:
        top_spotify_artists = ""
    
    for i in range (num_artists):
        print(i)
        top_spotify_artists.append(top_spotify_artists_list[i].text.strip())

    return (current_location, home_town, residential_location, top_spotify_artists)

def scroll_down(multiplier: int):
    scrollDown = f'-{multiplier * 100}%'
    albumContainer = safe_get_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
    driver.execute_script(f"arguments[0].style.transform = 'translateY({scrollDown})';", albumContainer)

if __name__ == '__main__':
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Path to chromedriver.exe
    service = Service("D:/FUNSIES/Project G/chromedriver-win64/chromedriver.exe")

    # Initialize WebDriver with Service and ChromeOptions
    driver = webdriver.Chrome(service=service, options=options)

    # Make new user to store data
    user = DatingAppUser.DatingAppUser()
 
    # Get the number of cards
    """ profile_cards = driver.find_elements(By.CLASS_NAME, 'encounters-album__story')
    num_cards = len(profile_cards)
    print(scrape_name_card()) """

    current_location, from_location, residential_location, top_spotify_artists = scrape_location_card()

    """ if current_location:
        print(current_location) """
    """ if from_location:
        print(from_location) """
    """ if residential_location:
        print(residential_location) """
    if top_spotify_artists:
        print(top_spotify_artists)


    """ pass_button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[2]/div')
    pass_button.click() """
    