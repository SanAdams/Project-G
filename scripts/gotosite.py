from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")
CHROMEDRIVER_PATH = '../BE/dependencies/chromedriver-win64/chromedriver.exe'

# Path to chromedriver.exe
service = Service(CHROMEDRIVER_PATH)

# Initialize WebDriver with Service and Options
driver = webdriver.Chrome(options, service)

sites = ["Bumble", "Tinder"]
reformatted_sites = ', '.join(sites) 
print(f"What website? Type the name of one of these (case-insensitive): {reformatted_sites}")
desired_site = input()
desired_site = desired_site.lower()

if desired_site == "bumble":
    driver.get("https://bumble.com/app")
elif desired_site == "tinder":
    driver.get("https://tinder.com/app/recs")

