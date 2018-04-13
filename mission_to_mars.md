

```python
# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req
import re
from splinter import Browser
import nbconvert
```


```python
## NASA Mars News
# assign mars news site html to variable
mars_news = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
response = req.get(mars_news)
mars_beautifulsoup = bs(response.text, "html.parser")
```


```python
# find mars news title 
news_title = mars_beautifulsoup.find('div', class_='content_title')
news_title = news_title.text.strip()
print(news_title)
```

    NASA Invests in Visionary Technology



```python
# find mars news paragraph 
news_para = mars_beautifulsoup.find('div', class_='rollover_description_inner')
news_para = news_para.text.strip()
print(news_para)
```

    NASA is investing in technology concepts, including several from JPL, that may one day be used for future space exploration missions.



```python
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
jpl_url_link = "https://www.jpl.nasa.gov" + jpl_tag.get('data-fancybox-href')
print(jpl_url_link)
```

    https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA13664_ip.jpg



```python
## MARS WEATHER
# assign mars twitter url to variable
mars_twitter = 'https://twitter.com/marswxreport?lang=en'
response = req.get(mars_twitter)
mars_tweet_beutifulsoup = bs(response.text, "html.parser")

mars_tweet = mars_tweet_beutifulsoup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

mars_tweet_text = mars_tweet.text
print(mars_tweet_text)
```

    Sol 2017 (April 09, 2018), Sunny, high -6C/21F, low -75C/-103F, pressure at 7.17 hPa, daylight 05:28-17:21



```python
## MARS FACTS
# assign url to variable
mars_facts_url = 'https://space-facts.com/mars/'

# read html tables into dataframes list
mars_facts_tables = pd.read_html(mars_facts_url)

# assign mars facts table to variable
mars_facts_df = mars_facts_tables[0]
mars_facts_df.columns = ['fact_title','fact_value']
mars_facts_df

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fact_title</th>
      <th>fact_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
#convert df to html
mars_facts_df.to_html('mars_facts.html', index=False)
##Mars Hemisperes

# assign hemispheres url to variable
mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
mars_response = req.get(mars_hemispheres_url)
mars_hem_beautifulsoup = bs(mars_response.text, 'html.parser')

# find all image lists
image_urls_list = mars_hem_beautifulsoup.find_all('a', class_="itemLink")
image_urls_list
```




    [<a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><img alt="Cerberus Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/dfaf3849e74bf973b59eb50dab52b583_cerberus_enhanced.tif_thumb.png"/><div class="description"><h3>Cerberus Hemisphere Enhanced</h3></div></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/schiaparelli_enhanced"><img alt="Schiaparelli Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/7677c0a006b83871b5a2f66985ab5857_schiaparelli_enhanced.tif_thumb.png"/><div class="description"><h3>Schiaparelli Hemisphere Enhanced</h3></div></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/syrtis_major_enhanced"><img alt="Syrtis Major Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/aae41197e40d6d4f3ea557f8cfe51d15_syrtis_major_enhanced.tif_thumb.png"/><div class="description"><h3>Syrtis Major Hemisphere Enhanced</h3></div></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/valles_marineris_enhanced"><img alt="Valles Marineris Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/04085d99ec3713883a9a57f42be9c725_valles_marineris_enhanced.tif_thumb.png"/><div class="description"><h3>Valles Marineris Hemisphere Enhanced</h3></div></a>]




```python


# open browser
browser1 = Browser('chrome', headless=False)
# initialize hemisphere images
hemisphere_images = []
full_images_list = []
# loop over all images in the list
for image in image_urls_list:
    #extract hemisphere name 
    hemi_name = image.h3.text
    
    #vist the mars page
    browser1.visit(mars_hemispheres_url)
    
    # go to the hemisphere image page
    browser1.click_link_by_partial_text(hemi_name)
    
    # go to hemisphere full image
    image_url = browser1.find_link_by_partial_href(".tif/full.jpg").first._element.get_attribute("href")
    
    # store name/url in dict
    image_dict = {}
    image_dict['name'] = hemi_name
    image_dict['url'] = image_url
    
    # append dict to list
    hemisphere_images.append(image_dict)

hemisphere_images
```




    [{'name': 'Cerberus Hemisphere Enhanced',
      'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
     {'name': 'Schiaparelli Hemisphere Enhanced',
      'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
     {'name': 'Syrtis Major Hemisphere Enhanced',
      'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
     {'name': 'Valles Marineris Hemisphere Enhanced',
      'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]




```python
#convert the notebook to script 
! jupyter nbconvert --to script --template basic mission_to_mars.ipynb --output scrape_mars
```

    [NbConvertApp] Converting notebook mission_to_mars.ipynb to script
    [NbConvertApp] Writing 3493 bytes to scrape_mars.py

