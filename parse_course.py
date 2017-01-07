import re
from bs4 import BeautifulSoup
import requests
from urlREGEX import URL_REGEX
import os


http_proxy  = "http://10.3.100.207:8080"
https_proxy = "https://10.3.100.207:8080"
ftp_proxy   = "ftp://10.3.100.207:8080"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

def getUniqueItems(iterable):
    result = []
    for item in iterable:
        if item not in result:
            result.append(item)
    return result

base_url = 'http://unacademy.in'
course_url = 'https://unacademy.com/course/january-2017-daily-summary-and-analysis-of-the-hindu/Q8Q3FZIV'

r = requests.get(course_url,proxies=proxyDict)
soup = BeautifulSoup(r.content, "lxml")

lessons = []

for a in soup.find_all('a', href=True):
    lessons.append(a['href'])
# print(lessons)

def set_start_url(img_start_url):
    img_url_split = img_start_url.split('/')
    last_seg = img_url_split[-1].split('.')
    last_seg[0] = str(0)
    img_url_split[-1] = '.'.join(last_seg)
    img_next_url = '/'.join(img_url_split)
    return img_next_url

def get_next_url(img_start_url):
    img_url_split = img_start_url.split('/')
    last_seg = img_url_split[-1].split('.')
    jpeg_num = int(last_seg[-2])
    last_seg[0] = str(jpeg_num + 1)
    img_url_split[-1] = '.'.join(last_seg)
    img_next_url = '/'.join(img_url_split)
    return img_next_url



# TODO : If dir does not exist, create it.
def download(url_as_str, dir='./images'):
    # headers = get_headers()
    cmd = ''
    headers = []
    filename = url_as_str.split('/')[-1]
    if not os.path.exists(filename):
        cmd = "wget -P " + dir + " -A jpg,jpeg,gif,png " + url_as_str
    return os.system(cmd)


def download_all(img_start_url):
    """
    Takes STRING url
    """
    response = download(img_start_url)
    if (response == 2048):
        return True
    else:
        return download_all(get_next_url(img_start_url))


lesson_list = [l for l in lessons if('/lesson/') in l]
lesson_list = getUniqueItems(lesson_list)

lesson_urls = [base_url + l for l in lesson_list]


def get_img_url(lesson_url):
    imgs = []
    lesson_soup = BeautifulSoup(requests.get(lesson_url,proxies=proxyDict).content, "lxml")
    image = lesson_soup.find(itemprop='image')
    img_url = re.findall(URL_REGEX, str(image))[0]
    return img_url

# TO DO : If the url error = 404 => test for png and other variants.

# for lesson_url in lesson_urls:
# 	# r_lesson = requests.get(lesson_url)
# 	img_start_url = get_img_url(lesson_url)
# 	confirm = download_all(get_next_url(img_start_url))

# print(lesson_urls)
lesson_url = lesson_urls[2]
print(type(lesson_url))
img_start_url = set_start_url(get_img_url(lesson_url))
print(img_start_url)
confirm = download_all(img_start_url)
print(confirm)
# print(lesson_list)
# lesson_list = [l for l in r_lesson.txt if('/lesson/') in l]
