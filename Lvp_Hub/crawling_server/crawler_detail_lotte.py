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

    main_img = soup.select("#stickyTopParent > div.stickyVisual.vue-affix.affix-top > div > div.swiper-container.largeImgSlide.default.swiper-container-initialized.swiper-container-vertical > div > div.swiper-slide.swiper-slide-active > div > img")
    print(main_img[0]["src"])

    name = soup.select_one("div.productName > h1").get_text()
    print(name)

    price = soup.select_one("#stickyTopParent > div.productDetailTop > div:nth-child(2) > div > div.priceInfo > div > span").get_text()
    print(price+"원")

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
    #print(img)
    for i in range (0,len(img)):
        print(img[i]['src'])
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
#url = "https://www.lotteon.com/p/product/LM2852520000002?sitmNo=LM2852520000002_001&mall_no=1&dp_infw_cd=SCH전복"
crawler_detail_lotte(sys.argv[1])
#crawler_detail_lotte(url)
