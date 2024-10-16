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
        return None
    
def scrape_name_card():
    name = safe_get_element_text(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[1]')
    age = safe_get_element_text(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[2]').replace(", " , "")
    profession = safe_get_element_text(By.CLASS_NAME, 'encounters-story-profile__occupation')
    age = int(age)
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

    height = physical_activity_frequency = education_level = drinking_frequency = ""
    smoking_frequency = weed_smoking_frequency = relationship_goals = family_plans = ""
    star_sign = political_leaning = religion = gender = ""
    bio = safe_get_element_text(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/p')
    
    # Assign the attribute the right value 
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
            relationship_goals = current_image_container.get_attribute('alt')
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
        smoking_frequency, gender, 
        weed_smoking_frequency, relationship_goals,
        family_plans, star_sign,
        political_leaning, religion
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
        location = location[8:length-4]
    else:
        length = len(location)
        location = location[12:length-4]
    return location

def scrape_location_card():
  
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

def scrape_flavor_cards(card: int, bio_present: bool):
    album_containter = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
    flavor_cards = filter_ptags(album_containter.find_elements(By.TAG_NAME, 'p'), 'encounters-story-about__text')
    num_flavor_cards = len(flavor_cards)
    flavor_texts = []
    
    if bio_present:
        start = 1
    else:
        start = 0

    for i in range(start, num_flavor_cards):
        flavor_texts.append(flavor_cards[i].text.strip())
        card += 1
        scroll_to(card)
        time.sleep(1)

    return flavor_texts


def filter_ptags(ptags, class_name):
    return [p for p in ptags if class_name == p.get_attribute('class')]
    

def scroll_to(multiplier: int):
    scrollDown = f'-{multiplier * 100}%'
    albumContainer = safe_get_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
    driver.execute_script(f"arguments[0].style.transform = 'translateY({scrollDown})';", albumContainer)

def next_profile():
    buttons_container = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div')
    buttons_list = buttons_container.find_elements(By.CLASS_NAME, 'encounters-controls__action')
    if len(buttons_list) == 4:
        pass_button = buttons_list[1]
    else:
        pass_button = buttons_list[0]
    pass_button.click()

if __name__ == '__main__':
    NUM_PROFILES = 1

    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Path to chromedriver.exe
    service = Service("D:/FUNSIES/Project G/chromedriver-win64/chromedriver.exe")

    # Initialize WebDriver with Service and ChromeOptions
    driver = webdriver.Chrome(service=service, options=options)

    # Make new user to store data
    user = DatingAppUser.DatingAppUser()

    start = time.time()
    sleep = 1

    for profile in range(NUM_PROFILES):
        bumbleUsers = []
        user = DatingAppUser.DatingAppUser()
        user.dating_app = "Bumble"
        card = 0

        time.sleep(sleep)
        user.name, user.age, user.profession = scrape_name_card()
        card += 1
        scroll_to(card)

        time.sleep(sleep)
        bio_card_data = []
        bio_card_data = scrape_bio_card()
        user.bio, user.height, user.physical_activity_frequency = bio_card_data[0], bio_card_data[1], bio_card_data[2]
        user.education_level, user.drinking_frequency, user.smoking_frequency = bio_card_data[3], bio_card_data[4], bio_card_data[5]
        user.gender, user.weed_smoking_frequency, user.relationship_goals = bio_card_data[6], bio_card_data[7], bio_card_data[8]
        user.family_plans, user.star_sign, user.political_leaning, user.religion = bio_card_data[9],bio_card_data[10],bio_card_data[11],bio_card_data[12]
        
        if user.bio:
            has_bio = True
        else:
            has_bio = False
        card += 1
        scroll_to(card)

        album_containter = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
        ptags = album_containter.find_elements(By.TAG_NAME, 'p')
        current_location = album_containter.find_element(By.CLASS_NAME, 'location-widget__town')

        # If there are only cards with 2 pictures, scroll past them
        if len(ptags) == 1:
            while not current_location.is_displayed():
                card += 1
                scroll_to(card)
                time.sleep(sleep)

        time.sleep(sleep)

        user.flavor_text = scrape_flavor_cards(card, has_bio)

        # If there is at least one flavor card with text
        # and some number of cards with 2 pictures, scrape then scroll past them
        while not current_location.is_displayed():
            card += 1
            scroll_to(card)
            time.sleep(sleep)

        time.sleep(sleep)
        user.current_location, user.home_town, user.residential_location, user.top_spotify_artists = scrape_location_card()

        user.time_scraped = int(time.time())
        bumbleUsers.append(user)
        # next_profile()
   
    end = time.time()
    print(f"It took {(end-start)} seconds to scrape {NUM_PROFILES} profiles")
    
    for bumbler in bumbleUsers:
        for attr, value in vars(bumbler).items():
            print(f"{attr}: {value}")