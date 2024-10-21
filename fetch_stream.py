import requests
import re

def fetch_stream_url():
    # URL of the Shemaroo Marathi Bana page
    url = "https://www.shemaroome.com/all-channels/shemaroo-marathibana"

    try:
        # Send a GET request to the page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Use regex to find the stream URL in the response text
        match = re.search(r'https://cdn\.live\.shemaroome\.com/marathibana/smil:marathibanaadp\.smil/playlist\.m3u8\?[^"]+', response.text)
        
        if match:
            stream_url = match.group(0)
            print("Fetched Stream URL:", stream_url)
            return stream_url
        else:
            print("Stream URL not found.")
            return None

    except requests.RequestException as e:
        print("Error fetching the stream URL:", e)
        return None

if __name__ == "__main__":
    fetch_stream_url()
