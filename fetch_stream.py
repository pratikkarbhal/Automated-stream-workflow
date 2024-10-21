import requests
import re

def fetch_stream_url():
    # URL of the Shemaroo Marathi Bana page
    url = "https://www.shemaroome.com/all-channels/shemaroo-marathibana"

    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.shemaroome.com/all-channels/'
    }

    try:
        # Send a GET request to the page with headers
        response = requests.get(url, headers=headers)
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
