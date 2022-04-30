# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()}
    
    # Stop webdriver and return data
    browser.quit()
    return data

# ### Mars News
def mars_news(browser):

    # Visit Mars NASA news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading page 
    browser.is_element_not_present_by_css('div.list_text', wait_time=1)

    # Convert browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:    
        # Add a parent elements to find news title
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save as news title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use parent element to find paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
def featured_image(browser):
    # Visit URL 
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the full image button
    full_image_element = browser.find_by_tag('button')[1]
    full_image_element.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for errors 
    try:
        # Find the relative image url 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Add base url to the img link pulled up
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
 
    return img_url

# ### Mars Facts
def mars_facts():
    # Add try/except for Base errors
    try:    
        # Read html to import table as dataframe and make changes
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of df 
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe back to html, add bootstrap
    return df.to_html()

if __name__ == '__main__':
    #If running a script, print scraped data
    print(scrape_all())


