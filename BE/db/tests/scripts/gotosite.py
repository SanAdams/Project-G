from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")

# Path to chromedriver.exe
service = Service("../dependencies/chromedriver-win64/chromedriver.exe")

# Initialize WebDriver with Service and Options
driver = webdriver.Chrome(options, service)

sites = ["Bumble", "Tinder"]
reformatted_sites = ', '.join(sites) 
print(f"What website? Type the name of one of these (case-insensitive): {reformatted_sites}")
desired_site = input()

if desired_site.lower() == "bumble":
    driver.get("https://bumble.com/app")
elif desired_site.lower() == "tinder":
    driver.get("https://tinder.com/app/recs")

