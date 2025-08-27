const util = require('util');

const { exec } = require('child_process');
const execPromise = util.promisify(exec);


async function cleamUpRedis() {
    try {
      console.log('All browser instances have finished.');
  
      // Wait 120 seconds (2 minutes)
      console.log('Waiting 120 seconds before stopping Redis...');
      await new Promise(resolve => setTimeout(resolve, 5000));
  
      console.log('Stopping Redis service...');
      await execPromise('brew services stop redis');
      console.log('Redis stopped successfully.');
  
      console.log('Cleaning up Redis data directory...');
      await execPromise('rm -rf /opt/homebrew/var/db/redis/*');
      console.log('Redis data directory cleaned successfully.');
  
      console.log('Starting Redis service...');
      await execPromise('brew services start redis');
      console.log('Redis started successfully.');
      
    } catch (error) {
      console.error(`Error: ${error.message}`);
    }
  }


  cleamUpRedis();
  