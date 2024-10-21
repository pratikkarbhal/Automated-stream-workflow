import subprocess
import sys
import time
import re
from seleniumwire import webdriver  # Import from selenium-wire
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# Check and install webdriver_manager if not already installed
try:
    import webdriver_manager
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'webdriver-manager'])

def fetch_stream_url():
    # URL of the Shemaroo Marathi Bana page
    url = "https://www.shemaroome.com/all-channels/shemaroo-marathibana"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the URL
        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely

        # Check for m3u8 URL in the intercepted requests
        for request in driver.requests:
            if 'cdn.live.shemaroome.com' in request.url and 'playlist.m3u8' in request.url:
                print("Fetched Stream URL:", request.url)
                return request.url

        print("Stream URL not found in the network requests.")
        return None

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()  # Close the browser

if __name__ == "__main__":
    fetch_stream_url()
