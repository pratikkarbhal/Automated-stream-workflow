const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: false,  // Set to false to see what's happening (can switch to true later)
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36');

    const m3u8Urls = [];

    // Intercept and monitor all network requests
    page.on('response', async (response) => {
        try {
            const url = response.url();
            const type = response.request().resourceType();
            
            console.log(`[${type.toUpperCase()}] Response URL: ${url}`);  // Log all response URLs with type

            // Check for XHR or fetch requests containing .m3u8
            if (type === 'xhr' || type === 'fetch') {
                if (url.includes('.m3u8')) {
                    console.log(`M3U8 URL Found: ${url}`);
                    m3u8Urls.push(url);  // Save found .m3u8 URL
                }
            }
        } catch (error) {
            console.error(`Error processing response: ${error.message}`);
        }
    });

    try {
        console.log('Navigating to the page...');
        
        // Increase timeout to avoid errors during slow loads
        await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
            waitUntil: 'networkidle2',  // Ensure all requests are complete
            timeout: 60000  // 60 seconds timeout
        });

        console.log('Waiting for potential XHR requests...');
        await page.waitForTimeout(10000);  // Allow extra time for network requests

        // Log the collected M3U8 URLs
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
