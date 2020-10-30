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



    ##item_detail > div.cdtl_sec_area > div:nth-child(5) > div.cdtl_cont_info > div > table > tbody

    img = soup.select("#_ifr_html")
    
#    print(img)
    detail ='http://emart.ssg.com'+ img[0]["src"]
   # print(detail)
    driver.get(detail) 
    time.sleep(3) 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    nameList = soup.findAll("p")
    imgList = soup.findAll("img")
    img_text =[]
    
    for name in nameList:
 #       print(name.get_text())
        img_text.append(name.get_text())
    
#     img = soup.select("#m2root > p > img")
    detail_img = []
    for i in range(0,len(imgList)-1): 
       detail_img.append(imgList[i]["src"])
       print(imgList[i]["src"])
    detail_page =[]
   
    '''
    detail_page.append(detail_info)
    detail_page.append(img_text)
    detail_page.append(detail_img)
    #print(detail_page)
    '''
    
    return detail_page

#url ="http://emart.ssg.com/item/itemView.ssg?itemId=2097000068565&siteNo=6001&salestrNo=2493&tlidSrchWd=고등어&srchPgNo=1&src_area=elist"
#url = "http://emart.ssg.com/item/itemView.ssg?itemId=1000037080202&siteNo=6001&salestrNo=6005&tlidSrchWd=고등어&srchPgNo=1&src_area=elist&advertBidId=1000340834&advertExtensTeryDivCd=10"
crawler_detail_emart(sys.argv[1])
