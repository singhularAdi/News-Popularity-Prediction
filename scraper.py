import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

url = "https://in.mashable.com/"
res = requests.get(url)

data = res.text

soup = BeautifulSoup(data, 'html.parser')

links = set()
for link in soup.findAll('a', attrs={'href': re.compile("^https://in.mashable.com/tech|https://in.mashable.com/e")}):
        links.add(link.get('href'))
print(len(links))
link = list(links)[0]


print(link)


res2 = requests.get(link)

data2 = res2.text
soup = BeautifulSoup(data2, 'html.parser')


# img_count = 0
# for img in soup.findAll('img', attrs={'itemprop': re.compile("contentUrl")}):
#         img_count+=1






vid_count = 0
for div in soup.findAll('div', attrs={'class':"vplayer"}):
        vid_count = 1

print(vid_count)

post_date = soup.find('time')
encoded_weekday = datetime.strptime(post_date['datetime'].split('T')[0],"%Y-%m-%d").weekday()
# monday = 0 sunday = 6


title = soup.find('h1',attrs={'id': "id_title"}).text

num_words_title = len(title.strip().split())
num_words_text = len(soup.get_text().strip().split())
# print(text)