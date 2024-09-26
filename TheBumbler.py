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

def scrape_bio_card():
    attribute_list_element = safe_get_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/ul')
    attribute_images_containers = attribute_list_element.find_elements(By.CLASS_NAME, 'pill__image-box')
    num_attributes = len(attribute_images_containers)
    img_src_map = {
        'height_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_heightv2.png',
        'physical_activity_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_exercisev2.png',
        'education_level_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_educationv2.png',
        'drinking_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_drinkingv2.png',
        'smoking_img_src':'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_smokingv2.png',
        'weed_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_cannabisv2.png',
        'relationship_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_intentionsv2.png',
        'family_plans_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_familyPlansv2.png',
        'star_sign_img_src':'/https:/us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_starSignv2.png',
        'political_leaning_img_src':'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_Politicsv2.png',
        'religion_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_religionv2.png',
        'gender_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_genderv2.png',
    }

    height = physical_activity_frequency = education_level = drinking_frequency = smoking_frequency = weed_smoking_frequency = relationship_type = family_plans = star_sign = political_leaning = religion = gender = None

    """ current_image_container = attribute_images_containers[0].find_element(By.CLASS_NAME, 'pill__image')
    current_image_src = current_image_container.get_attribute('src')
    print(current_image_src)
    print(current_image_container.get_attribute('alt'))
    print(img_src_map['height_img_src'] == current_image_src) """
    
    # Depending on the alt text of the "pill" images, assign the correct value to the correct variable 
    for i in range(num_attributes):
        current_image_container = attribute_images_containers[i].find_element(By.CLASS_NAME, 'pill__image')
        current_image_src = current_image_container.get_attribute('src')

        if current_image_src == img_src_map['height_img_src']:
            height = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['physical_activity_img_src']:
            physical_activity_frequency = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['education_level_img_src']:
            education_level = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['drinking_img_src']:  
            drinking_frequency = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['smoking_img_src']:
            smoking_frequency = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['weed_img_src']:
            weed_smoking_frequency = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['relationship_img_src']:
            relationship_type = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['family_plans_img_src']:
            family_plans = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['star_sign_img_src']:
            star_sign = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['political_leaning_img_src']:
            political_leaning = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['religion_img_src']:
            religion = current_image_container.get_attribute('alt')
        elif current_image_src == img_src_map['gender_img_src']:
            gender = current_image_container.get_attribute('alt')
 
    return(
        height, physical_activity_frequency,
        education_level, drinking_frequency,
        smoking_frequency,weed_smoking_frequency, 
        relationship_type, family_plans,
        star_sign, political_leaning,
        religion, gender
    )
        

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
    top_spotify_artists_list = safe_get_element(By.CLASS_NAME, 'spotify-widget__artist')
    num_artists = len(top_spotify_artists_list)
    
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

    """ pass_button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[2]/div')
    pass_button.click() """
    