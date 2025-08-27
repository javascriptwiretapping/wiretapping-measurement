const { spawn, exec } = require('child_process');
const ps = require('ps-node');

function isChromeRunning(callback) {
  ps.lookup({ command: 'chrome' }, (err, resultList) => {
    if (err) {
      throw new Error(err);
    }
    const chromeRunning = resultList.length > 0;
    callback(chromeRunning);
  });
}

function killChromeProcesses(callback) {
  const killCommand = `
    pkill -9 -i -f chrome || true;
    pkill -9 -i -f chromium || true;
    pkill -9 -i -f selenium || true;
    pkill -9 -f chrome_crashpad_handler || true;
    pkill -9 -f chrome-sandbox || true;
    pkill -9 -f chrome-wrapper || true;
    pkill -9 -f chrome-remote-desktop-host || true;
    pkill -9 -f headless_shell || true;
    pkill -9 -f "Google Chrome for Testing" || true;
  `;

  exec(killCommand, { shell: '/bin/bash' }, (killErr, stdout, stderr) => {
    if (killErr) {
      console.error('❌ Error killing Chrome processes:', killErr);
    } else {
      console.log('✅ Chrome processes killed.');
    }
    if (callback) callback();
  });
}

function startCrawler() {
  console.log('🚀 Starting crawler.js...');
  
  const crawler = spawn('node', ['crawler.js']);

  crawler.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  crawler.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  crawler.on('close', (code) => {
    console.log(`⚠️ crawler.js crashed/closed with code ${code}.`);

    console.log('🔪 Killing Chrome instances because crawler.js crashed...');
    killChromeProcesses(() => {
      isChromeRunning((running) => {
        console.log(`Chrome was ${running ? 'still' : 'not'} running after kill.`);

        console.log('🔄 Restarting crawler in 1 second...');
        setTimeout(startCrawler, 1000);
      });
    });
  });
}

startCrawler();