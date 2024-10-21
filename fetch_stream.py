from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

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

        # Get the network requests using DevTools protocol (requires additional setup)
        # You can also find the URL directly from the page source
        page_source = driver.page_source

        # Find the stream URL in the page source
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
