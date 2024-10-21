const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: true, // Run in headless mode
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--window-size=1920,1080',
            '--disable-dev-shm-usage' // Overcome limited resource problems
        ]
    });

    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36');

    const m3u8Urls = [];
    await page.setRequestInterception(true);

    page.on('request', (request) => {
        request.continue();
    });

    page.on('response', async (response) => {
        const url = response.url();
        if (url.includes('.m3u8')) {
            m3u8Urls.push(url);
            console.log(`M3U8 URL found: ${url}`);
        }
    });

    try {
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });

        await page.waitForSelector('your-selector-here', { timeout: 30000 }); // Replace with a relevant selector

        // Optionally simulate user actions here

        await new Promise(resolve => setTimeout(resolve, 10000));

        console.log('M3U8 URLs found:', m3u8Urls.length > 0 ? m3u8Urls : 'No M3U8 URLs found.');
    } catch (error) {
        console.error('Error during navigation:', error);
    } finally {
        await browser.close();
    }
})();
