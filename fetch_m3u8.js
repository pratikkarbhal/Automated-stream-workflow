const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to false to visually observe what’s happening.
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36');

    const m3u8Urls = [];

    // Intercept and log all XHR requests and responses
    await page.setRequestInterception(true);

    page.on('request', (request) => {
        request.continue();
    });

    page.on('response', async (response) => {
        const url = response.url();
        const type = response.request().resourceType();
        if (type === 'xhr' && url.includes('.m3u8')) {
            m3u8Urls.push(url);
            console.log(`M3U8 URL Found: ${url}`);
        }
    });

    try {
        // Navigate to the target URL with extended timeout
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'networkidle2', // Ensure page is fully loaded
            timeout: 60000, // Increase timeout
        });

        // Wait and simulate interaction with the player
        console.log('Simulating interaction...');
        await page.waitForSelector('video', { timeout: 20000 }); // Adjust if different selector is needed
        await page.click('video'); // Simulate clicking the video to start playback

        // Wait to capture delayed media requests (2 minutes as you mentioned)
        console.log('Waiting for 2 minutes to capture streams...');
        await new Promise(resolve => setTimeout(resolve, 120000)); // Wait 2 minutes

        // Output collected M3U8 URLs
        console.log('M3U8 URLs:', m3u8Urls.length > 0 ? m3u8Urls : 'No M3U8 URLs found.');

    } catch (error) {
        console.error('Error during execution:', error);
    } finally {
        await browser.close();
    }
})();
