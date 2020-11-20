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


#DB
import pymongo 
import dns
# 정은 언니용 capstone_test
#client = pymongo.MongoClient("mongodb+srv://yaewon:yaewon@testcluster.hft0m.mongodb.net/capstone_test?retryWrites=true&w=majority")

#db = client.capstone_test
client = pymongo.MongoClient("mongodb+srv://yaewon:yaewon@testcluster.hft0m.mongodb.net/capstone?retryWrites=true&w=majority")

#db = client.capstone_test
db = client.capstone

gmarket_db = db.productData  #collection 선택 ~ emart, lotte, gmarket 있는데 테스트 용으로 test table도 만들어놨어 ! 




def crawler_gmarket(word):
   # word="딸기"
    url = 'https://browse.gmarket.co.kr/search?keyword='+word
    #driver = webdriver.Chrome('./crawling_server/chromedriver') # 설치 폴더에 주의합니다. 
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
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
    soup = BeautifulSoup(html, 'html.parser') 
   # browser.close()

    img = soup.select('div.box__item-container > div.box__image > a > img') #src

  ##section__inner-content-body-container > div:nth-child(3) > div:nth-child(4) > div > div.box__image > a > img
    title =soup.select("div.box__item-container > div.box__information > div.box__information-major > div.box__item-title > span > a > span.text__item")
   #
    price = soup.select('div.box__item-container > div.box__information > div.box__information-major > div.box__item-price > div.box__price-seller > strong')
    url = soup.select('div.box__item-container > div.box__information > div.box__information-major > div.box__item-title > span > a')
#div.box__item-container > div.box__information > div.box__information-major > div.box__item-price > div.box__price-seller > strong
    if len(title)==0:
        return []
    title_input =[]
    price_input =[]
    img_input =[]
    output =[]


    for i in range (0,len(title)):
        check_img = img[i]["src"]
        if check_img[0] == "/":
            check_img = check_img.replace('//gdimg','http://gdimg')
        price_post = price[i].text.replace('원','')
        price_post = price_post.replace("\n","")
        price_post = price_post.replace(",","")
        numbers = re.findall("\d+",price_post) 
        data = {"search_category":"gmarket", "search_word":word, "product_name":title[i].text, "price":numbers[0], "image":check_img, "detail":url[i]["href"]}
        gmarket_db.insert_one(data)

        # 앞에서부터 순서대로 검색어 // 상품명// 가격 // 이미지 // 상세 
        tmp = [word ,title[i].text ,numbers[0] ,check_img ,url[i]["href"]]

        output.append( tmp)

    
   # print(output)    
    #print(subject)
    data = pd.DataFrame(output) 
    data.columns = ['검색어','title', 'price', 'img','url']
    #경로 고민해보셈 +이거 추가 인지 
    
    #data.to_csv('./crawling_gmarket.csv') 
    csv_name = './crawling_server/crawling_gmarket_search.csv'
    if not os.path.exists(csv_name):
        data.to_csv(csv_name, index=False, mode='w', encoding='utf-8-sig')
    else:
        data.to_csv(csv_name, index=False, mode='a', encoding='utf-8-sig', header=False)
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
