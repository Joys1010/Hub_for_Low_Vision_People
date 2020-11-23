import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import os
import time
import pandas as pd
import sys
import re
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

#chrome driver & DB ㄷㅏ 주석차리함 
#DB
import pymongo 
import dns

client = pymongo.MongoClient("mongodb+srv://yaewon:yaewon@testcluster.hft0m.mongodb.net/capstone?retryWrites=true&w=majority")
db = client.LVP_HUB
gmarket_db = db.productData  #collection 선택 ~ emart, lotte, gmarket 있는데 테스트 용으로 test table도 만들어놨어 ! 


def crawler_gmarket(word):
   # word="딸기"
    url = 'https://browse.gmarket.co.kr/search?keyword='+word
    # 설치 폴더에 주의합니다. 
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./crawling_server/chromedriver',options=chrome_options) 
    #driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
    #remember
    driver.get(url) 
    time.sleep(3) 

    some_tag = driver.find_elements_by_class_name('box__component')
  
    #print(some_tag)
    for i in range(0,len(some_tag)-1):
            action = ActionChains(driver)
            action.move_to_element(some_tag[i]).perform()

    
    html = driver.page_source
   # print(html)
    soup = BeautifulSoup(html, 'lxml') 
   # browser.close()
    output =[]
    soup = soup.select('div.box__item-container ')
    for tmp_soup in soup: 
        img = tmp_soup.select_one(' div.box__image > a > img') #src
        title =tmp_soup.select_one("div.box__information > div.box__information-major > div.box__item-title > span > a > span.text__item")
        price = tmp_soup.select_one('div.box__information > div.box__information-major > div.box__item-price > div.box__price-seller > strong')
        url = tmp_soup.select_one('div.box__information > div.box__information-major > div.box__item-title > span > a')
        review = tmp_soup.select_one('div.box__information > div.box__information-score > ul > li.list-item.list-item__pay-count > span.text')
        if review is not None:
            review = review.get_text()
        else :
            review = 0
        check_img = img["src"]
        if check_img[0] == "/":
            check_img = check_img.replace('//gdimg','http://gdimg')
        price_post = price.text.replace('원','')
        price_post = price_post.replace("\n","")
        price_post = price_post.replace(",","")
        numbers = re.findall("\d+",price_post) 
        data = {"search_category":"gmarket", "search_word":word, "product_name":title.text, "price":numbers[0], "image":check_img, "detail":url["href"],"review":review}
        gmarket_db.insert_one(data)

        # 앞에서부터 순서대로 검색어 // 상품명// 가격 // 이미지 // 상세 
        tmp = [word ,title.text ,numbers[0] ,check_img ,url["href"],review]
        output.append( tmp)
    driver.close()

    
    
    
    if len(title)==0:
        return []
    '''
    output =[]


    for i in range (0,len(title)):
        check_img = img[i]["src"]
        if check_img[0] == "/":
            check_img = check_img.replace('//gdimg','http://gdimg')
        price_post = price[i].text.replace('원','')
        price_post = price_post.replace("\n","")
        price_post = price_post.replace(",","")
        numbers = re.findall("\d+",price_post) 
        data = {"search_category":"gmarket", "search_word":word, "product_name":title[i].text, "price":numbers[0], "image":check_img, "detail":url[i]["herf"]}
        gmarket_db.insert_one(data)

        # 앞에서부터 순서대로 검색어 // 상품명// 가격 // 이미지 // 상세 
        tmp = [word ,title[i].text ,numbers[0] ,check_img ,url[i]["href"]]

        output.append( tmp)

    '''    
    return output

def check_gmarket(word):
    output =[]
    exist = False
    csv_name = './crawling_server/crawling_gmarket_search.csv'
    if not os.path.exists(csv_name):
        output = crawler_gmarket(word)
    else:
        with open(csv_name,'r') as f: 
            reader = csv.reader(f)
            for c in reader:
                if c[0]==word:
                    output.append(c)
                    exist = True
        if exist == False  :
            output = crawler_gmarket(word)
            #return output
    if output is not None and len(output) >=0 :
        for i in range(0,len(output)):
            print(output[i])

#crawler_gmarket(sys.argv[1])
check_gmarket(sys.argv[1])
