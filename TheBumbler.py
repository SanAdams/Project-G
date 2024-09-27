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

def safe_get_element(by:By, value:str):
    try:
        element = driver.find_element(by, value)
        return element
    except NoSuchElementException:
        return ""
    
def scrape_name_card():
    name = safe_get_element_text(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[1]')
    age = safe_get_element_text(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[2]').replace(", " , "")
    profession = safe_get_element_text(By.CLASS_NAME, 'encounters-story-profile__occupation')
    return (name, age, profession)

def scrape_bio_card():
    attribute_list_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/ul')
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
        'star_sign_img_src':'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_starSignv2.png',
        'political_leaning_img_src':'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_Politicsv2.png',
        'religion_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_religionv2.png',
        'gender_img_src': 'https://us1.ecdn2.bumbcdn.com/i/big/assets/bumble_lifestyle_badges/normal/web/standard/sz___size__/ic_badge_profileChips_dating_genderv2.png',
    }

    height = physical_activity_frequency = education_level = drinking_frequency = smoking_frequency = weed_smoking_frequency = relationship_type = family_plans = star_sign = political_leaning = religion = gender = ""
    bio = safe_get_element_text(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/p')
    
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
        bio, height, physical_activity_frequency,
        education_level, drinking_frequency,
        smoking_frequency,weed_smoking_frequency, 
        relationship_type, family_plans,
        star_sign, political_leaning,
        religion, gender
    )

def determine_location_type(location: str):
    if "Lives in" in location:
        return "residential"
    else:
        return "home_town"

def clean_location_text(location: str):
    location_type = determine_location_type(location)
    if location_type == 'home_town':
        length = len(location)
        location = location[12:length-4]
    else:
        length = len(location)
        location = location[8:length-4]
    return location

def scrape_location_card():
    print("Scraping location")
    current_location = safe_get_element(By.CLASS_NAME, 'location-widget__town')
    if current_location:
        current_location = current_location.text
    
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

    try: 
        top_spotify_artists_list = driver.find_elements(By.CLASS_NAME, 'spotify-widget__artist')
        num_artists = len(top_spotify_artists_list)
        top_spotify_artists = []
        for i in range (num_artists):
            top_spotify_artists.append(top_spotify_artists_list[i].text.strip())
    except NoSuchElementException:
            top_spotify_artists = []
    
    return (current_location, home_town, residential_location, top_spotify_artists)

def scroll_down(multiplier: int):
    scrollDown = f'-{multiplier * 100}%'
    albumContainer = safe_get_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
    driver.execute_script(f"arguments[0].style.transform = 'translateY({scrollDown})';", albumContainer)

if __name__ == '__main__':
    NUM_PROFILES = 2

    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Path to chromedriver.exe
    service = Service("D:/FUNSIES/Project G/chromedriver-win64/chromedriver.exe")

    # Initialize WebDriver with Service and ChromeOptions
    driver = webdriver.Chrome(service=service, options=options)

    # Make new user to store data
    user = DatingAppUser.DatingAppUser()

    start = time.time()
    sleep = 3
    for profile in range(NUM_PROFILES):
        start = time.time()
        current_card = 0
        print(scrape_name_card())
        current_card += 1
        scroll_down(current_card)
        time.sleep(sleep)
        print(scrape_bio_card())
        current_card += 1
        scroll_down(current_card)
        time.sleep(sleep)

        album_containter = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
        num_flavor_cards = len(album_containter.find_elements(By.CLASS_NAME, 'encounters-album__story')) - 3
        for i in range(1, num_flavor_cards):
            current_card += 1
            scroll_down(current_card)

        #TO-DO: fix flavor_text scraping code
        """profile_cards_container = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
        flavor_text_containers = profile_cards_container.find_elements(By.CLASS_NAME, 'encounters-story-section__content')
        num_flavor_text_containers = len(flavor_text_containers)

        for i in range(1, num_flavor_text_containers):
            flavor_text = flavor_text_containers[i].text    
            print(flavor_text)
            scroll_down(current_card)
            current_card += 1
            time.sleep(1) """
    
        scrape_location_card()
        buttons_container = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div')
        buttons_list = buttons_container.find_elements(By.CLASS_NAME, 'encounters-controls__action')
        pass_button = buttons_list[1]
        pass_button.click()
        time.sleep(sleep)
        time_scraped = time.time()
    end = time.time()
    print(f"It took {(end-start)} seconds to scrape {NUM_PROFILES} profiles")
    