const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36');

    // Listen for network requests and responses
    const m3u8Urls = [];
    await page.setRequestInterception(true);

    page.on('request', (request) => {
        console.log(`Request: ${request.method()} ${request.url()}`); // Log request method and URL
        request.continue();
    });

    page.on('response', async (response) => {
        const url = response.url();
        const status = response.status();
        console.log(`Response: ${status} ${url}`); // Log response status and URL

        // Check if the response is from an XHR request
        const type = response.request().resourceType();
        if (type === 'xhr' && url.endsWith('.m3u8')) {
            m3u8Urls.push(url);
            console.log(`M3U8 URL found: ${url}`); // Log found M3U8 URL
        }
    });

    try {
        // Navigate to the Shemaroo Marathi Bani page with increased timeout
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'domcontentloaded', // Change to 'domcontentloaded'
            timeout: 60000 // Increase timeout to 60 seconds
        });

        // Wait for some time to let all requests complete
        await new Promise(resolve => setTimeout(resolve, 5000)); // Use setTimeout as a workaround

        // Output the collected M3U8 URLs
        console.log('M3U8 URLs found:', m3u8Urls.length > 0 ? m3u8Urls : 'No M3U8 URLs found.');

    } catch (error) {
        console.error('Error during navigation:', error);
    } finally {
        await browser.close();
    }
})();
