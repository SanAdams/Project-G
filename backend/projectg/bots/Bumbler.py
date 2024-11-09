from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from projectg.bots.BaseScraper import BaseScraper 
 
class Bumbler(BaseScraper):

    @BaseScraper.retry_on_failure
    @BaseScraper.handle_errors
    def scrape_name_card(self) -> Optional[Dict[str, Any]]:
        name = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[1]')
        age = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[2]').replace(", ", "")
        profession = self.find_element(By.CLASS_NAME, 'encounters-story-profile__occupation')
        age = int(age)
        return (name, age, profession)
    
    @BaseScraper.retry_on_failure
    @BaseScraper.handle_errors
    def scrape_bio(self):
        bio = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/p')
        return bio
   
    @BaseScraper.retry_on_failure
    @BaseScraper.handle_errors
    def scrape_bio_card(self) -> Optional[Dict[str, Any]]:


        attribute_list_element = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/ul')
        attribute_images_containers = attribute_list_element.find_elements(By.CLASS_NAME, 'pill__image-box')
       
        attributes = {}

        attribute_map = {
            'heightv2.png': 'height',
            'exercisev2.png': 'physical_activity_frequency', 
            'educationv2.png': 'education_level',
            'drinkingv2.png': 'drinking_frequency',
            'smokingv2.png': 'smoking_frequency',
            'cannabisv2.png': 'weed_smoking_frequency',
            'intentionsv2.png': 'relationship_goals',
            'familyPlansv2.png': 'family_plans',
            'starSignv2.png': 'star_sign',
            'Politicsv2.png': 'political_leaning',
            'religionv2.png': 'religion',
            'genderv2.png': 'gender'
        }

        # Assign the attribute the right value
        for current_image_container in attribute_images_containers:
            current_image = current_image_container.find_element(By.TAG_NAME, 'img')
            current_image_src = current_image.get_attribute('src')
            attribute = current_image_container.get_attribute('alt')


            for identifier, attribute_name in attribute_map.items():
                if identifier in current_image_src:
                    attributes[attribute_name] = attribute
                    break


        return attributes


    def determine_location_type(location: str):
        if "Lives in" in location:
            return "residential"
        else:
            return "home_town"


    def clean_location_text(self, location: str):
        location_type = self.determine_location_type(location)
        if location_type == 'home_town':
            length = len(location)
            location = location[8:length-4]
        else:
            length = len(location)
            location = location[12:length-4]
        return location


    def scrape_location_card(self):

        current_location = self.safe_get_element(By.CLASS_NAME, 'location-widget__town')
        if current_location:
            current_location = current_location.text
        location_widget_element = self.safe_get_element(
            By.CLASS_NAME, 'location-widget__info')
        home_town = ""
        residential_location = ""

        if location_widget_element:
            location_widget_pills = location_widget_element.find_elements(
                By.CLASS_NAME, 'location-widget__pill')
            if len(location_widget_pills) > 1:
                residential_location = self.clean_location_text(
                    location_widget_pills[0].text)
                home_town = self.clean_location_text(location_widget_pills[1].text)
            elif len(location_widget_pills) == 1:
                if "Lives in" in location_widget_pills[0].text:
                    residential_location = self.clean_location_text(
                        location_widget_pills[0].text)
                else:
                    home_town = self.clean_location_text(location_widget_pills[0].text)

        try:
            top_spotify_artists_list = self.driver.find_elements(
                By.CLASS_NAME, 'spotify-widget__artist')
            num_artists = len(top_spotify_artists_list)
            top_spotify_artists = []
            for i in range(num_artists):
                top_spotify_artists.append(
                    top_spotify_artists_list[i].text.strip())
        except NoSuchElementException:
            top_spotify_artists = []

        return (current_location, home_town, residential_location, top_spotify_artists)

    def scrape_flavor_cards(self, bio_present):
        album_containter = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
        flavor_cards = self.filter_ptags(album_containter.find_elements(By.TAG_NAME, 'p'), 'encounters-story-about__text')
        num_flavor_cards = len(flavor_cards)
        flavor_texts = []
        
        start = 1 if bio_present else 0

        for i in range(start, num_flavor_cards):
            flavor_texts.append(flavor_cards[i].text.strip())
            self.scroll_down()
            time.sleep(1)

        return flavor_texts


    def filter_ptags(ptags, class_name):
        return [p for p in ptags if class_name == p.get_attribute('class')]


    def scroll_down(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_DOWN)
        return

    def next_profile(self) -> bool:
        buttons_container = self.self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div')
        buttons_list = buttons_container.find_elements(By.CLASS_NAME, 'encounters-controls__action')
        
        # Handle the case where the backtrack button is not interactable
        if len(buttons_list) == 4:
            pass_button = buttons_list[1]
        else:
            pass_button = buttons_list[0]
        pass_button.click()

    def scrape_profile(self):
        self.scrape_name_card()
        self.scrape_bio_card()
        self.scrape_flavor_cards()
        self.scrape_location_card()



# if __name__ == '__main__':

#     scraper = Bumbler(driver)

#     # Make new user to store data
#     user = DatingAppUser()
#     NUM_PROFILES = 1

#     start = time.time()
#     sleep = 1

#     bumbleUsers = []


#     for profile in range(NUM_PROFILES):
#         user = DatingAppUser()
#         user.dating_app = "Bumble"
#         card = 0

#         time.sleep(sleep)
#         user.name, user.age, user.profession = scrape_name_card()
#         scroll_down()

#         # Retry if the scrape failed
#         if not user.name or not user.age:
#             print("Scrape failed, refreshing")
#             driver.refresh()
#             continue

#         time.sleep(sleep)
#         bio_card_data = []
#         bio_card_data = scrape_bio_card()
        
#         bio_attributes = [
#                         "bio", "height", "physical_activity_frequency", "education_level",
#                         "drinking_frequency", "smoking_frequency", "gender", "weed_smoking_frequency",
#                         "relationship_goals", "family_plans", "star_sign", "political_leaning", "religion"
#                      ]

#         for i, attr in enumerate(bio_attributes):
#             setattr(user, attr, bio_card_data[i])
     
#         scroll_down()

#         album_containter = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]')
#         ptags = album_containter.find_elements(By.TAG_NAME, 'p')
#         current_location = album_containter.find_element(By.CLASS_NAME, 'location-widget__town')

#         # If there are only cards with 2 pictures, scroll past them
#         if len(ptags) == 1:
#             while not current_location.is_displayed():
#                 scroll_down()
#                 time.sleep(sleep)

#         time.sleep(sleep)

#         user.flavor_text = scrape_flavor_cards(user.bio)

#         # If there is at least one flavor card with text
#         # and some number of cards with 2 pictures, scrape then scroll past them
#         while not current_location.is_displayed():
         
#             scroll_down()
#             time.sleep(sleep)

#         time.sleep(sleep)
#         user.current_location, user.home_town, user.residential_location, user.top_spotify_artists = scrape_location_card()

#         user.time_scraped = int(time.time())
#         bumbleUsers.append(user)
#         user_data_json = json.dumps(user.__dict__)
#         print(user_data_json)
#         # next_profile()

#     end = time.time()
#     print(f"It took {(end-start)} seconds to scrape {NUM_PROFILES} profiles")

#     for bumbler in bumbleUsers:
#         for attr, value in vars(bumbler).items():
#             print(f"{attr}: {value}")

    
    
