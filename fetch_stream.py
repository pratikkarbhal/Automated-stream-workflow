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

        # Wait for XHR requests to finish and get all network requests
        time.sleep(3)  # Additional wait for XHR requests to complete
        logs = driver.get_log('performance')  # Collect performance logs

        # Find the m3u8 URL in the logs
        for log in logs:
            message = log['message']
            if 'cdn.live.shemaroome.com' in message and 'playlist.m3u8' in message:
                # Use regex to extract the URL from the log message
                match = re.search(r'https://cdn\.live\.shemaroome\.com/marathibana/smil:marathibanaadp\.smil/playlist\.m3u8\?[^"]+', message)
                if match:
                    stream_url = match.group(0)
                    print("Fetched Stream URL:", stream_url)
                    return stream_url

        print("Stream URL not found in the network requests.")
        return None

    finally:
        driver.quit()  # Close the browser

if __name__ == "__main__":
    fetch_stream_url()
