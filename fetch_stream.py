from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import re

def get_stream_url():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless if you don't need a UI
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Enable performance logging
    chrome_options.add_experimental_option('w3c', False)  # Important for logging
    chrome_options.add_experimental_option('prefs', {
        "profile.default_content_setting_values.notifications": 2  # Disable notifications
    })
    
    # Setting up the logging preferences
    chrome_options.add_experimental_option('loggingPrefs', {
        'performance': 'ALL',  # Enable performance logging
    })
    
    # Set the path to the ChromeDriver
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to the target URL
    driver.get("https://www.shemaroome.com/all-channels/shemaroo-marathibana")

    # Wait for the page to load completely
    time.sleep(5)  

    # Fetch performance logs
    logs = driver.get_log('performance')

    m3u8_url = None
    # Fixed regex pattern for the .m3u8 URL
    url_pattern = r"https:\/\/cdn\.live\.shemaroome\.com\/marathibana\/[^?]+\.m3u8\?[^ ]+"  

    for entry in logs:
        log_entry = json.loads(entry['message'])['message']
        if 'params' in log_entry:
            if 'request' in log_entry['params']:
                request_url = log_entry['params']['request']['url']
                # Check if the request URL matches the pattern
                match = re.search(url_pattern, request_url)
                if match:
                    m3u8_url = match.group(0)
                    break  # Exit loop once we find the .m3u8 URL

    if m3u8_url:
        print("Found m3u8 URL:", m3u8_url)  # Output the found URL
    else:
        print("No m3u8 URL found.")

    # Close the browser
    driver.quit()
    return m3u8_url  # Return the URL for further processing if needed

if __name__ == "__main__":
    get_stream_url()
