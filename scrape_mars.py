# coding: utf-8

# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req
import re
from splinter import Browser
import nbconvert

def scrape():
    scraped_data_dict = {}
    ## NASA Mars News
    # assign mars news site html to variable
    mars_news = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = req.get(mars_news)
    mars_beautifulsoup = bs(response.text, "html.parser")


    # find mars news title 
    news_title = mars_beautifulsoup.find('div', class_='content_title')
    news_title = news_title.text.strip()
    
    # find mars news paragraph 
    news_para = mars_beautifulsoup.find('div', class_='rollover_description_inner')
    news_para = news_para.text.strip()
    
    ### Store data into dict
    scraped_data_dict['news_title'] = news_title
    scraped_data_dict['news_para'] = news_para

    ## JPL Mars Space Images - Featured Image
    # assign jpl url to variable
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser = Browser('chrome', headless=False)
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    jpl_html = browser.html
    jpl_beautifulsoup = bs(jpl_html, 'html.parser')

    jpl_links = jpl_beautifulsoup.find('div', class_="carousel_items")
    jpl_tag = jpl_links.find('a', class_='button fancybox')
    jpl_url_link = "https://www.jpl.nasa.gov" + tag.get('data-fancybox-href')

    ### Store data into dict
    scraped_data_dict['jpl_url_link'] = jpl_url_link

    ## MARS WEATHER
    # assign mars twitter url to variable
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    response = req.get(mars_twitter)
    mars_tweet_beutifulsoup = bs(response.text, "html.parser")

    mars_tweet = mars_tweet_beutifulsoup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    mars_tweet_text = mars_tweet.text

    ### Store data into dict
    scraped_data_dict['mars_tweet'] = mars_tweet_text

    ## MARS FACTS
    # assign url to variable
    mars_facts_url = 'https://space-facts.com/mars/'

    # read html tables into dataframes list
    mars_facts_tables = pd.read_html(mars_facts_url)

    # assign mars facts table to variable
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df.columns = ['fact_title','fact_value']

    #convert df to html
    mars_facts_html = mars_facts_df.to_html('mars_facts.html', index=False)

    ### Store data into dict
    scraped_data_dict['mars_facts'] = mars_facts_html

    # assign hemispheres url to variable
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_response = req.get(mars_hemispheres_url)
    mars_hem_beautifulsoup = bs(mars_response.text, 'html.parser')

    # find all image lists
    image_urls_list = mars_hem_beautifulsoup.find_all('a', class_="itemLink")
    # open browser
    browser1 = Browser('chrome', headless=False)
    # initialize hemisphere images
    hemisphere_images = []

    # loop over all images in the list
    for image in image_urls_list:
        #extract hemisphere name 
        hemi_name = image.h3.text
        
        #vist the mars page
        browser1.visit(mars_hemispheres_url)
        
        #go to the hemisphere image page
        browser1.click_link_by_partial_text(hemi_name)
        
        # extract html from the browser
        image_html = browser1.html
        
        # create beautifulsoup object from the source
        mars_tweet_beutifulsoup = bs(image_html, "html.parser")
        
        # find the full image from the page
        full_image = mars_tweet_beutifulsoup.find('img', class_="wide-image")
        
        # get the src url
        full_image_url = full_image['src']
        
        # store name/url in dict
        image_dict = {}
        image_dict['name'] = hemi_name
        image_dict['url'] = full_image_url
        # append dict to list
        hemisphere_images.append(image_dict)
    
    ### Store data into dict
    scraped_data_dict['mars_hemisphere_images'] = hemisphere_images

    return scraped_data_dict

