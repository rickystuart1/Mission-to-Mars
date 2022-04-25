# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit Mars NASA news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading page 
browser.is_element_not_present_by_css('div.list_text', wait_time=1)

# Convert browser html to a soup object
html = browser.html
news_soup = soup(html, 'html.parser')

# Add a parent elements to find news title
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save as news title
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use parent element to find paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# Visit URL 
url = 'https://spaceimages-mars.com/'
browser.visit(url)

# Find and click the full image button
full_image_element = browser.find_by_tag('button')[1]
full_image_element.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url 
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Add base url to the img link pulled up
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts

# Read html to import table as dataframe and make changes
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

# Convert dataframe back to html
df.to_html

# Quit browser to keep it from running in the background
browser.quit()




