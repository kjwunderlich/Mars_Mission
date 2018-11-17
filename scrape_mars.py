from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pymongo
import requests
import os
import pandas as pd
from selenium import webdriver
import time

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.nhl_db
collection = db.articles

# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')

# Retrieve the parent divs for all articles
results = soup.find('div', class_='features')

news_title = results.find('div', class_='content_title').text
news_body = results.find('div', class_='rollover_description').text

# get featured image
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

top_thing = soup.find('div', class_='default floating_text_area ms-layer')
footer_thing = top_thing.find('footer')
featured_image_url = 'https://www.jpl.nasa.gov'+ footer_thing.find('a')['data-fancybox-href']


# get twitter info
twitter = 'https://twitter.com/marswxreport?lang=en'
browser.visit(twitter)

twitter_html = browser.html
twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

tweet_text = twitter_soup.find('div', 'js-tweet-text-container').text

#get mars facts and put in dataframe
mars_facts = 'https://space-facts.com/mars/'
browser.visit(mars_facts)    

mars_table = pd.read_html(mars_facts)
mars_table

mars_df = mars_table[0]
mars_df.columns = ['Description', 'Values']

# Reset index 
mars_df.set_index('Description')

# convert dataframe to html
mars_facts = mars_df.to_html()
mars_facts.replace("\n", "")
mars_df.to_html('mars_facts.html')

# search individual urls for hemesphere images
valles_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
cerberus_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
schiaparelli_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
syrtis_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"

browser.visit(cerberus_url)
cerberus_html = browser.html
cerberus_soup = BeautifulSoup(cerberus_html, 'lxml')

browser.visit(valles_url)
valles_html = browser.html
valles_soup = BeautifulSoup(valles_html, 'lxml')

browser.visit(schiaparelli_url)
schiaparelli_html = browser.html
schiaparelli_soup = BeautifulSoup(schiaparelli_html, 'lxml')

browser.visit(syrtis_url)
syrtis_html = browser.html
syrtis_soup = BeautifulSoup(syrtis_html, 'lxml')

cerberus_image = cerberus_soup.find('div', class_='downloads').find('a')['href']
valles_image = valles_soup.find('div', class_='downloads').find('a')['href']
schiaparelli_image = schiaparelli_soup.find('div', class_='downloads').find('a')['href']
syrtis_image = syrtis_soup.find('div', class_='downloads').find('a')['href']

hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": valles_image},
    {"title": "Cerberus Hemisphere", "img_url": cerberus_image},
    {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli_image},
    {"title": "Syrtis Major Hemisphere", "img_url": syrtis_image}
]