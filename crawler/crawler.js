const puppeteer = require('puppeteer');
const fs = require('fs');
const csv = require('csv-parser');
const { format } = require('date-fns');
const sqlite3 = require('sqlite3');
const Promise = require('bluebird').Promise;
const crypto = require('crypto');
const LZString = require('lz-string');
const zlib = require('zlib');
const lzwCompress = require('lzwcompress');
const base32 = require('hi-base32');
const bs58 = require('bs58');
const { x86, x64 } = require('murmurhash3js-revisited');
const {
  md4,
  createSHA3,
  whirlpool } = require('hash-wasm');

const tldjs = require('tldjs');
const { storeData, getDb, parseStackTrace, getDistinctThirdParties } = require('./helpers');
const { overrideJSFunctionsAndPropertiesStr } = require('./overrides');
const util = require('util');
const { exec } = require('child_process');
const execPromise = util.promisify(exec);
const { interactWithPage } = require('./interactions');

const {
  getConfig
} = require('./configs');

const Queue = require('bee-queue');

const queueInstances = {};

const path = require('path');


async function prepareQueues() {
  for (let i = 0; i < getConfig('redis_workers'); i++) {
    const wiretappingQueue = new Queue('wiretapping_queue_' + i, {
      redis: {
        host: getConfig('redis_ip'),
        port: getConfig('redis_port')
      }
    });
    // add to the queueInstances
    queueInstances[i] = wiretappingQueue;
  }
}

async function setupDatabase(dbname) {


  const urlListPath = getConfig('url_list');
  const chunkId = path.basename(urlListPath);
  const dbFile = path.join('measurement_data', `${chunkId}.db`);
  const dbFile_redis = path.join('measurement_data', `${chunkId}_redis.db`);

  db_list = [dbFile, dbFile_redis];
  for (const dbFile of db_list) {

    console.log('Opening SQLite DB at:', dbFile);
    const db = new sqlite3.Database(dbFile);

    db.serialize(() => {
      db.run(`CREATE TABLE IF NOT EXISTS requests (
      site_id integer, 
      site TEXT, 
      url TEXT, 
      method TEXT,   
      request_time TEXT, 
      payload TEXT, 
      resourceType TEXT,  
      after_interaction TEXT, 
      current_url TEXT, 
      current_etld TEXT, 
      target_etld TEXT, 
      third_party INTEGER,
      data_leak INTEGER DEFAULT 0 ,
      request_call_stack TEXT
    )`);
      db.run(`CREATE TABLE IF NOT EXISTS responses (
      site_id integer, 
      site TEXT, 
      url TEXT, 
      response_code INTEGER,  
      response_time TEXT, 
      current_url TEXT, 
      current_etld TEXT, 
      target_etld TEXT, 
      third_party INTEGER
    )`);

      db.run(`CREATE TABLE IF NOT EXISTS event_listeners (
      site_id integer, 
      site TEXT, 
      event_type TEXT, 
      init_id text,
      init_invoke TEXT, 
      event_time TEXT, 
      event TEXT, 
      function TEXT, 
      useCapture TEXT, 
      args text, 
      stack text,
      stack_json TEXT,
      third_parties TEXT
    )`);
      db.run(`CREATE TABLE IF NOT EXISTS removed_event_listeners (
      site_id integer, 
      site TEXT, 
      event_type TEXT, 
      init_invoke TEXT, 
      init_id text,
      event_time TEXT, 
      event TEXT, 
      function TEXT, 
      useCapture TEXT, 
      init_stack text,
      stack text,
      stack_json TEXT,
      third_parties TEXT
    )`);
      db.run(`CREATE TABLE IF NOT EXISTS cookies (
      site_id integer, 
      site TEXT, 
      name TEXT, 
      value TEXT, 
      domain TEXT, 
      path TEXT, 
      expires TEXT, 
      size INTEGER, 
      httpOnly INTEGER, 
      secure INTEGER, 
      session INTEGER
  )`);

      db.run(`CREATE TABLE IF NOT EXISTS callstacks (
    site_id integer,
    site TEXT,
    function TEXT,
    init_id text,
    init_invoke TEXT,
    event_type TEXT,
    stack TEXT,
    init_stack TEXT,
    stack_json TEXT,
    timestamp TEXT,
    value TEXT,
    is_set INTEGER DEFAULT 0,
    third_parties TEXT
  )`);

      db.run(`CREATE TABLE IF NOT EXISTS interactions ( 
    site_id integer, 
    site_url TEXT, 
    start_time TEXT, 
    end_time TEXT, 
    interaction_type TEXT
  ); )`);

    });
    db.close();
  }
}

