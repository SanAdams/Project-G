from typing import Literal
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from .config import Config
from .bots.Bumbler import Bumbler
from .bots.TinderBot import TinderBot

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

ScraperType = Literal['bumble', 'tinder']

def init_driver():
    try:
        options = Options()
        options.add_experimental_option("debuggerAddress", Config.CHROME_OPTIONS['debugger_address'])

        service = Service(str(Config.CHROME_PATHS['driver']))
        driver = webdriver.Chrome(options, service)

        logger.info("Successfully initialized Chrome webdriver")
    except Exception as e:
        logger.error(f"Failed to initialize webdriver: {str(e)}")
        raise

    return driver

def run_scraper(website: ScraperType, count: int):
    """
    Driver function for running scrapers

    Arguments:
        website: Which website is being scraped?
        count: How many profiles should be scraped?
    """

    # Create a mapping to the class we want, based on input
    scrapers = {
        'tinder' : TinderBot,
        'bumble' : Bumbler
    }
    
    # Get the class
    scraper_class = scrapers.get(website)
    
    driver = init_driver()
    
    # Create an instance of the class and pass in driver
    scraper = scraper_class(driver)
    
    for _ in range(count):
        scraper.scrape_profile()
        # scraper.next_profile()

    logger.info(f"Successfully scraped {count} profiles from {website}")

    driver.quit()
    logger.info("Web driver closed")

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m projectg.main <website> <num_profiles>")
        print("Example: python -m projectg.main bumble 100")
        sys.exit(1)
    

    website = sys.argv[1].lower()
    try:
        num_profiles = int(sys.argv[2])
    except ValueError:
        print("Error: profile_count must be a number")
        sys.exit(1)

    run_scraper(website, num_profiles)
        
    
if __name__ == "__main__":
    main()
