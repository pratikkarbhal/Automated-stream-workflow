// fetch_m3u8.js

const puppeteer = require('puppeteer');

(async () => {
    // Initialize browser and page
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Define the URL of the page you want to scrape
    const targetUrl = 'YOUR_TARGET_URL_HERE'; // Replace with the actual URL
    await page.goto(targetUrl, { waitUntil: 'networkidle2' });

    // Extract the M3U8 URL
    const m3u8Url = await page.evaluate(() => {
        // Logic to find the M3U8 URL
        let m3u8Links = [];
        const mediaElements = document.querySelectorAll('video, audio');

        mediaElements.forEach((media) => {
            const src = media.src || media.currentSrc;
            if (src && src.endsWith('.m3u8')) {
                m3u8Links.push(src);
            }
        });

        return m3u8Links.length > 0 ? m3u8Links : null;
    });

    // Log the extracted M3U8 URL(s)
    if (m3u8Url) {
        console.log('M3U8 URL(s) found:', m3u8Url);
    } else {
        console.log('No M3U8 URLs found.');
    }

    // Close browser
    await browser.close();
})();
