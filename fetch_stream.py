import asyncio
from pyppeteer import launch

async def fetch_m3u8_url():
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()

    # Navigate to the Shemaroo Marathibana live stream page
    await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', waitUntil='networkidle0')

    # Wait for the page to load completely
    await asyncio.sleep(5)  # Adjust if necessary

    # Get network requests
    client = await page.target.createCDPSession()
    await client.send('Network.enable')

    m3u8_url = None

    # Listen for network requests
    def log_request(request):
        nonlocal m3u8_url
        if 'playlist.m3u8' in request['url']:
            m3u8_url = request['url']
            print(f"Found M3U8 URL: {m3u8_url}")

    client.on('Network.requestWillBeSent', log_request)

    # Keep the browser open for a while to capture requests
    await asyncio.sleep(30)  # Allow time to capture all requests

    await browser.close()

    if m3u8_url:
        with open('m3u8_url.txt', 'w') as f:
            f.write(m3u8_url)
        print(f"M3U8 URL saved: {m3u8_url}")
    else:
        print("M3U8 URL not found.")

asyncio.get_event_loop().run_until_complete(fetch_m3u8_url())
