const puppeteer = require('puppeteer-core');

(async () => {
    const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
    const page = await browser.newPage();
    
    // Listen for network requests and responses
    page.on('response', async response => {
        const url = response.url();
        const status = response.status();
        const contentType = response.headers()['content-type'];
        
        // Log all XHR responses
        if (response.request().resourceType() === 'xhr') {
            console.log(`XHR Response: ${url}, Status: ${status}, Content-Type: ${contentType}`);
            const responseBody = await response.text();
            console.log(`Response Body: ${responseBody}`);
        }
    });

    await page.goto('https://www.shemaroome.com/all-channels/shemaroo-marathibana', {
        waitUntil: 'networkidle2', // Wait for the network to be idle
        timeout: 60000 // Increase the timeout to 60 seconds
    });

    console.log('Page loaded.');
    
    await browser.close();
})();
