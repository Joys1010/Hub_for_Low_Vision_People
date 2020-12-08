# Hub_for_Low_Vision_People

# Description

> Helping people who has low vision to search things easier with the internet shopping mall. (Gmarket, Emart, Lotte mall)

# Environments

- node.js - v14.7.0
- python3 - v3.8.5
- npm -v6.14.7

# How to use

### 0. Get Google API key file

- Cloud Vision API
- Cloud Text-to-Speech API

### 0. Make a mongoDB atlas and get connect-url

### 1. Make an .env file

```bash
# Lvp_Hub/.env 
GOOGLE_APPLICATION_CREDENTIALS  = 'location of Google API key file'
DB_CONNECT = 'URL of connecting MongoDB'
```

### 2. Install python3 pip3 packages

- selenium
- bs4
- pandas
- webdriver_manager
- lxml
- pymongo
- scikit-build
- opencv-python

### 3. Install chrome-driver by your OS for crawling 
```bash
$ sudo apt-get install chrominum-drvier
```

### 4. Get started!

```bash
# Lvp_Hub/
$ npm start
```
