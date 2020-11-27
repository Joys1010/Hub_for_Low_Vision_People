#이마트 검색
#chrome driver & DB ㄷㅏ 주석차리함 
import urllib 
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import json
import sys
import os
import requests
#DB
import pymongo 
import dns

client = pymongo.MongoClient("mongodb+srv://yaewon:yaewon@testcluster.hft0m.mongodb.net/LVP_HUB?retryWrites=true&w=majority")
db = client.LVP_HUB
emart_db = db.productData

def crawler_emart(word):
    start = time.time()
    url = 'https://emart.ssg.com/search.ssg?target=all&query='+word
    soup= BeautifulSoup(requests.get(url).content,'lxml')
    cunit_info = soup.select('#idProductImg > li.cunit_t232')
    output =[]
    for i in range(0,len(cunit_info)):
        tmp_soup = cunit_info[i] 
        
        title =  tmp_soup.select_one(' div.cunit_info > div.cunit_md.notranslate > div > a > em.tx_ko').get_text()
        price = tmp_soup.select_one(" div.cunit_info > div.cunit_price.notranslate > div.opt_price > em  ")
        review = tmp_soup.select_one(" div.cunit_info > div.cunit_app > div > span > em")
        if review is not None :
            review =review.get_text()
        else :
            review =0
        img = tmp_soup.select_one(" div.cunit_prod > div.thmb > a > img ")
        url = tmp_soup.select_one( "div.cunit_prod > div.thmb > a ")

        check_img = img["src"]
        check_url = url["href"]
        if check_img[0] == "/":
            check_img = 'https:'+check_img
        if check_url[0]!="h":
            check_url = "https://emart.ssg.com/" + check_url
        price_post = price.text.replace('원','')
        price_post = price_post.replace("\n","")
        price_post = price_post.replace(",","")
        numbers = re.findall("\d+",price_post) 
        data = {"search_category":"emart", "search_word":word, "product_name":title, "price":numbers[0], "image":check_img, "detail":check_url, "review" :review}
        emart_db.insert_one(data)
        tmp = [word,title,numbers[0],check_img,check_url,review]
        output.append(tmp)
        
    
    if len(title)==0:
        return []
   
    #print(round(time.time()-start,3))
    return output

def get_count(num, p):
	list = []
	allocate = int(num/p)
	for n in range(p):
		list.append(allocate)
	list[p-1]+= num%p
	return list

def check_emart(word):
    output =[]
    exist = False
    
    output =  crawler_emart(word)
  
    if output is not None :
        for i in range (0, len(output)):
            print(output[i])
    
check_emart(sys.argv[1])
