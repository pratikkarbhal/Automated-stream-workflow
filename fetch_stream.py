import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Stream page URL
STREAM_PAGE_URL = "https://www.shemaroome.com/all-channels/shemaroo-marathibana"

def get_stream_url():
    # Configure Selenium to run headless in GitHub Actions
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set up Chrome driver
    driver = webdriver.Chrome(options=options)

    try:
        # Open the website
        driver.get(STREAM_PAGE_URL)
        time.sleep(10)  # Wait for the page to load fully

        # Get network logs and search for m3u8 URLs
        logs = driver.get_log('performance')
        for log in logs:
            if ".m3u8" in log['message']:
                start_index = log['message'].find('https')
                end_index = log['message'].find('.m3u8') + 5
                stream_url = log['message'][start_index:end_index]
                print(f"Fetched Stream URL: {stream_url}")
                return stream_url

    finally:
        driver.quit()

if __name__ == "__main__":
    url = get_stream_url()
    if url:
        print(f"Stream URL: {url}")
    else:
        print("Failed to retrieve the stream URL.")
