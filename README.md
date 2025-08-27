# Wiretapping Measurement

A comprehensive research framework for measuring and analyzing potential wiretapping activities and data leakage patterns in web environments. This project provides automated tools for web crawling, data collection, and analysis of sensitive information transmission patterns.

## 🎯 Project Overview

This research project aims to detect and measure potential wiretapping vulnerabilities by:

- **Automated Web Crawling**: Systematically visiting websites and simulating user interactions
- **Data Leak Detection**: Identifying potential transmission of sensitive information to third parties
- **Traffic Analysis**: Analyzing network requests and responses for encoded or obfuscated data
- **Statistical Analysis**: Processing collected data to identify patterns and vulnerabilities

## 🏗️ Architecture

The project consists of two main components working together:

### 1. Crawler System (`crawler/`)

A sophisticated web crawling framework built with Node.js and Puppeteer:

- **`crawler.js`**: Main crawling engine with Puppeteer automation
- **`listener.js`**: Process manager and Chrome browser lifecycle management
- **`process_queue.js`**: Redis-based job queue processor for distributed crawling
- **`interactions.js`**: Automated user interaction simulation (form filling, clicking)
- **`configs.js`**: Centralized configuration management
- **`overrides.js`**: JavaScript function overrides for monitoring

#### Supporting Components:

- **`helpers/`**: Database operations, BigQuery integration, and utility functions
- **`lists/`**: Website lists and subpage extraction tools
- **`post-processes/`**: Data leak detection and analysis scripts
- **`measurement_data/`**: SQLite databases for storing crawl results

### 2. Analysis Tools (`measurement-scripts/`)

Python-based analysis and visualization toolkit:

- **`analysis.ipynb`**: Jupyter notebook for data analysis and visualization
- **`utils.py`**: Analysis utility functions and data processing helpers
- **`setup.sh`**: Environment setup script for external dependencies
- **`requirements.txt`**: Python package dependencies

## 🚀 Quick Start

### Prerequisites

- **Node.js 23+** (managed via nvm)
- **Python 3.8+** with Jupyter
- **Redis Server**
- **Chrome/Chromium Browser**

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd wiretapping-measurement
   ```

2. **Install system dependencies** (Ubuntu/Debian):

   ```bash
   sudo apt update && sudo apt install -y \
     libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
     libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
     libasound2 libpangocairo-1.0-0 libgtk-3-0 \
     nodejs npm redis-server unzip
   ```

3. **Setup Node.js environment**:

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
   source ~/.bashrc
   nvm install 23 && nvm use 23 && nvm alias default 23
   ```

4. **Install Node.js dependencies**:

   ```bash
   cd crawler/
   npm install
   ```

5. **Setup Python environment**:

   ```bash
   cd measurement-scripts/
   pip install -r requirements.txt
   ./setup.sh  # Downloads tracker databases
   ```

6. **Start Redis server**:
   ```bash
   sudo systemctl enable redis-server
   sudo systemctl start redis-server
   ```

### Running the System

1. **Start the crawler system**:

   ```bash
   cd crawler/

   # Start listener (manages Chrome processes)
   nohup node listener.js > run.log &

   # Start queue processor (handles crawl jobs)
   nohup node process_queue.js > queue.log &
   ```

2. **Monitor progress**:

   ```bash
   tail -f run.log queue.log
   ```

3. **Analyze results**:
   ```bash
   cd measurement-scripts/
   jupyter notebook analysis.ipynb
   ```

## 📊 Key Features

### Web Crawling Capabilities

- **Multi-browser support**: Chrome/Chromium with configurable options
- **Interaction simulation**: Form filling, button clicking, navigation
- **Request interception**: Monitor and analyze all network traffic
- **JavaScript override**: Custom monitoring of sensitive API calls
- **Distributed processing**: Redis-based job queue for scalability

### Data Collection

- **Network requests**: Complete HTTP/HTTPS traffic capture
- **DOM analysis**: Page structure and content examination
- **Third-party tracking**: Identification of external domains and services
- **Encoded data detection**: Multiple encoding/compression format support
- **SQLite storage**: Efficient local data persistence

### Analysis Tools

- **Leak detection**: Automated identification of potential data leaks
- **Encoding analysis**: Support for Base64, Base32, compression formats
- **Statistical analysis**: Pattern recognition and trend identification
- **Visualization**: Charts and graphs for result presentation
- **BigQuery integration**: Cloud-based data warehouse support

## 🔧 Configuration

Main configuration options in `crawler/configs.js`:

```javascript
{
  concurrentBrowsers: 1,          // Number of parallel browsers
  redis_workers: 20,              // Redis queue workers
  timeout_site: 95000,            // Site load timeout (ms)
  url_list: "lists/Result_25.csv", // Target website list
  max_subpage: 10,                // Subpages per site
  // ... additional options
}
```

## 📁 Data Flow

1. **Input**: Website list (`lists/Result_25.csv`)
2. **Processing**: Automated crawling with interaction simulation
3. **Storage**: Raw data in SQLite (`measurement_data/`)
4. **Analysis**: Python scripts process stored data
5. **Output**: Leak detection results and statistical reports

## 🛠️ Development

### Adding New Detection Methods

- Extend `post-processes/leackdetector.py` for new leak patterns
- Add encoding support in `post-processes/new_leak_identifier.py`
- Update analysis notebooks with new visualization methods

### Scaling the System

- Increase `redis_workers` for higher throughput
- Deploy multiple crawler instances with shared Redis
- Use BigQuery for large-scale data analysis

## 📝 Research Applications

This framework supports research in:

- **Web privacy analysis**
- **Third-party tracking measurement**
- **Data exfiltration detection**
- **Compliance monitoring**
- **Security vulnerability assessment**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit a pull request with detailed description

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🆘 Troubleshooting

### Common Issues

**Chrome crashes or timeouts**:

```bash
# Kill all Chrome processes
pkill -9 -f chrome
# Restart the crawler
node listener.js
```

**Redis connection errors**:

```bash
# Check Redis status
sudo systemctl status redis-server
# Clear Redis database if needed
redis-cli FLUSHDB
```

**Memory issues with large datasets**:

- Reduce `concurrentBrowsers` in config
- Increase system swap space
- Process data in smaller chunks

For detailed setup instructions specific to your platform, see `crawler/README.md`.
