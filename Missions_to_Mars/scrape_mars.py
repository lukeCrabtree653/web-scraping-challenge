from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

marsData = {}

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    newsURL = 'https://redplanetscience.com/'
    browser.visit(newsURL)

    newshtml = browser.html
    newssoup = bs(newshtml, 'html.parser')
    try:
        slideelem = newssoup.select_one('div.list_text')
        newstitle = slideelem.find('div', class_ = 'content_title').get_text()
        newsp = slideelem.find('div', class_ = 'article_teaser_body').get_text()
        marsData['news_title'] = newstitle
        marsData['news_p'] = newsp
    
    except AttributeError:
        marsData['news_title'] = None
        marsData['news_p'] = None
        
    imageURL = 'https://spaceimages-mars.com/'

    browser.visit(imageURL)

    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    all_images = image_soup.find_all('img')

    images = []
    for image in all_images:
        images.append(image['src'])

    base_url = 'https://spaceimages-mars.com/'
    featured_image_url = base_url + images[1]

    marsData['featured_image_url'] = featured_image_url    


    factsURL = 'https://galaxyfacts-mars.com/'

    browser.visit(factsURL)

    tables = pd.read_html(factsURL)

    facts_df = tables[0]

    facts_df.columns = ['Description', 'Mars', 'Earth']
    facts_df.set_index('Description', inplace = True)

    facts_html_table = facts_df.to_html()

    facts_html_table.replace('\n','')

    facts_df.to_html('mars_facts.html')

    marsData['facts_html_table'] = facts_html_table


    hemisphereURL = 'https://marshemispheres.com/'


    browser.visit(hemisphereURL + 'index.html')


    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')

    results = hemisphere_soup.find_all('div', class_ = 'item')


    hemisphereData = []


    baseURL = 'https://marshemispheres.com/'


    for item in results:
        hemisphere_title = item.find('h3').text
        imgURL = item.find('a', class_ = 'itemLink product-item')['href']
        
        browser.visit(baseURL + imgURL)
        
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        
        final_img_url = baseURL + img_soup.find('img', class_ = 'wide-image')['src']
        
        hemisphereData.append({'title': hemisphere_title, 'img_url': final_img_url })
    
    marsData['hemisphere_data'] = hemisphereData

    browser.quit()

    return marsData

print(marsData)