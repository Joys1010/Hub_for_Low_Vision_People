from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import sys
import csv
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def crawler_lotte(word):
   # word="딸기"
    url = 'https://www.lotteon.com/search/search/search.ecn?render=search&platform=pc&q='+word+'&mallId=1'
    #driver = webdriver.Chrome('./crawling_server/chromedriver') # 설치 폴더에 주의합니다. 
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
    #remember
    driver.get(url) 
    # 19년 5월부터 로그인 페이지 주소가 살짝 바뀌었네요.
    time.sleep(3) 
    html = driver.page_source
    #print(html)
    soup = BeautifulSoup(html, 'html.parser') 
   # subject = soup.body.find_all('li', class_='srchProductItem') 

    title =  soup.select('li.srchProductItem > div > a > div > div:nth-child(1) >div.srchProductUnitTitle')
    price = soup.select("li.srchProductItem div  a  div div:nth-child(2)  div  span.srchCurrentPrice  ")

    img = soup.select("li.srchProductItem div div a div.srchThumbImageWrap img ")
    
    url =  soup.select("li.srchProductItem div a ")
    #div a
    #div a  div div:nth-child(1) div.srchProductUnitTitle
    title_input =[]
    price_input =[]
    img_input =[]
    output =[]

    for i in range (0,len(title)):
        title_post = title[i].text.replace("\n","")
        price_post = price[i].text.replace('원','')
        price_post = price_post.replace("\n","")
        price_post = price_post.replace(",","")
        numbers = re.findall("\d+",price_post) 
        tmp = [word,title_post , numbers[0],img[i]["src"],url[i]["href"]]
        output.append( tmp)

    
    #print(subject)
    data = pd.DataFrame(output) 
    data.columns = ['검색어','title', 'price', 'img','url']
    #경로 고민해보셈 +이거 추가 인지 
    
    #data.to_csv('./crawling_lotte.csv') 
    csv_name = './crawling_server/crawling_lotte_search.csv'
    if not os.path.exists(csv_name):
        data.to_csv(csv_name, index=False, mode='w', encoding='utf-8-sig')
    else:
        data.to_csv(csv_name, index=False, mode='a', encoding='utf-8-sig', header=False)
    return output
    #sys.argv[1]
def check_lotte(word):
    output =[]
    exist = False
    csv_name = './crawling_server/crawling_lotte_search.csv'
    if not os.path.exists(csv_name):
        output = crawler_lotte(word)
    
    else:
        with open(csv_name,'r') as f: 
            reader = csv.reader(f)
            for c in reader:
                if c[0]==word:
                    output.append(c)
                    exist = True
        if exist == False :
            output =  crawler_lotte(word)
            #return outpu
    if output is not None :
        for i in range (0, len(output)):
            print(output[i])



    print(output)
#check_emart(sys.argv[1])
check_lotte(sys.argv[1])
