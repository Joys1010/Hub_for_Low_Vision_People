#이마트 검색
import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import json
import sys
import os
import csv

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def crawler_emart(word):
    url = 'http://emart.ssg.com/search.ssg?target=all&query='+word

    #jjeong remember
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
    #remember

    driver.get(url) 
    time.sleep(3) 
    html = driver.page_source
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')  
    undefine= soup.select('#content > div.csrch_tip.notranslate > div.tip_txt')
    title =  soup.select(' div.cunit_info > div.cunit_md.notranslate > div > a > em.tx_ko')
    price = soup.select(" div.cunit_info > div.cunit_price.notranslate > div.opt_price > em  ")
    img = soup.select(" div.cunit_prod > div.thmb > a > img ")

    url =  soup.select( "div.cunit_prod > div.thmb > a ")
    if len(title)==0:
        return []
    title_input =[]
    price_input =[]
    img_input =[]
    output =[]
    
   # print(str(len(title))+":"+str(len(price))+":"+str(len(img)))

    for i in range (0,len(title)-1):
        
        check_img = img[i]["src"]
        check_url = url[i]["href"]
        if check_img[0] == "/":
            #check_img = check_img.replace('//item','item')
            check_img = 'http:'+check_img;
        if check_url[0] !="h":
            check_url = "http://shinsegaemall.ssg.com/" + check_url
        tmp = [word,title[i].text,price[i].text,check_img,check_url]
        output.append( tmp)

    data = pd.DataFrame(output) 
    data.columns = ['검색어','title', 'price', 'img','url']
    csv_name = './crawling_server/crawling_emart_search.csv'
    if not os.path.exists(csv_name):
        data.to_csv(csv_name, index=False, mode='w', encoding='utf-8-sig')
    else:
        data.to_csv(csv_name, index=False, mode='a', encoding='utf-8-sig', header=False)
    #경로 고민해보셈 +이거 추가 인지 
    return output

def check_emart(word):
    output =[]
    exist = False
    csv_name = './crawling_server/crawling_emart_search.csv'
    if not os.path.exists(csv_name):
        output = crawler_emart(word)
    else:
        with open(csv_name,'r') as f: 
            reader = csv.reader(f)
            for c in reader:
                if c[0]==word:
                    output.append(c)
                    exist = True
        if exist == False :
            output =  crawler_emart(word)
            #return output
    if output is not None :
        for i in range (0, len(output)-1):
            print(output[i])

check_emart(sys.argv[1])
