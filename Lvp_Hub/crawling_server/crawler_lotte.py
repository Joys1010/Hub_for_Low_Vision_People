from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import sys
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
#chrome driver & DB ㄷㅏ 주석차리함 
#DB
import pymongo 
import dns

client = pymongo.MongoClient("mongodb+srv://yaewon:yaewon@testcluster.hft0m.mongodb.net/capstone?retryWrites=true&w=majority")
db = client.LVP_HUB
lotte_db = db.productData  #collection 선택 ~ emart, lotte, gmarket 있는데 테스트 용으로 test table도 만들어놨어 ! 



def crawler_lotte(word):
   # word="딸기"
    url = 'https://www.lotteon.com/search/search/search.ecn?render=search&platform=pc&q='+word+'&mallId=1'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #driver = webdriver.Chrome('./crawling_server/chromedriver',options=chrome_options) 
    driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
    #remember
    driver.get(url) 
    time.sleep(3) 
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml') 
    #soup= BeautifulSoup(requests.get(url).content,'lxml')
    output =[]
    soup = soup.select('li.srchProductItem > div')
    for tmp_soup in soup:
        title =  tmp_soup.select_one(' a > div > div:nth-child(1) >div.srchProductUnitTitle')
        price = tmp_soup.select_one("a  div div:nth-child(2)  div  span.srchCurrentPrice ")
        url =  tmp_soup.select(" a ")
        img = tmp_soup.select(" div a div.srchThumbImageWrap img")
        review = tmp_soup.select_one('a > div > div:nth-child(1) > div.srchProductStatusArea > div > span.srchRatingScore > strong')
        if review is not None:
            review = review.get_text().replace('(','').replace(')','')
        else :
            review = 0
        title_post = title.text.replace("\n","")
        price_post = price.text.replace('원','')
        price_post = price_post.replace("\n","")
        price_post = price_post.replace(",","")
        numbers = re.findall("\d+",price_post) 
        data = {"search_category":"lotte", "search_word":word, "product_name":title_post, "price":numbers[0], "image":img[0]["src"], "detail":url[0]["href"],"review":review}
        lotte_db.insert_one(data)

        tmp = [word,title_post , numbers[0],img[0]["src"],url[0]["href"],review]
        output.append( tmp)
        driver.close()

    return output

    #sys.argv[1]
def check_lotte(word):
    output =[]
    
    output = crawler_lotte(word)
    
    if output is not None :
        for i in range (0, len(output)):
            print(output[i])




check_lotte(sys.argv[1])
#crawler_lotte(sys.argv[1])
