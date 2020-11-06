# Import dependencies 
from splinter import Browser
import pandas as pd
import time

def scrape():

    executable_path = {'executable_path': 'C:\Program Files\Chrome Driver\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    news_title = browser.find_by_xpath('//div[@class="content_title"]/a')[0].text
    news_p = browser.find_by_xpath('//div[@class="article_teaser_body"]')[0].text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    base_img_url = "https://www.jpl.nasa.gov/"
    featured_image_url = base_img_url + browser.find_by_xpath('//article[@class="carousel_item"]')[0]['style'].split('"')[1]

    url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url)[0].to_html()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls_title = browser.find_by_xpath('//h3')
    hemisphere_image_urls_title = [h.text for h in hemisphere_image_urls_title]

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    hemisphere_image_urls = []
    not_tied_to_the_browser = [l['href'] for l in browser.find_by_xpath('//h3/parent::a')]
    for link in not_tied_to_the_browser:
        browser.visit(link)
        time.sleep(1)
        hemisphere_image_urls.append(browser.find_by_xpath('//a[text()="Sample"]')[0]['href'])

    hemisphere_image_urls = [{'title': title, 'img_url': link} for title, link in zip(hemisphere_image_urls_title,hemisphere_image_urls)]

    output = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_facts': mars_facts,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    # quit splinter session
    browser.quit()
    return output
