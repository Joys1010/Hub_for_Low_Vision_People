#emart detail

import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def crawler_detail_emart(url):
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

    main_img = soup.select("#mainImg")
    print("http:"+main_img[0]["src"])
    name = soup.select_one("div.cdtl_row_top > div.cdtl_col_rgt > div.cdtl_prd_info > h2").get_text()
    print(name)

    price = soup.select_one("div.cdtl_row_top > div.cdtl_col_rgt > div.cdtl_info_wrap > div.cdtl_optprice_wrap > div > span > em").get_text()
    print(price+"원")

    img = soup.select("div.cdtl_sec.cdtl_seller_html > div.cdtl_detail_img > img")
    if len(img) > 0 :
        for i in range(0, len(img)):
            print(img[i]["src"]) 

    else :
        img = soup.select("#_ifr_html")
    
    #    print(img)
        detail ='http://emart.ssg.com'+ img[0]["src"]
    # print(detail)
        driver.get(detail) 
        time.sleep(3) 
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #nameList = soup.findAll("p")
        imgList = soup.findAll("img")
        '''
        img_text =[]

        for name in nameList:
            #       print(name.get_text())
            img_text.append(name.get_text())

        #     img = soup.select("#m2root > p > img")
        detail_img = []
        '''

        for i in range(0,len(imgList)): 
            #detail_img.append(imgList[i]["src"])
            print(imgList[i]["src"])
    #detail_page =[]

    
    #detail_page.append(detail_info)
    #detail_page.append(img_text)
    #detail_page.append(detail_img)
    #print(detail_page)
    
    
    #return detail_page

#url ="http://emart.ssg.com/item/itemView.ssg?itemId=2097000068565&siteNo=6001&salestrNo=2493&tlidSrchWd=고등어&srchPgNo=1&src_area=elist"
#url = "http://emart.ssg.com/item/itemView.ssg?itemId=1000037080202&siteNo=6001&salestrNo=6005&tlidSrchWd=고등어&srchPgNo=1&src_area=elist&advertBidId=1000340834&advertExtensTeryDivCd=10"
#url = "http://www.ssg.com/item/itemView.ssg?itemId=1000041250742&siteNo=6001&salestrNo=2034&tlidSrchWd=휴지&srchPgNo=1&src_area=ssglist"
crawler_detail_emart(sys.argv[1])
#crawler_detail_emart(url)
