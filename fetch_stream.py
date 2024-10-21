import requests

def fetch_stream_url():
    # URL of the Shemaroo Marathi Bana API endpoint
    url = "https://cdn.live.shemaroome.com/marathibana/smil:marathibanaadp.smil/playlist.m3u8"

    # Set headers to mimic a browser request (you may need to adjust these)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.shemaroome.com/all-channels/shemaroo-marathibana',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        # Send a GET request to the XHR URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Debugging: Print the response text
        print("Response text:", response.text)

        # You might need to extract the stream URL from the response depending on its format
        if "playlist.m3u8" in response.text:
            print("Fetched Stream URL:", url)
            return url
        else:
            print("Stream URL not found in the response.")
            return None

    except requests.RequestException as e:
        print("Error fetching the stream URL:", e)
        return None

if __name__ == "__main__":
    fetch_stream_url()
