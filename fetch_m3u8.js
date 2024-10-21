const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: true, // Run in headless mode
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage();

    // Intercept requests
    await page.setRequestInterception(true);
    page.on('request', (request) => {
        request.continue();
    });

    // Log only XHR responses
    page.on('response', async (response) => {
        const url = response.url();
        const request = response.request();
        
        // Check if the response is an XHR request
        if (request.resourceType() === 'xhr') {
            console.log(`XHR Response URL: ${url}`); // Log the XHR response URLs

            // Check for .m3u8 URLs
            if (url.endsWith('.m3u8')) {
                console.log(`M3U8 URL found: ${url}`);
            }
        }
    });

    try {
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'networkidle2', // Wait until network is idle
            timeout: 60000
        });

        console.log('Page loaded. Check the logs for XHR responses.');

    } catch (error) {
        console.error('Error during navigation:', error);
    } finally {
        await browser.close();
    }
})();
