import requests
import time
import json
from bs4 import BeautifulSoup
from itertools import cycle
import traceback
import logging

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.FileHandler('./fiverr.log'), logging.StreamHandler()])

class ProxyRequest:
    def __init__(self,proxy_page=0) -> None:
        self.user_agents = cycle([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.37',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41'
        ])
        self.get_headers = {
            
            'authority': 'www.fiverr.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.fiverr.com',
            'accept-language': 'en-JP,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,hi-IN;q=0.6,hi;q=0.5,en-US;q=0.4',
            }
        self.post_headers = self.get_headers

        self.proxy_page = proxy_page
        self.proxy = {} # trying with no proxy
        self.proxies_cycle = cycle(self.get_proxy())

    def get_proxy(self):
        proxies_list = []

        with open('proxy_list.json') as f:
            proxies_list = json.load(f)
        proxies_per_process = len(proxies_list)//1 # change according to no. of processes
        return [{}] + proxies_list[self.proxy_page*proxies_per_process:proxies_per_process+(self.proxy_page*(proxies_per_process))]

    def get(self, url, headers = None, **kwargs):
        r = None
        timeout = time.time() 
        if not headers:
            headers = self.get_headers
        while 1:
            if time.time() - timeout >= 120: # 2 minutes from now
                logging.info("Request got timeout after 2 min")
                break
            try:
                headers.update({'User-Agent':next(self.user_agents)})
                self.proxy = next(self.proxies_cycle)
                # self.session.proxies.update(self.get_proxy())
                logging.info('started request')
                tempTime = time.time()
                r = requests.get(url, headers=headers, proxies=self.proxy, timeout=30, **kwargs)
                logging.info(f'ended request! Time taken : {time.time()-tempTime}')
                if  r.status_code != 200 :
                    logging.error(f"Bad Request: {r.status_code}")
                    if r.status_code == 403:
                        continue
                    break

                soup = BeautifulSoup(r.content, 'lxml')
                mydivs = soup.findAll("div")
                if len(mydivs) > 0:
                    if "Captcha" in str(mydivs[0]):
                        logging.error("got captcha error![GET]")
                        continue
                break
            except Exception as e:
                logging.error(f"Exception occurred: something went wrong!\n{e}")
                break
        return r

    def post(self, url, payload):
        r = None
        timeout = time.time()
        while 1:
            if time.time() - timeout >= 120: # 2 minutes from now
                logging.error("Request got timeout after 2 min")
                break
            try:
                self.post_headers.update({'User-Agent':next(self.user_agents)})
                self.proxy = next(self.proxies_cycle)
                # session.proxies.update(get_proxy())
                logging.info('started Post request')
                tempTime = time.time()
                r = requests.post(url, headers=self.post_headers, proxies=self.proxy, timeout=30, data=payload)
                logging.info(f'ended request! Time taken : {time.time()-tempTime}')

                if  r.status_code != 200 :
                    logging.error(f"Bad Request: {r.status_code}")
                    if r.status_code == 403:
                        continue
                    break

                soup = BeautifulSoup(r.content, 'lxml')
                mydivs = soup.findAll("div")
                if len(mydivs) > 0:
                    if "Captcha" in str(mydivs[0]):
                        logging.error("got captcha error![POST]")
                        continue
                break
            except Exception as e:
                traceback.print_exc()
                # logging.error(f"Exception occurred: something went wrong!\n{e}")
                break
        return r