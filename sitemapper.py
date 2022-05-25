import logging
import re
import json
import sys
from wsgiref import headers
import requests_cache
import requests

from bs4 import BeautifulSoup
from types import NoneType



logging.basicConfig(filename='sitemap_output.log', encoding='utf-8', level=logging.DEBUG)
session = requests_cache.CachedSession()

def individual_site_mapper(sitemaps):
    output = []
    for sitemap in sitemaps:
        if get_relevant_links(sitemap):
            output.append(sitemap.text)
    return output

def get_relevant_links(site):
    keyword_filter = ["conta", "about", "location", "provider", "meet", 
        "mission", "team", "who"] 
    keyword_hits = re.findall('|'.join(keyword_filter), str(site))

    if keyword_hits:
        return site
    else:
        return None


def get_sitemap(URL):
    #uses requests to grab an xml file of all linked pages to main/landing page
    contains_HTTPS = re.findall(r'http', URL)
    if (not contains_HTTPS):
        URL = 'https://' + URL

    try:
        response = session.get(URL, headers={'Accept': 'application/json','User-Agent': 'Chrome/42.0.2311.135'})
        if (response.status_code == 200):
            SITEMAP = URL + '/sitemap.xml'
    except requests.HTTPError as err:
        print(err)
        pass
    else:
        print('response code not 200, its: {}'.format(response.status_code))

    try:
        response = session.get(SITEMAP, headers={'Accept': 'application/json','User-Agent': 'Chrome/42.0.2311.135'})
        sitemap_souped = BeautifulSoup(response.text, 'lxml-xml')
        
        if response.status_code == 301 or response.status_code == 443 or response.status_code == 404:
            print('status code: {}'.format(response.status_code))
            sys.exit(1)

        logging.debug(sitemap_souped)
        return sitemap_souped
   
    except requests.HTTPError as err:
        print('HTTPError: {}, original url: {}'.format(err.code, URL))
        return None
    except AttributeError as err:
        print('error: {}'.format(err))

def get_child_sitemaps(xml):
    print(type(xml))
    x=input()
    print(xml.find_all("loc"))
    x=input()


    sitemaps = []
    sitemaps = xml.find_all("loc")
    sitemap_link_hits = individual_site_mapper(sitemaps)
 

    # print(len(sitemap_link_hits))

    if (len(sitemap_link_hits) < 1):
        print('FIRST 275 CHARS OF SITEMAP')
        print(xml[0:275])
        x=input()
    return sitemap_link_hits

def get_sitemap_type(xml):
    siteMapIndex = xml.find_all('sitemapindex')
    siteMap = xml.find_all('urlset')

    if siteMapIndex:
        return 'sitemapindex'
    elif siteMap:
        return 'urlset'
    else:
        return

