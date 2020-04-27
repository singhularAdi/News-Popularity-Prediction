import pickle
import numpy as np
from fabulous.color import highlight_green

from scraper import get_links, parse_page_data


links = get_links()
data = parse_page_data(links)

model = pickle.load(open("finalized_model.sav", 'rb'))
y = model.predict(data)

indices = np.argwhere(y == np.max(y)).flatten()
print(highlight_green("\nArticles most likely to go viral:\n\n"))

for key, value in enumerate(indices):
    print('{}.'.format(key+1), end = '    ')
    print(links[value])
