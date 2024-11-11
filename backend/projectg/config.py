from pathlib import Path

class Config:

    PACKAGE_ROOT = Path(__file__).parent

    CHROME_PATHS = {
        'driver': PACKAGE_ROOT / "dependencies" / "chromedriver-win64" / "chromedriver.exe",
        'binary': PACKAGE_ROOT / "dependencies" / "chrome-win64" / "chrome.exe"
    }

    CHROME_OPTIONS = {
        'debugger_address' : 'localhost:9222'
    }