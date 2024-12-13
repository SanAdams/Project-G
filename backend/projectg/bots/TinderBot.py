from collections import defaultdict
from typing import Optional, DefaultDict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .BaseScraper import BaseScraper
from selenium.webdriver.common.keys import Keys
from projectg.models.Prompt import Prompt
class TinderBot(BaseScraper):

    def get_div_indexes(self) -> DefaultDict[str, Optional[int]]:
        """Returns a mapping of section titles to their corresponding div indices."""
        div_indexes = defaultdict(lambda: None)
        
        content_divs = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, 
                "//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)')]"
            ))
        )
        
        for i, div in enumerate(content_divs):
            try:
                # Get all text content of the heading element
                heading_element = div.find_element(By.XPATH, 
                    ".//div[contains(@class, 'Mstart(8px)') and contains(@class, 'Mb(0)') and contains(@class, 'Typs(body-2-strong)')]"
                )
                
                # Try different methods to get the text
                heading = heading_element.get_attribute('textContent') or heading_element.text
                heading = heading.strip()
                
                if heading:
                    div_indexes[heading] = i
                else:
                    # Debug output for empty headings
                    print(f"Empty heading at index {i}:")
                    print(f"innerHTML: {heading_element.get_attribute('innerHTML')}")
                    print(f"outerHTML: {heading_element.get_attribute('outerHTML')}")
                    
            except Exception as e:
                print(f"Error processing div {i}: {e}")
                continue

        return div_indexes

    def open_profile(self) -> None:
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_UP)


    def scrape_name(self) -> str:
        names = self.driver.find_elements(By.XPATH, '//span[@class="Typs(display-1-strong)"]')
        return names[1].text


    def scrape_age(self) -> int:
        ages = self.driver.find_elements(
            By.XPATH, '//span[@class="Typs(display-2-regular) As(b)"]//span')
        return int(ages[1].text)
    

    def next_profile(self) -> None:
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_LEFT)


    def scrape_relationship_intent(self) ->Optional[str]:
        relationship_span_xpath = "//span[contains(@class, 'Typs(display-3-strong)') and contains(@class, 'C($c-ds-text-primary)') and contains(@class, 'Mstart(4px)')]"

        try:
            span = self.driver.find_element(By.XPATH, relationship_span_xpath)
            return span.text
        except NoSuchElementException:
            self.logger.error('Relationship intent not found')
            return None

    def scrape_bio(self, index: int) -> Optional[str]:
        bio_div_xpath = f"//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')][{index + 1}]"
        bio_xpath = ".//div[contains(@class, 'C($c-ds-text-primary)') and contains(@class, 'Typs(body-1-regular)')]"

        if not index:
            return None
        else:    
            try:
                bio = self.driver.find_element(By.XPATH, bio_div_xpath).find_element(By.XPATH, bio_xpath).text
                return bio
            except NoSuchElementException:
                self.logger.error('Bio not found')
                return None

        
    def scrape_relationship_type(self) -> Optional[str]:
        relationship_types = [
            'Open to exploring',
            'Ethical non-monogamy',
            'Monogamy',
            'Open relationship',
            'Polyamory'
        ]

        for relationship_type in relationship_types:
            try:
                self.driver.find_element(By.XPATH, f"//div[text() = '{relationship_type}']")
                return relationship_type
            except NoSuchElementException:
                pass
        
        return None

    def scrape_basics(self, index: Optional[int]) -> dict[str, str]:
        """
        Scrape the basics section of a Tinder profile.

        Returns a dict[str, str] of attribute titles to attribute values
        """

        if not index:
            return {}
        else:
            
            basic_attributes = {}
            basics_div_xpath = f"//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')][{index + 1}]"
            basics_div = self.driver.find_element(By.XPATH, basics_div_xpath)

            basics_values_xpath = (
                ".//div[contains(@class, 'Typs(body-1-regular)') and "
                "contains(@class, 'C($c-ds-text-primary)') and "
                "contains(@class, 'Mstart(8px)')]"
            )

            # If there are more attributes hidden from view, reveal them
            try:
                more_button = basics_div.find_element(By.XPATH, "//div[contains(@class, 'Px(16px)')]")
                more_button.click()
            except NoSuchElementException:
                pass

            basics_values = [
                element.text or element.get_attribute('textContent')
                for element in basics_div.find_elements(By.XPATH, basics_values_xpath)
            ]
            
            basics_titles_xpath = ".//h3[contains(@class, 'C($c-ds-text-secondary)') and contains(@class, 'Typs(subheading-2)')]"
            basics_titles = [
                element.text or element.get_attribute('textContent')
                for element in basics_div.find_elements(By.XPATH, basics_titles_xpath)
            ]
            
            basic_attributes = dict(zip(basics_titles, basics_values))

        return basic_attributes

    # Might implement this later, seems a bit much
    def scrape_going_out(self, index: int):
        pass

    def scrape_lifestyle(self, index: Optional[int]) -> dict[str, str]:
        if not index:
            return {}
        else:
            
            lifestyle_attributes = {}
            lifestyle_div_xpath = f"//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')][{index + 1}]"
            lifestyle_div = self.driver.find_element(By.XPATH, lifestyle_div_xpath)

            lifestyle_values_xpath = (
                ".//div[contains(@class, 'Typs(body-1-regular)') and "
                "contains(@class, 'C($c-ds-text-primary)') and "
                "contains(@class, 'Mstart(8px)')]"
            )

            # If there are more attributes hidden from view, reveal them
            try:
                more_button = lifestyle_div.find_element(By.XPATH, "//div[contains(@class, 'Px(16px)')]")
                more_button.click()
            except NoSuchElementException:
                pass

            lifestyle_values = [
                element.text or element.get_attribute('textContent')
                for element in lifestyle_div.find_elements(By.XPATH, lifestyle_values_xpath)
            ]
            
            basics_titles_xpath = ".//h3[contains(@class, 'C($c-ds-text-secondary)') and contains(@class, 'Typs(subheading-2)')]"
            lifestyle_titles = [
                element.text or element.get_attribute('textContent')
                for element in lifestyle_div.find_elements(By.XPATH, basics_titles_xpath)
            ]
            
            lifestyle_attributes = dict(zip(lifestyle_titles, lifestyle_values))

        return lifestyle_attributes


    def scrape_interests(self, index: int) -> list[str]:
        if not index:
            return []
        else:
            interests = {}
            interests_div_xpath = f"//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')][{index + 1}]"
            interests_div = self.driver.find_element(By.XPATH, interests_div_xpath)

            interests_values_xpath = (
                ".//span[contains(@class, 'Typs(body-1-regular)') and "
                "contains(@class, 'C($c-ds-text-passions-shared)')]"
            )

            interests = [element.text or element.get_attribute('textContent') for element in interests_div.find_elements(By.XPATH, interests_values_xpath)]

        return interests

    def scrape_top_spotify_artists(self):
        pass


    def scrape_essentials(self):

        pass


    def scrape_languages(self):
        pass

    def scrape_anthem(self):
        pass
    
    def scrape_profile(self):

        print(self.scrape_name())
        print(self.scrape_age())
        self.open_profile()

        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')]")))
        div_indexes = self.get_div_indexes()
        
        print(self.scrape_relationship_intent())
        print(self.scrape_relationship_type())
        
        bio_index = div_indexes['About me']
        print(self.scrape_bio(bio_index))

        basics_index = div_indexes['Basics']
        print(self.scrape_basics(basics_index))
        
        lifestlye_index = div_indexes['Lifestyle']
        print(self.scrape_lifestyle(lifestlye_index))

        # essentials_index = div_indexes['Essentials']
        # print(self.scrape_essentials(essentials_index))

        interests_index = div_indexes['Interests']
        print(self.scrape_interests(interests_index))
        # print(div_indexes)
        
        # print(self.scrape_lifestyle())