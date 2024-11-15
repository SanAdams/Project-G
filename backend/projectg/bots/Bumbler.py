from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from typing import Optional, Dict, Any, List
from projectg.models.Prompt import Prompt
from .BaseScraper import BaseScraper 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Bumbler(BaseScraper):


    def scrape_name_card(self) -> Optional[Dict[str, Any]]:
        """
        Scrapes the first card on bumble: Returns a dictionary of name, age, and profession-- 
        None for any field not found
        """

        def get_name() -> str:
            return self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[1]').text
        
        def get_age() -> int:
            return int(self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[1]/article/div[2]/section/header/h1/span[2]').text.replace(", ", ""))
        
        def get_profession() -> Optional[str]:
            try:
                return self.driver.find_element(By.CLASS_NAME, 'encounters-story-profile__occupation').text
            except NoSuchElementException:
                return None
            
        return {
            'name' : get_name(),
            'age' : get_age(),
            'profession' : get_profession()
        }


    def scrape_bio(self) -> Optional[str]:
        try:
            bio = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/p').text
        except NoSuchElementException:
            return None
        return bio


    def scrape_bio_card(self) -> Optional[Dict[str, Any]]:
        """
        Scrapes the second card on Bumble, returns a dictionary of different attributees found on the card (e.g
        height, relationionship intent, etc.-- 
        None for any field not found
        """
        attribute_list_element = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/ul')
        attribute_images_containers = attribute_list_element.find_elements(By.CLASS_NAME, 'pill__image-box')
       
        attributes = {}

        attributes['bio'] = self.scrape_bio()

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
            attribute = current_image.get_attribute('alt')


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


    # def clean_location_text(self, location: str):
    #     location_type = self.determine_location_type(location)
    #     if location_type == 'home_town':
    #         length = len(location)
    #         location = location[8:length-4]
    #     else:
    #         length = len(location)
    #         location = location[12:length-4]
    #     return location

    @BaseScraper.retry_on_failure
    def scrape_location_card(self) -> Optional[Dict[str, Any]]:
        """
        Scrapes last card on bumble, returns a dictionary of attributes (e.g home town, residential location etc. --)
        None for any field not found
        """
        current_location = self.driver.find_element(By.CLASS_NAME, 'location-widget__town')
        if current_location:
            current_location = current_location.text
        location_widget_element = self.safe_get_element(
            By.CLASS_NAME, 'location-widget__info')

        attributes = {}

        if location_widget_element:
            location_widget_pills = location_widget_element.find_elements(By.CLASS_NAME, 'location-widget__pill')
            if len(location_widget_pills) > 1:
                attributes['residential_location'] = location_widget_pills[0].text
                attributes['home_town'] = location_widget_pills[1].text
            elif len(location_widget_pills) == 1:
                if "Lives in" in location_widget_pills[0].text:
                    attributes['residential_location'] = self.clean_location_text(
                        location_widget_pills[0].text)
                else:
                    attributes['home_town'] = self.clean_location_text(location_widget_pills[0].text)

            top_spotify_artists_list = self.driver.find_elements(
                By.CLASS_NAME, 'spotify-widget__artist')
            num_artists = len(top_spotify_artists_list)
            top_spotify_artists = []
            for i in range(num_artists):
                top_spotify_artists.append(
                    top_spotify_artists_list[i].text.strip())

        return attributes


    def scrape_prompts(self) -> List[Prompt]:
        """
        Scrapes prompts from a profile and returns them as a list of Prompt objects.
        """
        
        prompts = []
        sections = self.driver.find_elements(By.CSS_SELECTOR, 'section.encounters-story-section--question')
        
        for section in sections:
            question = section.find_element(By.CSS_SELECTOR, 'h2.p-2').get_attribute('innerHTML')
            answer = section.find_element(By.CSS_SELECTOR, 'p.encounters-story-about__text').get_attribute('innerHTML')
            prompts.append(Prompt(question=question, answer=answer))
            

        return prompts
        

    def scroll_down(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_DOWN)


    @BaseScraper.refresh_on_failure
    def next_profile(self) -> bool:
        buttons_container = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div')
        buttons_list = buttons_container.find_elements(By.CLASS_NAME, 'encounters-controls__action')
        
        # Handle the case where the backtrack button is not present/interactable
        if len(buttons_list) == 4:
            pass_button = buttons_list[1]
        else:
            pass_button = buttons_list[0]
        pass_button.click()


    def scrape_profile(self):
        print(self.scrape_name_card())
        self.scroll_down()

        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[1]/article/div[1]/div[2]/article/div/section/div/ul'))
        )
        
        print(self.scrape_bio_card())
        self.scroll_down()
        
        print(self.scrape_prompts())
       
        location_visible = self.driver.find_element(By.CLASS_NAME, 'location-widget__town').is_displayed()
        while not location_visible:
            location_visible = self.driver.find_element(By.CLASS_NAME, 'location-widget__town').is_displayed()
            self.scroll_down()

        
        # self.scrape_location_card()

    
