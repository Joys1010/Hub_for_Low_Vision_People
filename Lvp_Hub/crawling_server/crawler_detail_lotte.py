#lotte 상세
import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def crawler_detail_lotte(url):
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

    
    # 참고 해보셈
    # print(detail_info)
    # for i in range(0,len(detail_info)-1): 
    #          save_html = save_html+str(detail_info[i])
    #
    img = soup.select("#m2-prd-frame")
    detail = img[0]["src"]
    driver.get(detail) 
    time.sleep(3) 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #img = soup.select("#m2root > p > img")
    img = soup.select("img")
    print(img)
    '''
    detail_img = []

    if img is None :
        return 

    print(img[0]["src"]);
    for i in range(0,len(img)-1): 
        detail_img.append(img[i]["src"])
    detail_page =[]
   
    detail_page.append(detail_info)
    detail_page.append(detail_img)
    
    
    #print(detail_page)
    return detail_page
'''
#url ="https://www.lotteon.com/p/product/LM8809137650063?sitmNo=LM8809137650063_001&mall_no=1&dp_infw_cd=SCH바나나"
crawler_detail_lotte(sys.argv[1])
#crawler_detail_lotte(url)
