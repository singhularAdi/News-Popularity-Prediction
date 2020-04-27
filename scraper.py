import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from fabulous.color import highlight_green

def get_links():
        url = "https://in.mashable.com/"
        res = requests.get(url)

        data = res.text

        soup = BeautifulSoup(data, 'html.parser')

        links = set()
        for link in soup.findAll('a', attrs={'href': re.compile("^https://in.mashable.com/tech|https://in.mashable.com/e")}):
                links.add(link.get('href'))
        
        print(highlight_green("\nRetrieved {} links.".format(len(links))))

        print(highlight_green("\nArticles fetched:\n\n"))

        i = 1
        for key in links:
                print('{}.'.format(i), end = '    ')
                print(key)
                i+=1
        # print('{}.'.format(key+1), end = '    ')
        # print(value)
        return list(links)




def parse_page_data(links):
        page_data = []

        encoder = ColumnTransformer(
                [('days', OneHotEncoder(categories=[[0,1,2,3,4,5,6]]), [7])],
                remainder='passthrough')
                
        for link in links:
                res = requests.get(link)

                data2 = res.text
                soup = BeautifulSoup(data2, 'html.parser')

                img_count = 0.0
                vid_count = 0.0


                for img in soup.findAll('img', attrs={'itemprop': re.compile("contentUrl")}):
                        img_count+=1.0
                
                for div in soup.findAll('div', attrs={'class':"vplayer"}):
                        vid_count += 1.0

                # print(vid_count)

                post_date = soup.find('time')
                weekday = datetime.strptime(post_date['datetime'].split('T')[0],"%Y-%m-%d").weekday()
                # monday = 0 sunday = 6

                channel = link.split('/')[3]

                title = soup.find('h1',attrs={'id': "id_title"}).text

                num_words_title = len(title.strip().split())
                num_words_text = len(soup.get_text().strip().split())
                if channel == "tech":
                        data = [0.0, num_words_title, num_words_text, img_count, vid_count, 0.0, 1.0, weekday]
                elif channel == "entertainment":
                        data = [0.0, num_words_title, num_words_text, img_count, vid_count, 1.0, 0.0, weekday]
                else:
                        data = [0.0, num_words_title, num_words_text, img_count, vid_count, 0.0, 0.0, weekday]

                if data[-1]==6 or data[-1]==5 :
                        data[0] = 1.0
                
                page_data.append(data)
        encoded = encoder.fit_transform(page_data)

        # print(links[0]) 
        # print(page_data[0])
        # print(encoded[0])
        print(highlight_green("\nData preprocessing done."))
        return encoded



# if __name__ == "main"":
#         links = get_links()
#         p = parse_page_data(links)