import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    URL = f'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    r = requests.get(URL, headers=headers)
    print(r.status_code)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup

def transform(soup):
    list = soup.find_all('ul', {'class':'ipc-metadata-list ipc-metadata-list--dividers-between sc-71ed9118-0 kxsUNk compact-list-view ipc-metadata-list--base'})
    items = list[0].find_all('li', {'class':'ipc-metadata-list-summary-item sc-1364e729-0 caNpAE cli-parent'})
    for item in items:
        # get name
        detaildiv = item.find_all('div', {'class':'ipc-metadata-list-summary-item__c'})
        name = detaildiv[0].find('h3', {'class':'ipc-title__text'}).text.strip()

        #get release year
        midspans = detaildiv[0].find_all('span', {'class':'sc-be6f1408-8 fcCUPU cli-title-metadata-item'})
        year = ''
        length = ''
        movie_rate = ''
        if len(midspans) == 3:
            year = midspans[0].text.strip() if midspans[0].text else ''
            length = midspans[1].text.strip() if midspans[1].text else ''
            movie_rate = midspans[2].text.strip() if midspans[2] else ''
        elif len(midspans) == 2:
            year = midspans[0].text.strip() if midspans[0].text else ''
            length = midspans[1].text.strip() if midspans[1].text else ''

        #get rating
        rating = detaildiv[0].find('span', {'class': 'ratingGroup--imdb-rating'}).text.strip()
        movie =  {"name":name, "release_year": year, "length": length, "movie_rate": movie_rate,"rating": rating}

        movies_list.append(movie)


movies_list = []
soup = extract(0)  # 0, 10, 20, 30, ......
transform(soup)


df = pd.DataFrame(movies_list)
print(df)

df.to_csv('D:/OneDrive-WSU/OneDrive - Wayne State University/Python/imdb_top250movies.csv')