from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

    def refresh_on_failure(self):
        self.driver.refresh()
        time.sleep(self.wait_for_retry)

    def handle_errors(self, func):
        """
        Decorator for handling common scraping errors
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NoSuchElementException as e:
                return None
            except TimeoutException as e:
                return None
            except Exception as e:
                return None
        return wrapper
    
    def retry_on_failure(self, func):
        """
        Decorator for retrying failed operations
        """
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt + 1 == self.max_retries:
                        raise
                    time.sleep(self.wait_for_retry)
        return wrapper
