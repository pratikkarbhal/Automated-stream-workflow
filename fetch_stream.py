from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import time

def get_stream_url():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Start the WebDriver
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the target URL
    driver.get("https://www.shemaroome.com/all-channels/shemaroo-marathibana")

    # Wait for the page to load (adjust as necessary)
    time.sleep(10)  # Increase this time if needed

    # Extract the page source
    page_source = driver.page_source

    # Use regex to find the .m3u8 URL
    url_pattern = r"https:\/\/cdn\.live\.shemaroome\.com\/marathibana\/[^\"']+\.m3u8\?[^\"']+"  # Regex pattern for the .m3u8 URL
    match = re.search(url_pattern, page_source)

    if match:
        stream_url = match.group(0)  # Extract the matched URL
        print("Stream URL:", stream_url)
    else:
        print("No .m3u8 URL found.")

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    get_stream_url()
