from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def init_driver():
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Path to chromedriver.exe
    # service = Service(chromedriver_path)

    # Initialize WebDriver with Service and ChromeOptions
    # driver = webdriver.Chrome(service, options)

    # return driver

def main(website: str, num_profiles: int):
    driver = init_driver()
    pass

if __name__ == 'main':
    main()