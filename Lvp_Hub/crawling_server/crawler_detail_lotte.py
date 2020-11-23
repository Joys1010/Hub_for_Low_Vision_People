#lotte 상세
import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
#chrome driver & DB ㄷㅏ 주석차리함 

def crawler_detail_lotte(url):

    #soup= BeautifulSoup(requests.get(url).content,'lxml')
    
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

    main_img = soup.select("#stickyTopParent > div.stickyVisual.vue-affix.affix-top > div > div.swiper-container.largeImgSlide.default.swiper-container-initialized.swiper-container-vertical > div > div.swiper-slide.swiper-slide-active > div > img")
    print(main_img[0]["src"])
    name = soup.select_one("div.productName > h1").get_text()
    print(name)

    price = soup.select_one("#stickyTopParent > div.productDetailTop > div:nth-child(2) > div > div.priceInfo > div > span").get_text()
    print(price+"원")

    __product_info = soup.select(" #stickyTabParent > div.tabArea > div > div > div > div.productDetailInfo ")#> tbody> tr
    product_info =[]
    for info in __product_info :
        _info = info.select("dl")
        for __info in _info:
            _in = __info.select_one("dt")
            __in = __info.select_one("dd")
            if _in and __in is not None:
                tmp_info=[]
                tmp_info.append(_in.text)
                tmp_info.append(__in.text)
                product_info.append(tmp_info)

    img = soup.select("#m2-prd-frame")
    soup = BeautifulSoup(requests.get(img[0]["src"]).content, 'lxml')
    img = soup.select("img")

    for i in range (0,len(img)):
        print(img[i]['src'])
    # 이마트 때무네
    print("")
    print(product_info)
   driver.close()

#url = "https://www.lotteon.com/p/product/LM2852520000002?sitmNo=LM2852520000002_001&mall_no=1&dp_infw_cd=SCH전복"
crawler_detail_lotte(sys.argv[1])
#crawler_detail_lotte(url)
