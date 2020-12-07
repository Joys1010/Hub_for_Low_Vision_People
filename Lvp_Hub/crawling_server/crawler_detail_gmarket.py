#chrome driver 
import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString, Tag
import time
import pandas as pd
import sys
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
def crawler_detail_gmarket(url):
    
    soup= BeautifulSoup(requests.get(url).content,'lxml')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./crawling_server/chromedriver',options=chrome_options) 
    #driver = webdriver.Chrome(executable_path="/home/ubuntu/Hub_for_Low_Vision_People/Lvp_Hub/crawling_server/chromedriver",options=chrome_options) # 설치 폴더에 주의합니다. 
    driver.get(url) 
    time.sleep(3) 
    ##container > div.item-topinfowrap > div.thumb-gallery.uxecarousel.alone > div.box__viewer-container > ul > li.on > a > img
    main_img =driver.find_elements_by_css_selector(' div.item-topinfowrap > div.thumb-gallery.uxecarousel.alone > div.box__viewer-container > ul > li.on')
    ##stickyTopParent > div.stickyVisual.vue-affix.affix-top > div > div.swiper-container.largeImgSlide.default.swiper-container-initialized.swiper-container-vertical > div > div > div > img
    #main_img = soup.select("#container > div.item-topinfowrap > div.thumb-gallery.uxecarousel.alone > div.box__viewer-container > ul > li.on ")#> a > img")
    main_img = BeautifulSoup(main_img[0].get_attribute('innerHTML'), 'lxml') 
    main_img = main_img.select(" a > img")
   
    print(main_img[0]['src'])
    driver.close()

    name = soup.select_one("#itemcase_basic > h1").get_text()
    print(name) 

    price = soup.select_one("#itemcase_basic > p > span > strong").get_text()
    print(price)


    __product_info = soup.select(" #vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content > div.box__product-notice-list ")#> tbody> tr
    product_info =[]
    for info in __product_info :
        _info = info.select("tr")
        for __info in _info:
            _in = __info.select_one("th")
            __in = __info.select_one("td")
            if _in and __in is not None:
                tmp_info=[]
                tmp_info.append(_in.text)
                tmp_info.append(__in.text)
                product_info.append(tmp_info)


    detail_info = soup.select("#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content >div> table:nth-child(1) > tbody ")
    img = soup.select("#detail1")
    soup = BeautifulSoup(requests.get(img[0]["src"]).content, 'lxml')
    img = soup.findAll("img")
    detail_img = []
    #
    for i in range(0,len(img)): 
        detail_img.append(img[i]["src"])
        print(img[i]["src"])
    # 이마트 때무네
    print("")
    print(product_info)
    
    return detail_img
crawler_detail_gmarket(sys.argv[1])
#url = "http://item.gmarket.co.kr/Item?goodscode=1915402492"
#crawler_detail_gmarket(url)

