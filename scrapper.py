from re import X, findall
from sys import getprofile
from typing import Text
import pandas as pd
from proxy_request import ProxyRequest
from bs4 import BeautifulSoup
from requests.models import Response
import os

def getReviewDetails(review,rev_no):
    
    reviewer_name = review.find('div',{'class':'reviewer-details'}).find('h5').text
    country= review.find('div',{'class':'country-name tbody-6'}).text
    review_rating = review.find('div', {'class':'reviewer-details'}).find('span', {'class':'total-rating-out-five text-display-7'}).text
    review_description= review.find('div',{'class':'review-description'}).find('p').text
    rev_total[rev_no] = [reviewer_name.strip(),country.strip(),review_rating.strip(),review_description.strip()]
    return rev_total

# def getNextPageReviewDetails(response,rev_no):
#     global rev_total_df
#     data = response.text
#     soup = BeautifulSoup(data, 'html.parser')
#     reviews = soup.find_all('div',{'class':'views-row'})
#     for review in reviews:
#         rev_no=rev_no+1
#         rev_total= getReviewDetails(review,rev_no)
#         rev_total_df = pd.DataFrame.from_dict(rev_total, 
#                                     orient = 'index', 
#                                     columns = ['Reviewer Name','Country', 'Review Rating','Review Description'])

#         # print("Total Companies:", rev_no)
#     rev_total_df.to_csv(os.path.join('reviewDetails.csv'), index=False)
#     return rev_no

requests = ProxyRequest()
web_url =open("review_url.txt" ,"r")
urlList=web_url.read().splitlines()
web_url.close()
rev_no = 0
rev_total = {}
for url in urlList:
    response = requests.get(url)
    print("got response", response.status_code)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    reviews = soup.find_all('li',{'class':'review-item'})
    for review in reviews:
        rev_no+=1
        print("review no : {}".format(rev_no))
        rev_total= getReviewDetails(review,rev_no)
        rev_total_df = pd.DataFrame.from_dict(rev_total, 
                                orient = 'index', 
                                columns = ['Reviewer Name','Country', 'Review Rating','Review Description'])
rev_total_df.to_csv(os.path.join('reviewDetails.csv'), index=False)
    # pageNo:int=0
    # PageFlag=True
    # while PageFlag:
    #     pageNo=pageNo+1
    #     nextPageUrl= a +'?' + 'page=' + str(pageNo)  +"#"+ b
    #     response = requests.get(nextPageUrl)
    #     firstPageRevNo=rev_no
    #     rev_no=getNextPageReviewDetails(response, rev_no)
    #     if firstPageRevNo == rev_no:
    #         PageFlag=False