# Setup Instructions

This guide explains how to install the required dependencies and run the application.

## Supported Platforms

We have tested this project on the following operating systems:

- macOS 15.06
- Windows 11
- Ubuntu 22.04

## Clone the Repository

First, clone this repository using Git:

```bash
git clone <this repo>
cd <repo directory>
```

## Install Prerequisites

Use the following commands to install all necessary packages:

```bash
sudo apt update

sudo apt install -y \
  libnss3 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  libgbm1 \
  libasound2 \
  libpangocairo-1.0-0 \
  libpango-1.0-0 \
  libgtk-3-0 \
  libxshmfence1 \
  libx11-xcb1 \
  libxss1 \
  libnss3-tools \
  libdrm2 \
  unzip \
  nodejs \
  npm \
  redis-server
```

Enable and start Redis:

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server --no-pager
```
 
## Setup Node Environment

Install `nvm` (Node Version Manager) and configure Node.js version 23:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

nvm install 23
nvm use 23
nvm alias default 23
```

## Install Node.js Dependencies

Run the following inside the project directory:

```bash
npm install
```

## Clear Redis DB

(Optional) Clear Redis database:

```bash
redis-cli FLUSHDB
```

## Start the Application

Start both listener and queue processor:

```bash
nohup node listener.js > run.log &
nohup node process_queue.js > queue.log &
```

The application is now running in the background.