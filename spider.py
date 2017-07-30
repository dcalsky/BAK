from bs4 import BeautifulSoup, NavigableString
from os import path
from urllib.parse import urljoin
import json
import requests

# Strategy: 
# Primary key: ('title', 'time')
# Set i = 0
# 1. if current[i] === history[0]
# 1. True -> store current[0:i] -> if i > 0: update last time 
# 3. False -> send current[i] -> i++ -> back to [2]

ROOT_URL = 'http://sse.tongji.edu.cn'
UNDER_GRADUATE_CATALOG = '/data/list/bkstz'

CURRENT_URL = urljoin(ROOT_URL, UNDER_GRADUATE_CATALOG)

class Li:
    def __init__(self, title, href, time):
        self.title = title
        self.href = href
        self.time = time
    def __iter__(self):
       return iter([('title',self.title), ('href',self.href), ('time',self.time)])

r = requests.get(url = CURRENT_URL)
soup = BeautifulSoup(r.text, 'html.parser')

result = soup.find("ul", class_='data-list')
array = []
for child in result.contents:
    if isinstance(child, NavigableString): 
        continue
    li = Li(child.a.text.strip(), urljoin(ROOT_URL, child.a.get('href').strip()), child.find('span', class_='data-list-time').text.strip())
    print('标题: ', li.title)
    print('链接: ', li.href)
    print('时间: ', li.time)
    array.append(dict(li))
    
    with open('data.json', 'w+') as f:
        json.dump(array, f)