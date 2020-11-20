#chrome driver 
import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString, Tag
import time
import pandas as pd
import sys
import requests

def crawler_detail_gmarket(url):
    
    soup= BeautifulSoup(requests.get(url).content,'lxml')
    ##stickyTopParent > div.stickyVisual.vue-affix.affix-top > div > div.swiper-container.largeImgSlide.default.swiper-container-initialized.swiper-container-vertical > div > div > div > img
    main_img = soup.select("#container > div.item-topinfowrap > div.thumb-gallery.uxecarousel.alone > div.box__viewer-container > ul > li.on ")#> a > img")
    print(main_img)
    
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
