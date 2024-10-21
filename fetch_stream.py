from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_stream_url():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless if you don't need a UI
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Enable performance logging
    chrome_options.add_experimental_option('w3c', False)  # Important for logging
    chrome_options.add_experimental_option('prefs', {
        "profile.default_content_setting_values.notifications": 2
    })
    
    # Setting up the logging preferences
    chrome_options.add_experimental_option('loggingPrefs', {
        'performance': 'ALL',  # Enable performance logging
    })
    
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.shemaroome.com/all-channels/shemaroo-marathibana")

    time.sleep(5)  # Wait for the page to load completely

    # Fetch performance logs
    logs = driver.get_log('performance')

    # Process the logs as per your requirement
    for entry in logs:
        print(entry)  # Or your logic to extract the URL

    driver.quit()

if __name__ == "__main__":
    get_stream_url()
