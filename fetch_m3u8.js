const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to false to see the browser actions
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36');

    // Listen for network requests and responses
    const m3u8Urls = [];
    await page.setRequestInterception(true);

    page.on('request', (request) => {
        request.continue();
    });

    page.on('response', async (response) => {
        const url = response.url();

        // Check if the response URL contains .m3u8
        if (url.includes('.m3u8')) {
            m3u8Urls.push(url);
            console.log(`M3U8 URL found: ${url}`);
        }
    });

    try {
        // Navigate to the Shemaroo Marathi Bani page
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'domcontentloaded', // Load the DOM content first
            timeout: 60000
        });

        // Wait for the page to load completely
        await page.waitForSelector('your-selector-here', { timeout: 30000 }); // Replace with a relevant selector

        // Simulate user interactions (click buttons, etc.)
        // Example: Click on a button to load streams
        // await page.click('button-selector-here'); // Replace with the actual button selector

        // Wait for additional time to let all requests complete
        await new Promise(resolve => setTimeout(resolve, 10000));

        // Output the collected M3U8 URLs
        console.log('M3U8 URLs found:', m3u8Urls.length > 0 ? m3u8Urls : 'No M3U8 URLs found.');

    } catch (error) {
        console.error('Error during navigation:', error);
    } finally {
        await browser.close();
    }
})();
