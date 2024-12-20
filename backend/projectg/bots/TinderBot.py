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

        if not index:
            return None
        else:    
            try:
                bio_div_xpath = f"//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')][{index + 1}]"
                bio_xpath = ".//div[contains(@class, 'C($c-ds-text-primary)') and contains(@class, 'Typs(body-1-regular)')]"
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
    # def scrape_going_out(self, index: int):
    #     pass

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

    def scrape_top_spotify_artists(self) -> list[str]:

        try:
            spotify_artists_div_xpath = "//div[text() = 'My top artists']/../.."
            spotify_artists_div = self.driver.find_element(By.XPATH, spotify_artists_div_xpath)
            
            # Reveal hidden artists
            try:
                more_button = spotify_artists_div.find_element(By.XPATH, ".//div[@class = 'Px(16px)']")
                more_button.click()
            except NoSuchElementException:
                pass

            spotify_artists = spotify_artists_div.find_elements(By.XPATH, './/span[@class = "Va(m)"]')

            artists = [element.text or element.get_attribute('textContent') for element in spotify_artists]
            return artists
        except NoSuchElementException:
            return []


    def scrape_prompts(self) -> Optional[list[Prompt]]:
        """
        Returns a list of Prompt objects corresponding to prompts answered on a particular Tinder profile
        """

        try:
            prompt_divs_xpath = "//div[contains (@class, 'C($c-ds-text-primary)') and contains (@class ,'Typs(display-2-strong)')]/../.."
            answer_xpath = ".//div[contains (@class, 'C($c-ds-text-primary)') and contains (@class ,'Typs(display-2-strong)')]"
            question_xpath = ".//div[contains(@class, 'D(f)') and contains(@class, 'Ai(c)') and contains (@class, 'Mb(8px)')]"
            
            prompt_divs = self.driver.find_elements(By.XPATH, prompt_divs_xpath)
            
            prompts: list[Prompt] = []
            for prompt_div in prompt_divs:

                question = prompt_div.find_element(By.XPATH, question_xpath)
                answer = prompt_div.find_element(By.XPATH, answer_xpath)

                prompt = Prompt(question=question.text or question.get_attribute('textContent'), answer=answer.text or answer.get_attribute('textContent'))
                prompts.append(prompt)

            return prompts
        except NoSuchElementException:
            return None


    def scrape_essentials(self) -> dict[str, str]:
        
        try:
            essentials_div_xpath = "//div[text() = 'Essentials']/../.."
            essentials_div = self.driver.find_element(By.XPATH, essentials_div_xpath)
            essential_xpath = (
                ".//div[contains(@class, 'Typs(body-1-regular)') and " 
                "contains(@class, 'C($c-ds-text-primary)') and " 
                "contains(@class, 'Mstart(8px)')]"
            )


            svg_pathfill_d_map = {
                'M2.25' : 'residential_location',
                'M12.301' : 'distance',
                'M16.995' : 'profession',
                'M11.171' : 'education',
                'M16.301' : 'height',
                'M10.077' : 'sexuality',
                'M12.225' : 'pronouns',
                'M22.757' : 'languages'
            }

            # Grab the elements that contain the text of the essential attributes
            essential_text_elements = [
                element for element in essentials_div.find_elements(By.XPATH, essential_xpath)
            ]


            # Process the elements by extracting the text and mapping that text to what it represents
            essentials = {}
            print(len(essential_text_elements))
            for element in essential_text_elements:
                svg = element.find_element(By.XPATH, "./..//*[name()= 'svg']")
                path_fill_d = svg.find_element(By.XPATH, ".//*[name() = 'path']").get_attribute('d')
                essential_text = element.text or element.get_attribute('textContent')

                if 'Verified' in essential_text:
                    essentials['verification_status'] = essential_text
                    continue

                for key in svg_pathfill_d_map.keys():
                    if key in path_fill_d:
                        if svg_pathfill_d_map[key] == 'residential_location':
                            essentials[svg_pathfill_d_map[key]] = essential_text[8:]
                        else:
                            essentials[svg_pathfill_d_map[key]] = essential_text

            
            self.logger.info('Successfully scraped essentials')
            return essentials
        except NoSuchElementException as e:
            self.logger.error(f'Failed to scrape essentials - element not found - {e}')
            pass
        except Exception as e:
            self.logger.error(f'Failed to scrape essentials -- {e}')
            pass


    def scrape_anthem(self) -> dict[str, str]:
        try:
            anthem_div_xpath = "//div[text() = 'My anthem']/../.."
            anthem_div = self.driver.find_element(By.XPATH, anthem_div_xpath)
            anthem_values = anthem_div.find_elements(By.XPATH, './/span[@class = "Va(m)"]')
            
            anthem = { 
                        anthem_values[0].text or anthem_values[0].get_attribute('textContent'): 
                        anthem_values[1].text or anthem_values[1].get_attribute('textContent')
            }
            return anthem
        except NoSuchElementException:
            return {}
    
    
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

        interests_index = div_indexes['Interests']
        print(self.scrape_interests(interests_index))

        print(self.scrape_anthem())

        print(self.scrape_top_spotify_artists())

        print(self.scrape_prompts())

        print(self.scrape_essentials())