import re
from bs4 import BeautifulSoup
import requests
from urlREGEX import URL_REGEX
import os
import shutil
import argparse

# http_proxy = "http://10.3.100.207:8080"
# https_proxy = "https://10.3.100.207:8080"
# ftp_proxy = "ftp://10.3.100.207:8080"

http_proxy = ""
https_proxy = ""
ftp_proxy = ""


proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}


base_url = 'https://iasbaba.com/daily-current-affairs-quiz/'


def get_days_url(base_url):
    r = requests.get(base_url, proxies=proxyDict)
    to_return = []
    if r.status_code != 404:
        day_soup = BeautifulSoup(r.content, "lxml")
        links = re.findall(URL_REGEX,str(day_soup))
        for l in links:
            if 'iasbabas-daily-current-affairs-quiz-day' in l:
                to_return.append(l)
    return to_return


day_urls = get_days_url(base_url)

def get_pdf_url(day_url):
    r = requests.get(day_url, proxies=proxyDict)
    to_return = []
    if r.status_code != 404:
        day_soup = BeautifulSoup(r.content, "lxml")
        links = re.findall(URL_REGEX,str(day_soup))
        for l in links:
            if '.pdf' in l:
                to_return = l
    return to_return

def download(url_as_str, dir='./iasbaba'):
    # headers = get_headers()
    cmd = ''
    headers = []
    filename = url_as_str.split('/')[-1]
    if not os.path.exists(filename):
        cmd = "wget -P "+ dir +' '  +  url_as_str
        print(cmd)
    return os.system(cmd)

for urls in day_urls:
    pdf_url = get_pdf_url(urls)
    if pdf_url:
        download(str(pdf_url))
    else:
        print('no pdf on ' + str(urls))
