from collections import defaultdict
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .BaseScraper import BaseScraper
from selenium.webdriver.common.keys import Keys
class TinderBot(BaseScraper):
    def open_profile(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_UP)


    def scrape_name(self):
        names = self.driver.find_elements(By.XPATH, '//span[@class="Typs(display-1-strong)"]')
        return names[1].text


    def scrape_age(self):
        ages = self.driver.find_elements(
            By.XPATH, '//span[@class="Typs(display-2-regular) As(b)"]//span')
        return int(ages[1].text)
    

    def next_profile(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_LEFT)


    def scrape_relationship_intent(self):
        self.driver.find_element(By.XPATH, '//div[text() = "Looking for"]')
        

    def scrape_relationship_type(self) -> Optional[str]:
        try:
            relationship_type = self.driver.find_element(By.CSS_SELECTOR, 
            r'.Bdrs\(30px\).M\(4px\).Px\(12px\).Typs\(body-1-regular\).Py\(4px\).Bgc\(\$c-ds-background-passions-sparks-inactive\)')
            return relationship_type.text
        except NoSuchElementException:
            self.logger.error('Relationship type element not properly found')
            return None
        

    def scrape_basics(self):
        basic_attributes = defaultdict(lambda: "")

        try:
            # Wait for the "Basics" section to be present
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//h2[text()="Basics"]'))
            )

            # Locate the Basics section
            basics_section = self.driver.find_element(
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

                    attribute_value = self.driver.execute_script(
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


    def scrape_interests():
        pass


    def scrape_top_spotify_artists():
        pass


    def scrape_essentials():
        pass


    def scrape_languages():
        pass

    def scrape_anthem():
        pass
    
    def scrape_profile(self):
        print(self.scrape_name())
        print(self.scrape_age())
        self.open_profile()
        print(self.scrape_relationship_type())
        # print(self.scrape_basics())
        # print(self.scrape_lifestyle())
        # self.next_profile()