function delay(time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time)
  });
}


async function getCrawledURLs() {
  const db = await getDb();
  const query = `SELECT DISTINCT site_id FROM requests`; // Fetch distinct URLs instead of site_id
  const rows = await db.all(query); // Use .all() to get multiple rows
  return rows.map(row => row.site_id); // Return an array of URLs
}


function readUrlsFromCsv(filePath = getConfig('url_list')) {
  return new Promise((resolve, reject) => {
    const urls = [];
    fs.createReadStream(filePath)
      .pipe(csv({
        headers: ['site', 'rank', 'subpage_id', 'url'],
        skipLines: 1 // Skip the header line if present
      }))
      .on('data', (row) => {
        // Extract 'subpage_id' and 'url' directly
        const id = row['subpage_id'].trim();
        const url = row['url'].trim();

        // Push the 'id' and 'url' into the array
        urls.push([id, url]);
      })
      .on('end', () => resolve(urls))
      .on('error', reject);
  });
}

async function generateVariations(str) {
  const inputBuffer = Buffer.from(str);
  const sha3_224 = await createSHA3(224);
  const sha3_256 = await createSHA3(256);
  const sha3_384 = await createSHA3(384);
  const sha3_512 = await createSHA3(512);

  return [
    // Original
    str,
    // Base64-Encoding
    inputBuffer.toString('base64'),
    // URL-Encoding
    encodeURIComponent(str),
    // LZ-String Compression
    LZString.compressToEncodedURIComponent(str),
    // LZW Compression
    JSON.stringify(lzwCompress.pack(str)),

    // Hashes
    crypto.createHash('md5').update(str).digest('hex'),
    crypto.createHash('sha1').update(str).digest('hex'),
    crypto.createHash('sha224').update(str).digest('hex'),
    crypto.createHash('sha256').update(str).digest('hex'),
    crypto.createHash('sha384').update(str).digest('hex'),
    crypto.createHash('sha512').update(str).digest('hex'),
    crypto.createHash('ripemd160').update(str).digest('hex'),      // RIPEMD160

    await md4(str),

    sha3_224.update(str).digest('hex'),
    sha3_256.update(str).digest('hex'),
    sha3_384.update(str).digest('hex'),
    sha3_512.update(str).digest('hex'),
    await whirlpool(str),


    // MurmurHash3
    x86.hash32(str),
    x64.hash128(str),

    // Base Encodings
    inputBuffer.toString('hex'),               // Base16
    base32.encode(str),                        // Base32
    bs58.encode(Buffer.from(str)),

    // Compress to Base64
    zlib.deflateSync(str).toString('base64'),
    zlib.deflateRawSync(str).toString('base64'),
    zlib.gzipSync(str).toString('base64'),
    zlib.brotliCompressSync(inputBuffer).toString('base64'),

    // Compress to HEX
    zlib.deflateSync(str).toString('hex'),
    zlib.gzipSync(str).toString('hex')
  ];
}

// this functions checks if the payload or the target URL contains any of the sensitive strings (data leak)
async function checkSensitiveData(payload, targetUrl, sensitiveStrings, siteId) {
  let data_leak = 0;

  payload = payload || '';
  targetUrl = targetUrl || '';

  for (const str of sensitiveStrings) {

    const strWithSiteId = str.replace('siteID', siteId.replace('_', '.'));
    const variations = await generateVariations(strWithSiteId);
    if (variations.some(variation => payload.includes(variation)) || variations.some(variation => targetUrl.includes(variation))) {
      data_leak = 1;
      break;
    }
  }

  return data_leak;
}

async function handleRequest(request, entry, page) {
  const [siteId, siteUrl, interactionFlag] = entry;
  const currentPageUrl = await page.url(); // Get current page URL in real-time
  const targetUrl = request.url();
  const requestInit = JSON.stringify(request.initiator());


  const currentEtld = tldjs.getDomain(currentPageUrl);
  const targetEtld = tldjs.getDomain(targetUrl);
  const thirdParty = currentEtld !== targetEtld ? 1 : 0; // 1 for true, 0 for false
  // const siteId = entry[0];
  // const siteUrl = entry[1];
  let payload = null;

  try {
    const postData = request.postData();
    if (postData) {
      payload = postData //Buffer.from(postData).toString('base64');
    }
  } catch (e) {
    console.error(e);
  }

  const resourceType = request.resourceType();
  // Define the list of sensitive strings to check for
  const sensitiveStrings = getConfig('sensitiveStrings');
  let data_leak = await checkSensitiveData(payload, targetUrl, sensitiveStrings, siteId);


  storeData("requests", [
    siteId,
    siteUrl,
    targetUrl,
    request.method(),
    format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS'),
    payload,
    resourceType,
    interactionFlag,
    currentPageUrl,
    currentEtld,
    targetEtld,
    thirdParty,
    data_leak,
    requestInit
  ]);

}

