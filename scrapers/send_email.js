const { chromium } = require('playwright');
require('dotenv').config();  // Load environment variables from .env file


(async (propertyUrl, customMessage, delay) => {
    const browser = await chromium.launch({
        headless: false,
        executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' // Specify the path to your Chrome executable
    });
    const page = await browser.newPage();

    try {
        await page.goto(propertyUrl, { timeout: 60000 });

        
        // Function to generate a random wait time between 5 to 8 seconds
        function getRandomWaitTime() {
            return (Math.floor(Math.random() * 4) + 5) * 1000; // Random wait time between 5000 and 8000 ms
        }

        // Scroll down the page
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        

        // Fill in the form fields with simulated human typing
        
        await page.fill('#name', 'Alber Mara');        
        
        
        await page.fill('#email', 'Info@cs-properties.com');

        
        await page.fill("#telephone", '02045521255')

        
        await page.fill('#postcode', 'IG7 6JD');

        
        await page.selectOption('#moving-situation', 'moving-within-3-mo');

        
        await page.selectOption('#situation', 'professional');

        
        await page.check('input[name="enquiry"][value="viewing"]');
        
        // Ensure the comments textarea is visible and type into it
        try {
           
            await page.waitForSelector('#message', { timeout: 10000 });
            await page.fill('#message', customMessage);
        } catch (e) {
            console.log(`Could not find the comments textarea: ${e}`);
        }
        
        
        
        // await page.click('label[for="create-alert-contact-no"]');
        await page.click('label.border.border-dove.block.w-full.font-heading.font-semibold.bg-white.mb-0.text-sm.py-3.px-7.rounded-md.cursor-pointer.text-left');

        
        // Click on the submit button
        await page.click('button.otm-Button.whitespace-nowrap.py-2.leading-normal.h-auto.shadow-none.font-heading.font-semibold.text-center.justify-center.inline-flex.items-center.px-8.rounded-md.border-2.disabled\\:bg-dove.disabled\\:text-white.disabled\\:border-transparent.hover\\:disabled\\:opacity-100.transition.duration-200.ease-in-out.border-burnt-coral.bg-burnt-coral.text-white.hover\\:opacity-80.w-full.min-h-\\[50px\\].text-md');
        await sleep(5000)
        

        console.log('Email sent successfully');
        process.exit(0); // Indicate successful completion
    } catch (e) {
        console.log(`Error during form submission: ${e}`);
        process.exit(1); // Indicate failure
    } finally {
        await browser.close();
    }
})(process.argv[2], process.argv[3], process.argv[4]);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

