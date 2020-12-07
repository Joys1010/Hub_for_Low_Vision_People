from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import sys
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

#DB
import pymongo 
import dns

from dotenv import load_dotenv
load_dotenv()
client = pymongo.MongoClient(os.getenv("DB_CONNECT"))

db = client.LVP_HUB
lotte_db = db.productData
MAX_COUNT = 30

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

    output =[]
   
    info = driver.find_elements_by_css_selector('li.srchProductItem > div')
    count =0
    for soup in info:
        tmp_soup = BeautifulSoup(soup.get_attribute('innerHTML'), 'lxml') 
        title =  tmp_soup.select_one(' a > div > div:nth-child(1) >div.srchProductUnitTitle')

        if title is None or len(title)==0:
            return []
   
        price = tmp_soup.select_one("a  div div:nth-child(2)  div  span.srchCurrentPrice ")
        url =  tmp_soup.select(" a ")
        img = tmp_soup.select(" div a div.srchThumbImageWrap img")
        review = tmp_soup.select_one('a > div > div:nth-child(1) > div.srchProductStatusArea > div > span.srchRatingScore > strong')
        if review is not None:
            review = review.get_text().replace('(','').replace(')','').replace(",","")
            if review == '0':
                review =0
        else :
            review = 0
        title_post = title.text.replace("\n","")
        price_post = price.text.replace('원','')
        price_post = price_post.replace("\n","")
        price_post = price_post.replace(",","")
        numbers = re.findall("\d+",price_post)#.replace(",","") 
        numbers = numbers[0].replace(",","")
        data = {"search_category":"lotte", "search_word":word, "product_name":title_post, "price":int(numbers), "image":img[0]["src"], "detail":url[0]["href"],"review":int(review)}
        lotte_db.insert_one(data)

        tmp = [word,title_post , numbers,img[0]["src"],url[0]["href"],review]
        output.append( tmp)
        if count >= MAX_COUNT :
            break
        count = count+1
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