async function handleResponse(response, entry, page) {
  const [siteId, siteUrl] = entry;
  const currentPageUrl = await page.url(); // Get current page URL in real-time
  const targetUrl = response.url();
  const currentEtld = tldjs.getDomain(currentPageUrl);
  const targetEtld = tldjs.getDomain(targetUrl);
  const thirdParty = currentEtld !== targetEtld ? 1 : 0; // 1 for true, 0 for false

  storeData("responses", [
    siteId,
    siteUrl,
    targetUrl,
    response.status(),
    format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS'),
    currentPageUrl,
    currentEtld,
    targetEtld,
    thirdParty
  ]);
}



async function launchWithRetries(attempts = 5) {
  let lastErr;
  for (let i = 1; i <= attempts; i++) {
    try {

      const browser = await puppeteer.launch({
        headless: false, // Opting into the new headless mode
        args: ['--start-maximized', '--disable-gpu'],
        protocolTimeout: getConfig("timeout_site"),
      });

      const page = await browser.newPage();
      await page.setViewport({ width: 1920, height: 1080 });
      return { browser, page };

    } catch (err) {
      lastErr = err;
      console.warn(`⚠️  Attempt ${i} failed: ${err.message}`);
      // clean up before retrying
      try { if (browser && browser.close) await browser.close(); } catch { }
      if (i < attempts) {
        await new Promise(r => setTimeout(r, 1000));
      }
    }
  }
  throw new Error(`All ${attempts} launch attempts failed.\nLast error: ${lastErr}`);
}


