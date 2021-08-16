from os import name
import pandas as pd
from proxy_request import ProxyRequest
from bs4 import BeautifulSoup
import os
import urllib
import re

def getReviewDetails(review,rev_no,keyword,service_url):
    reviewer_name = review.find('div',{'class':'reviewer-details'}).find('h5').text
    country= review.find('div',{'class':'country-name tbody-6'}).text
    review_rating = review.find('div', {'class':'reviewer-details'}).find('span', {'class':'total-rating-out-five text-display-7'}).text
    review_description= review.find('div',{'class':'review-description'}).find('p').text
    rev_total[rev_no] = [keyword,service_url,reviewer_name.strip(),country.strip(),review_rating.strip(),review_description.strip()]
    return rev_total

requests = ProxyRequest()
print(os.getcwd())
with open('keyword.txt','r') as f:
    keywords = [key.strip() for key in f.read().split('\n')]
print("keywords"+str(keywords))
rev_total = {}
rev_no = 0
for keyword in keywords:
    key = re.sub(r' +','%20',keyword)
    print(key)
    url= "https://www.fiverr.com/search/gigs?query="+key+"&source=top-bar&search_in=everywhere&search-autocomplete-original-term="+key
    print('Requesting main url: {}'.format(url))
    response = requests.get(url)
    print("got response", response.status_code)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    sellers = soup.find_all('div',{'class': "gig-wrapper-impressions gig-wrapper card"})
    for seller in sellers:
        link_url= seller.find('a').get('href')
        service_url= 'https://fiverr.com'+ link_url
        print('Requesting serive url: {}'.format(service_url))
        response = requests.get(service_url)
        print("got response", response.status_code)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        reviews = soup.find_all('li',{'class':'review-item'})
        for review in reviews:
            rev_no+=1
            print("review no : {}".format(rev_no))
            rev_total= getReviewDetails(review,rev_no,keyword,service_url)
            rev_total_df = pd.DataFrame.from_dict(rev_total, 
                                    orient = 'index', 
                                    columns = ['Keyword','Service Url','Reviewer Name','Country', 'Review Rating','Review Description'])

rev_total_df.to_csv(os.path.join('reviewDetailsCombined.csv'), index=False)