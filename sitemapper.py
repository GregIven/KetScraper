import requests
import logging
import re
from bs4 import BeautifulSoup


logging.basicConfig(filename='sitemap_output.log', encoding='utf-8', level=logging.DEBUG)
# logging.basicConfig(filename='links.log', encoding='utf-8', level=logging.INFO)
# logging.info(site)

def get_sitemap(URL):
    #uses requests to grab an xml file of all linked pages to main/landing page
    contains_HTTPS = re.findall(r'http', URL)
    # print('URL1: {}'.format(URL))
    if (not contains_HTTPS):
        URL = 'https://' + URL

    SITEMAP = URL + '/sitemap.xml'
    # print('URL2: {}'.format(URL))

    try:
        print('tried, sitemap: {}'.format(SITEMAP))
        sitemap = requests.get(SITEMAP)
        soup_sitemap = BeautifulSoup(sitemap.content, "lxml-xml")
        soup_sitemap_pretty = soup_sitemap.prettify()
        print(soup_sitemap_pretty[0:250])
        logging.debug(soup_sitemap_pretty[0:250])
        # print('len on soup: {}'.format(soup_sitemap))
        return soup_sitemap
    except ConnectionError as err:
        print('{} is the error'.format(err))
        return None

def get_child_sitemaps(xml):
    def get_relevant_links(site):
        keyword_filter = ["conta", "about", "location", "provider", "meet", 
            "mission", "team", "who"] 
        keyword_hits = re.findall('|'.join(keyword_filter), str(site))

        if keyword_hits:
            return site
        
    sitemaps = xml.find_all("loc")

    output = []
    
    for sitemap in sitemaps:
        if get_relevant_links(sitemap):
            output.append(sitemap.text)
    return output

def get_sitemap_type(xml):
    siteMapIndex = xml.find_all('sitemapindex')
    siteMap = xml.find_all('urlset')

    if siteMapIndex:
        return 'sitemapindex'
    elif siteMap:
        return 'urlset'
    else:
        return