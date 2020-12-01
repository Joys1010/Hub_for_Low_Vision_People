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

client = pymongo.MongoClient("mongodb+srv://yaewon:yaewon@testcluster.hft0m.mongodb.net/LVP_HUB?retryWrites=true&w=majority")
db = client.LVP_HUB
gmart_db = db.productData


def crawler_gmarket(word):
   # word="딸기"
    url = 'https://browse.gmarket.co.kr/search?keyword='+word
    # 설치 폴더에 주의합니다. 
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #driver = webdriver.Chrome('./crawling_server/chromedriver',options=chrome_options) 
    driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
    #remember
    driver.get(url) 
    time.sleep(3) 

    some_tag = driver.find_elements_by_class_name('box__component')
    output =[]
    info =[]
    for i in range(0,(len(some_tag)-1)):
            action = ActionChains(driver)
            action.move_to_element(some_tag[i]).perform()
            #info.append(some_tag[i].get_attribute('innerHTML'))
            tmp_soup = BeautifulSoup(some_tag[i].get_attribute('innerHTML'), 'lxml') 
        
            img = tmp_soup.select_one('div.box__item-container > div.box__image > a > img') #src
            if img is None :
                continue
            title =tmp_soup.select_one("div.box__item-container > div.box__information > div.box__information-major > div.box__item-title > span > a > span.text__item")

            if title is None or len(title)==0:
                return []
   
            price = tmp_soup.select_one('div.box__information > div.box__information-major > div.box__item-price > div.box__price-seller > strong')
            url = tmp_soup.select_one('div.box__information > div.box__information-major > div.box__item-title > span > a')
            review = tmp_soup.select_one('div.box__information > div.box__information-score > ul > li.list-item.list-item__pay-count > span.text')
            if review is not None:
                review = review.get_text()
                review = re.findall("\d+",review.replace(",",""))
                if len(review)==0:
                    review = 0
                else :
                    review = review[0]
                    review = review.replace(",","")
            else :
                review = 0
            check_img = img['src']
            if check_img[0] == "/":
                check_img = check_img.replace('//gdimg','http://gdimg')
            price_post = price.text.replace('원','')
            price_post = price_post.replace("\n","")
            price_post = price_post.replace(",","")
            numbers = re.findall("\d+",price_post) 
            data = {"search_category":"gmarket", "search_word":word, "product_name":title.text, "price":int(numbers[0].replace(",","")), "image":check_img, "detail":url["href"],"review":int(review)}
            gmart_db.insert_one(data)

            # 앞에서부터 순서대로 검색어 // 상품명// 가격 // 이미지 // 상세 
            tmp = [word ,title.text ,numbers[0].replace(",","") ,check_img ,url["href"],review]
            output.append( tmp)

            if i >30:
                break
           
    driver.close()
    '''
    for soup in info:
        
        s_soup = 
        tmp_soup = BeautifulSoup(soup.get_attribute('innerHTML'), 'lxml') 
        
        img = tmp_soup.select_one('div.box__item-container > div.box__image > a > img ') #src

        title =tmp_soup.select_one("div.box__item-container > div.box__information > div.box__information-major > div.box__item-title > span > a > span.text__item")
        price = tmp_soup.select_one('div.box__information > div.box__information-major > div.box__item-price > div.box__price-seller > strong')
        url = tmp_soup.select_one('div.box__information > div.box__information-major > div.box__item-title > span > a')
        review = tmp_soup.select_one('div.box__information > div.box__information-score > ul > li.list-item.list-item__pay-count > span.text')
        if review is not None:
            review = review.get_text()
            review = re.findall("\d+",review)
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
        #gmarket_db.insert_one(data)

        # 앞에서부터 순서대로 검색어 // 상품명// 가격 // 이미지 // 상세 
        tmp = [word ,title.text ,numbers[0] ,check_img ,url["href"],review]
        output.append( tmp)
    '''    

    
    
    
    return output

def check_gmarket(word):
    output =[]
    exist = False
    
    output = crawler_gmarket(word)
            #return output
    if output is not None and len(output) >=0 :
        for i in range(0,len(output)):
            print(output[i])

#crawler_gmarket(sys.argv[1])
check_gmarket(sys.argv[1])

