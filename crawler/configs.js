const os = require('os');

function getHostnameNumber() {
    // Check if the platform is macOS (Darwin)
    if (os.platform() === 'darwin') {
        return 1;
    }
    const hostname = os.hostname().split('-');
    return hostname.length > 1 ? hostname[hostname.length - 1] : '';
}

function getConfig(name) {
    const params = {
        // debugging options
        do_not_close_browser: false,
        do_not_close_page: false,
        static_site_url: "https://example.com",
        dont_use_list_sites: false,
        max_subpage: 10,
        concurrentBrowsers: 1,
        redis_workers: 20,

        // general options 
        url_list: "lists/Result_25.csv",
        max_chunk_to_process: 2,
        db_name: "measurement_data/",
        db_name_redis: "measurement_data/crawler_data_redis.db",
        timeout_site: 95000,
        timeout_interactions: 82000,
        dom_ready_wait_time: 15000,
        redis_ip: "127.0.0.1",
        redis_port: 6379,

        //sensitiveStrings
        sensitiveStrings: [
            'velisiteID@trustedmed.de',
            '4922122200',
            'SaltySeedsTea9!',
            'hi_my_honey_text',
            'curious-cat.com',
            'https://curious-cat.com',
            'my_funny_honey',
            'hi_my_honey_field'
        ]
    };
    return params[name];
}

module.exports = {
    getConfig
};