# Import Libraries
from bs4 import BeautifulSoup
import pandas as pd
import json
import requests
import csv
from time import sleep

# Where data will be stored
final_list = []

print('“Your most unhappy customers are your greatest source of learning.” — Bill Gates')

# Website that will be scraped
url = 'https://www.trustpilot.com/review/wealthsimple.com'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

# Get number of reviews
num_reviews = soup.find('h2', class_ = 'header--inline').text.strip()
num_reviews = num_reviews.partition('\n')[0]

# Get number of pages
pages = min(250, int(num_reviews)//20)

# Scrape Reviews
for pg in range(1, pages):
    pg = url + '?page=' + str(pg)
    r = requests.get(pg)
    soup = BeautifulSoup(r.text, 'lxml')
    for paragraph in soup.find_all('section', class_ = 'review__content'):

        # Scrape title
        title = paragraph.find('h2', class_ = 'review-content__title').text.strip()
        title = str(title)
        
        # Scrape comment
        content_object = paragraph.find('p', class_ = 'review-content__text')
        content = ""

        if content_object != None:
            content = content_object.text.strip()

        # Scrape date 
        date = paragraph.find('div', class_ = 'review-content-header__dates')
        date = date.find('script', type = 'application/json')
        date = str(date)
        date = date.split('publishedDate')
        date = date[1][0:13][3:] 

        # Scrape rating
        rating = paragraph.find('div', {'class': 'star-rating--medium'}).find('img').get('alt')
        rating = str(rating)

        final_list.append([title, content, date, rating])

# Create DataFrame
df = pd.DataFrame(final_list, columns = ['Title','Content', 'Date', 'Rating'])
df = df.drop_duplicates(keep = 'first')

# Convert Date to DateTime
df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
df = df.sort_values(by = 'Date', ascending = True).reset_index()
df = df.drop('index', axis = 1)

# Get number rating
df['num_rating'] = df['Rating'].str[:2].astype(int)

print(df)
df.to_csv(r'C:\Users\Terence\Desktop\test.csv')