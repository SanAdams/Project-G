from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import logging

class BaseScraper(ABC):
    """
    Base class for all scrapers to inherit from. Provides functionality that all
    scrapers must implement
    """
    
    def __init__(self, driver: webdriver, max_retries: int = 3, wait_for_retry: float = 1.0):
        self.driver = driver
        self.max_retries = max_retries
        self.wait_for_retry = wait_for_retry
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def next_profile():
        pass

    @abstractmethod
    def scrape_profile():
        pass

    @staticmethod
    def refresh_on_failure(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.driver.refresh()
                time.sleep(self.wait_for_retry)
                return func(self, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def retry_on_failure(func):
        """
        Decorator for retrying failed operations
        """
        def wrapper(self, *args, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    if attempt + 1 == self.max_retries:
                        self.logger.error(f"Failed after {self.max_retries} attempts: {e}")
                        raise
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(self.wait_for_retry)
        return wrapper
