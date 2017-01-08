import re
from bs4 import BeautifulSoup
import requests
from urlREGEX import URL_REGEX
import os
import shutil
import argparse

http_proxy = "http://10.3.100.207:8080"
https_proxy = "https://10.3.100.207:8080"
ftp_proxy = "ftp://10.3.100.207:8080"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}


def getUniqueItems(iterable):
    result = []
    for item in iterable:
        if item not in result:
            result.append(item)
    return result


parser = argparse.ArgumentParser(description='Adding course_url and dest_folder')

parser.add_argument('-u', '--url', help='URL',required=True)
parser.add_argument('-d', '--dest', help='destination folder name', required=True)
parser.add_argument('-s', '--start', help='start_lesson', default=0)

args = vars(parser.parse_args())


base_url = 'http://unacademy.in'
course_url = args['url']
# course_url = 'https://unacademy.com/course/january-2017-daily-summary-and-analysis-of-the-hindu/Q8Q3FZIV'

r = requests.get(course_url, proxies=proxyDict)
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

def alternate(img_url):
	img_url_split = img_url.split('/')
	last_seg = img_url_split[-1].split('.')
	if(last_seg[1] == 'png'):
		last_seg[1] = 'jpeg'
	elif (last_seg[1] == 'jpeg'):
		last_seg[1] = 'png'
	img_url_split[-1] = '.'.join(last_seg)
	img_alternate_url = '/'.join(img_url_split)
	return img_alternate_url



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


def download_all(img_start_url,change=0):
    """
    Takes STRING url
    """
    response = download(img_start_url)	
    if(change == 0):
    	if (response == 2048):
    		response = download_all(alternate(img_start_url),1)
    	else:
    		return download_all(get_next_url(img_start_url),0)
    elif (change == 1):
    	if (response == 2048):
    		return True
    	else:
    		return download_all(get_next_url(img_start_url),0)



lesson_list = [l for l in lessons if('/lesson/') in l]
lesson_list = getUniqueItems(lesson_list)

lesson_urls = [base_url + l for l in lesson_list]
print("\n",lesson_urls)


def get_img_url(lesson_url):
    imgs = []
    lesson_soup = BeautifulSoup(requests.get(
        lesson_url, proxies=proxyDict).content, "lxml")
    image = lesson_soup.find(itemprop='image')
    img_url = re.findall(URL_REGEX, str(image))[0]
    return img_url


def mv_lessonwise(destname):
	"""
	Move .jpeg,.png images to dest folder.
	"""
	cur_path = os.getcwd() + "/images/"
	target = cur_path + destname
	print("\n\n MOVING FILES into " + target)
	if not os.path.exists(target):
	    os.makedirs(target)
	imgs = [f for f in os.listdir(cur_path) for a in ['.jpeg','.png'] if f.endswith(a)]
	images = [cur_path + i for i in imgs]
	final_images = [shutil.move(img,	target) for img in images]


i = int(args['start'])
print("i=",i,len(lesson_urls[int(args['start'])-1:]))
for lesson_url in lesson_urls[int(args['start'])-1:]:
    img_start_url = set_start_url(get_img_url(lesson_url))
    confirm = download_all(img_start_url,0)
    mv_lessonwise(args['dest'] + str(i))
    i = i + 1

# lesson_url = lesson_urls[2]
# print(img_start_url)

print("\n\n\n" + str(confirm))
