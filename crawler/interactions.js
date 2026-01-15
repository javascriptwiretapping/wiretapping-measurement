const {
    format
} = require('date-fns');
const {
    storeData
} = require('./helpers');
const { getConfig } = require('./configs');

async function fillInputFields(page, entry) {

    const processedInputs = new Set();

    const siteId = entry[0];
    const siteUrl = entry[1];

    // Find all input fields
    await new Promise(resolve => setTimeout(resolve, 1000));
    const inputs = await page.$$('input');

    // Fill each input field based on its type
    for (let index = 0; index < inputs.length; index++) {
        const input = inputs[index];
        const inputType = await input.evaluate(input => input.type);
        const nameAttribute = await input.evaluate(el => el.name ? el.name.toLowerCase() : '');
        const placeholderAttribute = await input.evaluate(el => el.placeholder ? el.placeholder.toLowerCase() : '');
        const idAttribute = await input.evaluate(el => el.id);
        const classAttribute = await input.evaluate(el => el.className);

        const inputIdentifier = `${idAttribute}_${classAttribute}_${nameAttribute}_${inputType}_${index}`;

        // Skip if the input field has already been processed
        if (processedInputs.has(inputIdentifier)) {
            continue;
        }

        // process checkbox and radio inputs
        try {
            // Skip hidden inputs
            if (['hidden', 'submit', 'button', 'checkbox', 'radio', 'file'].includes(inputType)) {
                processedInputs.add(inputIdentifier);
                continue;
            } else {
                // Click the input field if it's not hidden
                try {
                    // Focus the input field before interacting
                    await input.focus();

                    // Optionally, click at the center of the input field for better precision
                    const inputBox = await input.boundingBox();
                    if (inputBox) {
                        await page.mouse.click(
                            inputBox.x + inputBox.width / 2,
                            inputBox.y + inputBox.height / 2
                        );
                    }

                } catch (error) {
                }
                finally {
                    processedInputs.add(inputIdentifier);
                }
            }
        } catch (error) { }
        finally {
            processedInputs.add(inputIdentifier);
        }

        // Determine the value to enter based on inputType
        let inputValue;
        if (nameAttribute.includes('mail') || placeholderAttribute.includes('mail')) { 
            inputValue = 'veli' + siteId.replace('_','.') + '@xtrustedmed.de';
        } else {
            switch (inputType) {
                case 'email':
                    inputValue = 'veli' + siteId.replace('_','.') + '@xtrustedmed.de';
                    break;
                case 'number':
                    inputValue = '4922122200';
                    break;
                case 'tel':
                    inputValue = '4922122200';
                    break;
                case 'password':
                    inputValue = 'SaltySeedsTea9!';
                    break;
                case 'text':
                    inputValue = 'hi_my_honey_text';
                    break;
                case 'url':
                    inputValue = 'curious-cat.com';
                    break;
                default:
                    inputValue = 'hi_my_honey_field';
                    break;
            }
        }

        // Fill the input field with the determined value, skip if it's already filled
        const currentValue = await input.evaluate(el => {
            return (
                el.value?.trim() || // The current value in the input field
                el.defaultValue?.trim() || // The default value that might be set on the element
                el.getAttribute('value')?.trim() || // The 'value' attribute, if directly set in HTML
                ''
            );
        });
        const interactionStartTime = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
        const sensitiveStrings = getConfig('sensitiveStrings');

        const containsSensitiveString = sensitiveStrings.some(sensitive => currentValue.includes(sensitive));
        // console.log('processedInputs: ', processedInputs);
        // console.log('Sensitive strings: ', sensitiveStrings);
        // console.log('Current value: ', currentValue);
        // console.log('Contains sensitive string: ', containsSensitiveString);
        // console.log('Input value: ', inputValue);
        // console.log('Input type: ', inputType);
        // console.log('Input identifier: ', inputIdentifier);
        // // print input id
        // console.log('ID: ', idAttribute);

        if (!currentValue.includes(inputValue) && !containsSensitiveString) {
            await input.type(inputValue, {
                delay: 20
            });
            const interactionEndTime = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
            await storeData("interactions", [siteId, siteUrl, interactionStartTime, interactionEndTime, "fill_form_" + inputType]);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }

        // dont focus anymore
        await input.evaluate(el => el.blur());
        processedInputs.add(inputIdentifier);

        // Wait for a short duration after typing (adjust as needed)
        //await page.waitForTimeout(500);
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

async function realisticMouseMove(page, startX, startY, endX, endY) {
    await page.mouse.move(startX, startY);
    const totalDuration = 3000;
    const steps = 10; // Number of steps to break the movement into
    let prevX = startX,
        prevY = startY;

    const maxDelayPerStep = totalDuration / steps;

    for (let i = 1; i <= steps; i++) {
        // Calculate a point along a simple Bezier curve
        const t = i / steps;
        const x = startX + (endX - startX) * t + (Math.random() - 0.5) * 10 * (1 - t);
        const y = startY + (endY - startY) * t + (Math.random() - 0.5) * 10 * (1 - t);

        const delay = Math.random() * (maxDelayPerStep - 10) + 10;

        await page.mouse.move(x, y, {
            steps: 1
        });

        await new Promise(resolve => setTimeout(resolve, delay));

        prevX = x;
        prevY = y;
    }
    await page.mouse.move(endX, endY);
}

async function interactWithPage(page, entry) {
    const siteId = entry[0];
    const siteUrl = entry[1];

    const mouseMoveStartTime = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');

    // interaction 1
    try {
        await realisticMouseMove(page, 0, 0, 200, 300); // Move from (0, 0) to (200, 200)
    } catch (error) {
        //console.log(error)
        console.log("error during interaction 1: " + error.message + ": " + entry[1])
    }
    const mouseMoveEndTime = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
    await storeData("interactions", [siteId, siteUrl, mouseMoveStartTime, mouseMoveEndTime, "mouse_movement"]);

    const keyboardStartTime = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
    // interaction 2
    try {
        for (let i = 0; i < 3; i++) {
            await page.keyboard.press('PageUp');
            await page.keyboard.press('PageDown');
            await page.keyboard.press('PageDown');
        }

        for (let i = 0; i < 15; i++) {
            await page.keyboard.press('Tab');
        }
        for (let i = 0; i < 3; i++) {
            await page.keyboard.press('ArrowUp');
            await page.keyboard.press('ArrowDown');
        }

    } catch (error) {
        console.log("error during interaction 2: " + error.message + ": " + entry[1])
        //console.log(error)

    } finally {
        const keyboardEndTime = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
        await storeData("interactions", [siteId, siteUrl, keyboardStartTime, keyboardEndTime, "pageup_pagedown_tabs"]);
    }

    // interaction 3
    try {
        await fillInputFields(page, entry);
    } catch (error) {
        console.log("error during interaction 3: " + error.message + ": " + entry[1])
        //console.log(error)
    }

    // interaction 4
    const textAreaStart = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
    try {
        // Find all textarea fields
        const textAreas = await page.$$('textarea');
        const processedTextAreas = new Set(); // To track processed textareas

        for (let index = 0; index < textAreas.length; index++) {
            const textArea = textAreas[index];
            const idAttribute = await textArea.evaluate(el => el.id);
            const classAttribute = await textArea.evaluate(el => el.className);
            const nameAttribute = await textArea.evaluate(el => el.name.toLowerCase());

            const textAreaIdentifier = `${idAttribute}_${classAttribute}_${nameAttribute}_textarea_${index}`;

            if (processedTextAreas.has(textAreaIdentifier)) {
                continue;
            }

            const currentValue = await textArea.evaluate(el => el.value);
            if (!currentValue.startsWith('ifisnur')) {
                try {
                    await textArea.click();
                }
                catch (error) { }
                await textArea.evaluate(el => el.value = '');
                await textArea.type('hi_my_honey_text_area', { delay: 20 });
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
            processedTextAreas.add(textAreaIdentifier);
        }
    } catch (error) {
        console.error("Error during interaction 4: " + error.message + ": " + entry[1]);
    } finally {
        const textAreaEnd = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
        await storeData("interactions", [siteId, siteUrl, textAreaStart, textAreaEnd, "fill_textarea"]);
    }


    // interaction 5
    try {
        await page.evaluate(() => document.activeElement.blur());
    } catch (error) { }

    const bodyStart = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
    try {
        for (const key of 'ifisnur_track_home') {
            await page.keyboard.press(key);
        }

        // Additional wait after interactions
        //await page.waitForTimeout(1500);
        await new Promise(resolve => setTimeout(resolve, 1000));

    } catch (error) {
        console.log("error during interaction 5: " + error.message + ": " + entry[1])
        //console.log(error)
    } finally {
        const bodyEnd = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
        await storeData("interactions", [siteId, siteUrl, bodyStart, bodyEnd, "type_in_body"]);
    }
}

module.exports = {
    interactWithPage
};