
import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def crawler_detail_gmarket(url):
    #url = 'http://item.gmarket.co.kr/Item?goodscode=1886205248'
    #driver = webdriver.Chrome('./crawling_server/chromedriver') # 설치 폴더에 주의합니다. 
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
    #remember
    driver.get(url) 

    time.sleep(3) 


    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser') 







    detail_info = soup.select("#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content >div> table:nth-child(1) > tbody ")
    img = soup.select("#detail1")

    detail = img[0]["src"]

    driver.get(detail) 
    time.sleep(3) 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    img = soup.findAll("img")
    detail_img = []
    #
    for i in range(0,len(img)-1): 
        detail_img.append(img[i]["src"])
        print(img[i]["src"])
    output = []
    output.append(detail_info)
    output.append(detail_img)
   # print(output)
    return detail_img
crawler_detail_gmarket(sys.argv[1])
