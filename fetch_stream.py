from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Function to fetch the M3U8 URL
def fetch_m3u8_url():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Enable performance logging
    chrome_options.add_experimental_option("w3c", False)
    chrome_options.add_experimental_option("loggingPrefs", {"performance": "ALL"})
    
    driver_service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    driver.get("https://www.shemaroome.com/all-channels/shemaroo-marathibana")  # Updated URL
    time.sleep(5)  # Wait for the page to load

    # Get logs and extract the M3U8 URL
    logs = driver.get_log('performance')
    for log in logs:
        # Process log entries
        print(log)  # You can implement your logic to extract the M3U8 URL here

    driver.quit()

if __name__ == "__main__":
    fetch_m3u8_url()