async function startCrawler(urls) {


  // maxID = await getMaxSiteId();

  try {

    for (const entry of urls) {
      printCurrentState()


      const siteURL = entry[1];
      const siteID = entry[0];

      // 
      if (siteID.split('_')[1] > getConfig('max_subpage')) {
        continue;
      }

      // if (maxID >= siteURL) {
      //   console.log(`Skipping ${siteID} as it already has records.`);
      //   continue; // Skip this URL as it already has records
      // }

      if (getConfig('dont_use_list_sites')) {
        entry[0] = -1
        entry[1] = getConfig('static_site_url');
      }

      console.log(`Processing site ID ${siteID} with URL: ${siteURL}`)


      // Launch Puppeteer with the extension loaded
      // const browser = await puppeteer.launch({
      //   headless: false, // Extensions only work in head-full mode
      //   args: [
      //     // `--disable-extensions-except=${extensionPath}`,
      //     // `--load-extension=${extensionPath}`,
      //     "--start-maximized"
      //   ],
      //   headless: true, 
      //   protocolTimeout: 60000,
      // });


      try {
        const { browser, page } = await launchWithRetries();

        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36');

        const client = await page.target().createCDPSession();

        await client.send('Network.enable');
        await client.send('Debugger.enable');

        // make a global variable to store the site id
        await page.evaluateOnNewDocument((entry) => {
          window.measurement_data = entry;
        }, entry);

        page.on('request', request => handleRequest(request, entry, page));
        page.on('response', response => handleResponse(response, entry, page));
        // page.on('console', msg => handleConsoleMessage(msg, entry));

        // we are exposing the sendToQueue function to the page (to send the data later to redis)
        await page.exposeFunction('sendToQueue', async (message) => {
          const jobData = { message: message };
          // wiretappingQueue = await getQueueInstance(siteID);
          // get random queueinstance between 0 and redis_worker
          wiretappingQueue = queueInstances[Math.floor(Math.random() * getConfig('redis_workers'))];
          // console.log("I GOT_________________________________:" + Math.floor(Math.random() * getConfig('redis_workers')))

          const job = wiretappingQueue.createJob(jobData);
          try {
            const savedJob = await job.save();
            //console.log(`Event is queued with ID: ${savedJob.id}`);
          } catch (err) {
            console.error('Error creating job:', err);
          }
        });

        await page.evaluateOnNewDocument(() => {
          window.sendToQueue = window.sendToQueue || function (message) {
            if (typeof window.sendToQueue === 'function') {
              window.sendToQueue(message);
            }
          };
        });

        await page.evaluateOnNewDocument(`(${overrideJSFunctionsAndPropertiesStr})()`);
        try {

          console.log(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - Navigating to page: ${entry[0]} (${entry[1]})`);

          // Navigate to the page with a 'load' event wait condition
          const domReadyCheckPromise = new Promise((resolve) => setTimeout(() => resolve('domNotReady'), getConfig("dom_ready_wait_time")));
          const navigationPromise = page.goto(siteURL, {
            // waitUntil: 'domcontentloaded',
            // waitUntil: 'networkidle2', 
            waitUntil: 'load',
            timeout: getConfig("dom_ready_wait_time")
          }).catch(e => {
            console.error(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - Timeout during navigation to ${siteID}: ${e}`);
          });

          // Race between navigation and 5-second timeout
          const navigationResult = await Promise.race([navigationPromise, domReadyCheckPromise]);
          if (navigationResult === 'domNotReady') {
            console.warn(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - DOM not ready within ${getConfig("dom_ready_wait_time")} for ${siteID}.`);
          }

          // Wait for 3 seconds before starting interactions, regardless of page load status
          await Promise.all([
            navigationPromise,
            delay(3000) // Waits for 3 seconds
          ]);
          // Set a total timeout for interactions
          const interactionTimeoutPromise = new Promise(resolve => setTimeout(resolve, getConfig("timeout_interactions"), 'interactionTimeout'));
          const interactionResult = await Promise.race([interactWithPage(page, entry), interactionTimeoutPromise]);

          if (interactionResult === 'interactionTimeout') {
            console.log(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - Interaction timed out after ${getConfig("timeout_interactions")} seconds for ${siteID}`);
          } else {
            console.log(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - Interactions completed successfully for ${siteID}`);
          }

          if (interactionResult === 'totalTimeout') {
            console.log(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - Total page interaction timed out after 30 seconds: ${entry[1]}`);
          } else {
            console.log(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - Interactions completed successfully for ${entry[1]}`);
          }

        } catch (e) {
          console.error(`${format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS')} - Failed to process ${entry[1]}: ${e}`);
        } finally {

          try {
            // TODO: Fix it, it throws sometimes errors.
            const cookies = await page.cookies();
            for (const cookie of cookies) {
              storeData("cookies", [
                entry[0], entry[1], cookie.name, cookie.value, cookie.domain, cookie.path, cookie.expires, cookie.size, cookie.httpOnly ? 1 : 0, cookie.secure ? 1 : 0, cookie.session ? 1 : 0
              ]);
            }
          } catch (e) {
            console.log("error during getting/storing cookies: " + e.message)
          }
          try {
            await closePage(page);
          }
          catch (e) {
            console.log("error during closing page: " + e.message
            ) // Close the page
          }
          try {
            await closeBrowser(browser);
          }
          catch (e) {
            console.log("error during closing browser: " + e.message
            ) // Close the browser
          }
        }



        // end catch here


      } catch (fatal) {
        console.error('🚨 Could not start browser:', fatal);
      }

    }
    try {
      await closeBrowser(browser);
    }
    catch (e) {
      console.log("error during closing browser: " + e.message
      ) // Close the browser
    }
  }
  catch (e) {
    console.log('\x1b[41m%s\x1b[0m', "unhandled error : " + e.message);
  }
}

async function closePage(page) {
  if (!getConfig('do_not_close_browser')) {
    if (!page.isClosed()) {
      const closePage = page.close();
      await Promise.race([
        closePage,
        new Promise(resolve => setTimeout(resolve, 2000))
      ]);
    }
  } else {
    console.log("Page is not closed (debugging)!")
    // wait 100 seconds (sleep) before running furhter code
    await new Promise(resolve => setTimeout(resolve, 10000000));
  }
}
async function closeBrowser(browser) {
  if (!getConfig('do_not_close_browser')) {
    await browser.close();
  } else {
    console.log("Browser is not closed (debugging)!")
  }
}

async function printCurrentState() {
  const row_urls = await readUrlsFromCsv(); // Read URLs from CSV
  const crawledUrls = await getCrawledURLs(); // Make sure to await this call 
  console.log('\x1b[42m%s\x1b[0m',
    `Crawled URLs (%): ${crawledUrls.length}, ${(crawledUrls.length / row_urls.length * 100).toFixed(2)}%`
  );
}



const groupByRank = (urls) => {
  const groupedUrls = {};
  for (const [id, url] of urls) {
    const rank = id.split('_')[0];
    if (!groupedUrls[rank]) {
      groupedUrls[rank] = [];
    }
    groupedUrls[rank].push([id, url]);
  }
  return Object.values(groupedUrls);
};


async function bumpChunkAndExit() {
  const cfgPath = path.join(__dirname, 'configs.js');
  const raw = fs.readFileSync(cfgPath, 'utf8');

  const maxChunk = parseInt(/max_chunk_to_process\s*:\s*(\d+)/.exec(raw)[1], 10);
  const urlListMatch = /url_list\s*:\s*['"](.+?_chunk_)(\d+)['"]/.exec(raw);

  if (!urlListMatch) {
    console.error('cannot parse url_list.');
    process.exit(1);
  }

  const prefix = urlListMatch[1];
  const curr = parseInt(urlListMatch[2], 10);

  if (curr >= maxChunk) {
    console.log(`Already lust chunk (${curr}). Measurement done.`);
    process.exit(0);
  }

  const next = curr + 1;
  const updated = raw.replace(
    /url_list\s*:\s*['"].+?_chunk_\d+['"]/,
    `url_list: "${prefix}${next}"`
  );

  fs.writeFileSync(cfgPath, updated, 'utf8');
  // print colored green message
  console.log('\x1b[42m%s\x1b[0m', `→ url_list in configs.js was adjusted to ${next}.`);


  //await cleamUpRedis()

  process.exit(0);
}



async function cleamUpRedis() {
  try {
    console.log('All browser instances have finished.');

    // Wait 120 seconds (2 minutes)
    console.log('Waiting 120 seconds before stopping Redis...');
    await new Promise(resolve => setTimeout(resolve, 120000));

    console.log('Stopping Redis service...');
    //await execPromise('brew services stop redis');
    console.log('Redis stopped successfully.');

    console.log('Cleaning up Redis data directory...');
    //await execPromise('rm -rf /opt/homebrew/var/db/redis/*');
    console.log('Redis data directory cleaned successfully.');

    console.log('Starting Redis service...');
    //await execPromise('brew services restart redis');
    console.log('Redis started successfully.');

  } catch (error) {
    console.error(`Error: ${error.message}`);
  }
  finally {
    // Ensure Redis is restarted even if an error occurs
    try {
      console.log('Restarting Redis service...');
      await execPromise('brew services start redis');
      await execPromise('brew services restart redis');
      console.log('Redis restarted successfully.');
    } catch (restartError) {
      console.error(`Error restarting Redis: ${restartError.message}`);
    }
  }
}



(async () => {
 
 
  //await execPromise('brew services start redis');

  await setupDatabase();
  // exit
  const row_urls = await readUrlsFromCsv(); // Read URLs from CSV
  const crawledUrls = await getCrawledURLs(); // Make sure to await this call

  printCurrentState()
  try {
    await prepareQueues();
  }
  catch (e) {
    console.log('\x1b[41m%s\x1b[0m', "error during preparing queues - without redis I cannot work: " + e.message);
    // throw e;
  }

  const urls = [];

  for (const [id, url] of row_urls) {
    // Check if the site_id is in the crawled URLs using the Set
    if (!crawledUrls.includes(id)) {
      urls.push([id, url]); // Keep this URL if it's not crawled
    }
  }


  // Group URLs by rank
  const groupedUrls = groupByRank(urls);

  const concurrentBrowsers = getConfig('concurrentBrowsers');
  if (concurrentBrowsers > 1) {
    const chunkSize = Math.ceil(groupedUrls.length / concurrentBrowsers);

    // Split grouped URLs into chunks for parallel processing
    const urlChunks = [];
    for (let i = 0; i < groupedUrls.length; i += chunkSize) {
      urlChunks.push(groupedUrls.slice(i, i + chunkSize));
    }

    // Launch multiple Puppeteer instances concurrently using Promise.all
    await Promise.all(
      urlChunks.map(async (chunk) => {
        const flattenedChunk = chunk.flat(); // Flatten the chunk before processing
        await startCrawler(flattenedChunk);
      })
    );
  } else {
    const flattenedUrls = groupedUrls.flat();
    await startCrawler(flattenedUrls);
  }


  console.log('All browser instances have finished.');

  

  await bumpChunkAndExit()



})();
