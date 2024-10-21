const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: true, // Disable headless for troubleshooting
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    );

    const m3u8Urls = [];

    // Capture all network responses
    page.on('response', async (response) => {
        try {
            const url = response.url();
            const type = response.request().resourceType();

            console.log(`[${type.toUpperCase()}] Response URL: ${url}`);

            // Filter for .m3u8 URLs from XHR or fetch requests
            if ((type === 'xhr' || type === 'fetch') && url.includes('.m3u8')) {
                console.log(`M3U8 URL Found: ${url}`);
                m3u8Urls.push(url);
            }
        } catch (error) {
            console.error(`Error processing response: ${error.message}`);
        }
    });

    try {
        console.log('Navigating to the page...');

        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'networkidle2', // Wait for network to settle
            timeout: 120000, // 1-minute timeout
        });

        console.log('Waiting for XHR requests...');
        await new Promise((resolve) => setTimeout(resolve, 60000)); // 10-second wait

        // Print collected M3U8 URLs
        if (m3u8Urls.length > 0) {
            console.log('M3U8 URLs found:', m3u8Urls);
        } else {
            console.log('No M3U8 URLs found.');
        }
    } catch (error) {
        console.error(`Error during navigation: ${error.message}`);
    } finally {
        await browser.close();
    }
})();
