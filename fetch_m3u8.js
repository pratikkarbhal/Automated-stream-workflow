const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to false to see the browser in action (for troubleshooting)
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    );

    // Intercept requests and responses
    const m3u8Urls = [];

    page.on('response', async (response) => {
        try {
            const url = response.url();
            const type = response.request().resourceType();

            console.log(`Response: ${response.status()} ${type} - ${url}`);

            if (type === 'xhr' || type === 'fetch') {
                const text = await response.text();
                if (url.includes('.m3u8') || text.includes('.m3u8')) {
                    m3u8Urls.push(url);
                    console.log(`M3U8 URL Found: ${url}`);
                }
            }
        } catch (err) {
            console.error(`Error processing response: ${err}`);
        }
    });

    try {
        // Navigate to the target URL
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'networkidle2', // Wait until network requests settle
            timeout: 60000,
        });

        // Evaluate JavaScript to extract XHR logs directly from the browser context
        const xhrUrls = await page.evaluate(() => {
            const urls = [];
            const open = window.XMLHttpRequest.prototype.open;
            window.XMLHttpRequest.prototype.open = function (method, url) {
                urls.push(url);
                console.log(`XHR Request: ${method} ${url}`);
                open.apply(this, arguments);
            };
            return urls;
        });

        console.log('XHR URLs captured:', xhrUrls);

        // Wait to ensure all requests are captured
        await page.waitForTimeout(10000);

        console.log('M3U8 URLs found:', m3u8Urls.length > 0 ? m3u8Urls : 'None found');
    } catch (error) {
        console.error('Error during navigation:', error);
    } finally {
        await browser.close();
    }
})();
