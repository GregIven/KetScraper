import requests
import logging
import re
from bs4 import BeautifulSoup

from scraper_definitions import html_parser


logging.basicConfig(filename='sitemap_output.log', encoding='utf-8', level=logging.DEBUG)
# logging.basicConfig(filename='links.log', encoding='utf-8', level=logging.INFO)
# logging.info(site)

def get_sitemap(URL):
    #uses requests to grab an xml file of all linked pages to main/landing page
    contains_HTTPS = re.findall(r'http', URL)
    if (not contains_HTTPS):
        URL = 'https://' + URL

    SITEMAP = URL + '/sitemap.xml'

    try:
        sitemap = requests.get(SITEMAP)
        soup_sitemap = BeautifulSoup(sitemap.content, "lxml-xml")
        if (sitemap.status_code == 200):
            print(sitemap[0:10])
            return soup_sitemap.prettify()
        elif (sitemap.status_code != 200):
            _links = html_parser(URL)
            # print(_links)
        # soup_sitemap_pretty = soup_sitemap.prettify()
        # logging.debug(soup_sitemap_pretty[0:250])
        # print('len on soup: {}'.format(soup_sitemap))
        return soup_sitemap
    except BaseException as err:
        return None

def get_child_sitemaps(xml):
    def get_relevant_links(site):
        keyword_filter = ["conta", "about", "location", "provider", "meet", 
            "mission", "team", "who"] 
        keyword_hits = re.findall('|'.join(keyword_filter), str(site))

        if keyword_hits:
            return site
        
    try:
        sitemaps = xml.find_all("loc")
    except BaseException as err:
        print('no sitemap found')
        pass

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
