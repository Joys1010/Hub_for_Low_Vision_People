#emart detail
#chrome driver & DB ㄷㅏ 주석차리함 
import urllib 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests

def crawler_detail_emart(url):
 
    soup= BeautifulSoup(requests.get(url).content,'lxml')
  
    main_img=""
    _main_img = soup.select_one("#mainImg")
    if(_main_img is not None):
        main_img ="http:"+_main_img["src"]
    else:
        return
    print(main_img)
    name = soup.select_one("div.cdtl_row_top > div.cdtl_col_rgt > div.cdtl_prd_info > h2")
    if name is not None :
        name = name.get_text()
    print(name)

    price = soup.select_one("div.cdtl_row_top > div.cdtl_col_rgt > div.cdtl_info_wrap > div.cdtl_optprice_wrap > div > span > em")
    if price is not None :
        price = price.get_text()
    else :
        price = "_"
    print(str(price)+"원")
    __product_info = soup.select("#item_detail > div.cdtl_sec_area > div > div.cdtl_cont_info > div > table > tbody> tr")
    product_info =[]
 
    for info in __product_info :
        #print(info)
        _in = info.select("div")
        tmp_info=[]
        tmp_info.append(_in[0].text)
        tmp_info.append(_in[1].text)
        product_info.append(tmp_info)
    
    img = soup.select("div.cdtl_detail_img > img")
    if img is not None:
        for i in img :
            print(i['src'])
    text = soup.select("div.cdtl_tmpl_tip > div")
    tip_text=[]
    if text is not None :
        for i in text :
            tip_text.append(i.get_text())
    frame_ = soup.select('#_ifr_html')
    
    soup= BeautifulSoup(requests.get('http://emart.ssg.com'+frame_[0]['src']).content,'lxml')
    nameList = soup.select('#wrap_ifr > div')
    imgList = soup.findAll("img")
    p_text=[]
    
    if nameList is not None:
        for name in nameList:
            p_text.append((name.get_text()).replace('\n','').replace('\t',''))
    
    for i in range(0,len(imgList)): 
        print(imgList[i]["src"])
    
    p_text = p_text + tip_text
    print(p_text)
    print(product_info)
   

crawler_detail_emart(sys.argv[1])

