import logging
import re
import json
from wsgiref import headers
import requests_cache
import requests

from bs4 import BeautifulSoup
from types import NoneType



logging.basicConfig(filename='sitemap_output.log', encoding='utf-8', level=logging.DEBUG)
session = requests_cache.CachedSession()


def get_sitemap(URL):
    #uses requests to grab an xml file of all linked pages to main/landing page
    contains_HTTPS = re.findall(r'http', URL)
    if (not contains_HTTPS):
        URL = 'https://' + URL

    SITEMAP = URL + '/sitemap.xml'
    try:
        # sitemap_req = Request(SITEMAP, headers={'User-Agent': 'Mozilla/5.0'})
        # sitemap_decoded = urlopen(sitemap_req).read().decode('utf-8')
        response = session.get(SITEMAP, headers={'Accept': 'application/json','User-Agent': 'Chrome/42.0.2311.135'})
        sitemap_souped = BeautifulSoup(response.text, 'lxml-xml')
        logging.debug(sitemap_souped)
        # x=input()
   
    except requests.HTTPError as err:
        print('HTTPError: {}, original url: {}'.format(err.code, URL))
        return None
    except AttributeError as err:
        print('error: {}'.format(err))
    else:
        #code 200
        return sitemap_souped

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
