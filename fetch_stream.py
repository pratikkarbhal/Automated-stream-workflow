from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def fetch_m3u8_url():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Start the Chrome WebDriver
    service = Service('/usr/bin/chromedriver')  # Adjust path if necessary
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the target URL
        driver.get("https://www.shemaroome.com/all-channels/shemaroo-marathibana")
        time.sleep(5)  # Wait for the page to load completely

        # Fetch network requests
        logs = driver.get_log('performance')
        for log in logs:
            log_message = log['message']
            if 'cdn.live.shemaroome.com' in log_message and 'playlist.m3u8' in log_message:
                # Extract the M3U8 URL from the log
                # Note: You will need to parse the log_message to extract the URL
                print("Found M3U8 URL:", log_message)

    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_m3u8_url()
