const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: 'new', // Ensures the correct headless mode is used
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--window-size=1920,1080',
        ],
    });

    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36');

    const m3u8Urls = [];

    // Intercept XHR requests and look for .m3u8 URLs
    await page.setRequestInterception(true);
    page.on('request', (request) => request.continue());

    page.on('response', async (response) => {
        const url = response.url();
        if (url.includes('.m3u8')) {
            m3u8Urls.push(url);
            console.log(`M3U8 URL Found: ${url}`);
        }
    });

    try {
        console.log('Navigating to the page...');
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'networkidle2',
            timeout: 60000,
        });

        console.log('Waiting for video element...');
        await page.waitForSelector('video', { timeout: 20000 });
        await page.click('video'); // Simulate click to start the stream

        console.log('Observing for network activity...');
        await new Promise((resolve) => setTimeout(resolve, 120000)); // Wait 2 minutes

        console.log('M3U8 URLs found:', m3u8Urls.length ? m3u8Urls : 'None found.');
    } catch (error) {
        console.error('Error during execution:', error);
    } finally {
        await browser.close();
    }
})();
