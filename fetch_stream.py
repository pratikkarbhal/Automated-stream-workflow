import subprocess
import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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

        # Interact with the page if necessary (e.g., click on buttons)
        # For example, you may need to click on a play button to initiate the stream:
        # play_button = driver.find_element_by_xpath("//button[@id='play-button-id']")  # Use the correct ID
        # play_button.click()
        # time.sleep(5)  # Wait for the stream to start

        # Now look for the m3u8 URL in the page source or logs
        page_source = driver.page_source
        
        # Search for the m3u8 URL in the page source
        match = re.search(r'https://cdn\.live\.shemaroome\.com/marathibana/smil:marathibanaadp\.smil/playlist\.m3u8\?[^"]+', page_source)
        
        if match:
            stream_url = match.group(0)
            print("Fetched Stream URL:", stream_url)
            return stream_url
        else:
            print("Stream URL not found in the page source.")
            return None

    finally:
        driver.quit()  # Close the browser

if __name__ == "__main__":
    fetch_stream_url()
