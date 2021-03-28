# Dependencies and Setup
import pandas as pd
import requests
import time
import pymongo
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

   # nasa mars news scrape setup

    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html = browser.html
    time.sleep(2)
    soup = BeautifulSoup(html, 'html.parser')

    # find stories

    news_feed = soup.find_all('li', class_='slide')

    print(news_feed[0])
    # it worked!

    mars_feed = news_feed[0]
    mars_feed

    # latest mars news scrape

    latest_news = mars_feed.find('div', class_= 'content_title').text
    latest_news

    # paragraph

    latest_para = mars_feed.find('div', class_='article_teaser_body').text
    latest_para

    # mars images (yikes) image url scrape

    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    # jpl_image_path = soup.find_all('img', class_= 'headerimage fade-in')
    # jpl_image_path

    jpl_image_path = soup.find_all('img', class_= 'headerimage')[0]['src']
    jpl_image_path

    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'

    featured_image_url = base_url + jpl_image_path

    featured_image_url

    # mars facts

    mars_facts_url = 'https://space-facts.com/mars/'

    mars_table = pd.read_html(mars_facts_url)
    mars_table

    mars_table_df = mars_table[0]
    mars_table_df

    mars_table_df.columns = ['Mars','Facts / Measurements']
    mars_table_df

    # table to html

    mars_html = mars_table_df.to_html()
    mars_html

    # clean html table

    mars_html = mars_html.replace('\n', '')

    mars_html

    mars_table_df.to_html('mars_facts.html')

    # mars hemispheres - remember to click links

    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    html = browser.html

    time.sleep(2)
    soup = BeautifulSoup(html, 'html.parser')

    hemi_list = soup.find_all(class_= 'description')

    hemi_list # takes a few seconds to load

    # append the titles
    titles = []
    for title in hemi_list:
        titles.append(title.a.h3.text)
        
    titles

    # image links info

    browser.visit(mars_hemi_url)
    hemisphere_image_urls = []

    for x in range(len(titles)):
        browser.click_link_by_partial_text(titles[x])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = titles[x]
        img_url = soup.find(class_='downloads')
        
        hemispheres_dict = {}
        hemispheres_dict['title'] = title
        hemispheres_dict['img_url'] = img_url.a['href']
        hemisphere_image_urls.append(hemispheres_dict)
        browser.back()
        
    hemisphere_image_urls # takes a minute and don't quit browser in cell

    # close the browser
    browser.quit()

    mars_dictionary = {
        'article_title':latest_news,
        'article_paragraph':latest_para,
        'article_image':featured_image_url,
        'mars_facts':mars_html,
        'hemisphere_image_urls':hemisphere_image_urls
    }

    mars_dictionary

return mars_dictionary

