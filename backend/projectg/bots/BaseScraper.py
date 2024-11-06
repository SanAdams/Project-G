from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time

class BaseScraper(ABC):
    """
    Base class for all scrapers to inherit from. Provides functionality that all
    scrapers must implement
    """
    
    def __init__(self, driver: webdriver, max_retries: int = 3, wait_for_retry: float = 1.0):
        self.driver = driver
        self.max_retries = max_retries
        self.wait_for_retry = wait_for_retry

    @abstractmethod
    def next_profile():
        pass

    @abstractmethod
    def scrape_profile():
        pass

    def safe_get_element_text(self, by: By, value: str) -> str:
        try:
            element = self.driver.find_element(by, value)
            return element.text.strip()
        except NoSuchElementException:
            return ""

    def safe_get_element(self, by: By, value: str) -> WebElement:
        try:
            element = self.driver.find_element(by, value)
            return element
        except NoSuchElementException:
            return None

    def refresh_on_failure(self):
        self.driver.refresh()
        time.sleep(self.wait_for_retry)

    def retry_on_failure():
        
        pass

