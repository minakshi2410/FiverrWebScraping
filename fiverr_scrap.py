from os import name
import pandas as pd
# import requests
from proxy_request import ProxyRequest
from bs4 import BeautifulSoup
from requests.models import encode_multipart_formdata
import os
import urllib
import re

requests = ProxyRequest()
print(os.getcwd())
with open('keyword.txt','r') as f:
    keywords = [key.strip() for key in f.read().split('\n')]
print("keywords"+str(keywords))
fo = open("review_url.txt","w")
count =0
for key in keywords:
    key = re.sub(r' +','%20',key)
    print(key)
    url= "https://www.fiverr.com/search/gigs?query="+key+"&source=top-bar&search_in=everywhere&search-autocomplete-original-term="+key
    response = requests.get(url)
    print("got response", response.status_code)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    sellers = soup.find_all('div',{'class': "gig-wrapper-impressions gig-wrapper card"})
    
    for seller in sellers:
        link_url= seller.find('a').get('href')
        review_url= 'https://fiverr.com'+ link_url
        fo.write(review_url+'\n')
        print(review_url)
        count+=1
fo.close()
print("seller count:"+str(count))