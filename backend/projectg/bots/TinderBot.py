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

    def get_div_indexes(self) -> dict[str, Optional[int]]:
        """Returns a mapping of section titles to their corresponding div indices."""
        div_indexes = {}
        
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


    def scrape_relationship_intent(self) -> str:
        relationship_span_xpath = "//span[contains(@class, 'Typs(display-3-strong)') and contains(@class, 'C($c-ds-text-primary)') and contains(@class, 'Mstart(4px)')]"

        span = self.driver.find_element(By.XPATH, relationship_span_xpath)
        return span.text

    def scrape_bio(self, index: int) -> Optional[str]:
        print(f"bio index is {index}")
        bio_div_xpath = f"//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')][{index + 1}]"
        bio_xpath = ".//div[contains(@class, 'C($c-ds-text-primary)') and contains(@class, 'Typs(body-1-regular)')]"

        bio = self.driver.find_element(By.XPATH, bio_div_xpath).find_element(By.XPATH, bio_xpath).text
        
        return bio

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

    def scrape_basics(self, index: Optional[int]) -> DefaultDict[str, str]:
        """
        Scrape the basics section of a Tinder profile. Empty string for any field not found
        """

        if not index:
            return {}
        else:
            #TODO: Rewrite this entire function. It doesn't work
            basic_attributes = defaultdict(lambda: "")
            basics_div_xpath = f"//div[contains(@class, 'P(24px)') and contains(@class, 'W(100%)') and contains(@class, 'Bgc($c-ds-background-primary)') and contains(@class, 'Bdrs(12px)')][{index + 1}]"

            self.driver.find_element(By.XPATH, basics_div_xpath)

        return basic_attributes


    def scrape_lifestyle(self):
        lifestyle_attributes = defaultdict(lambda: "")
        try:
            # Wait for the "lifestyle" section to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//h2[text()="Lifestyle"]'))
            )

            # Locate the lifestyle section
            lifestyle_section = self.driver.find_element(
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

                    attribute_value = self.driver.execute_script(
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


    def scrape_interests(self):
        pass


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
        
        # print(div_indexes)
        
        # print(self.scrape_lifestyle())