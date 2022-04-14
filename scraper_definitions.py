import requests
import re
import logging
import time

from bs4 import BeautifulSoup
from pydoc import classname
from urllib.parse import urlparse
from Selenium_test import sel_invoke

def parse_keywords_from_page(URL):
    page = requests.get(URL)

    soup_page = BeautifulSoup(page.content, "html.parser")

    results = soup_page.select("body")

    for tags in results:
        char_map = {
        ord('\n') : ' ',
        ord('\t') : None,
    }

    cleaned_tag_list = tags.text.translate(char_map).split('  ')

    true_strings = []

    for word in cleaned_tag_list:
        if len(word) > 0:
            true_strings.append(word)
    # print(true_strings)

    return true_strings


def get_sitemap(URL):
    SITEMAP = URL + 'sitemap.xml'
    sitemap = requests.get(SITEMAP)
    soup_sitemap = BeautifulSoup(sitemap.content, "lxml-xml")

    return soup_sitemap

def get_sitemap_type(xml):
    siteMapIndex = xml.find_all('sitemapindex')
    siteMap = xml.find_all('urlset')

    if siteMapIndex:
        return 'sitemapindex'
    elif siteMap:
        return 'urlset'
    else:
        return


#TODO check if the html has a locations/team/contact form on the home page
#TODO see also if there is a profile/directory of providers
#TODO the doctors/providers can be identified by a title/certification
#TODO look for href to tel/mailto

def get_child_sitemaps(xml):
    def get_relevant_links(site):
        # logging.basicConfig(filename='links.log', encoding='utf-8', level=logging.INFO)
        # logging.info(site)

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

def get_google_results(term):
    logging.basicConfig(filename='google_links.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('yoy')
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term
    source = sel_invoke(current_term)

    soup = BeautifulSoup(source, 'html.parser')

    sub_results = soup.find(id="search")
    all_a_tags = sub_results.find_all('a')
    links = []

    for link in all_a_tags:
        if link.has_attr('href'):
            url = re.search(r'(https?://\S+)', link['href'])
            if url:
                url_parsed = urlparse(url.group(0))
                if url_parsed.netloc not in links:
                    links.append(url_parsed.netloc)


    print(links)

    return None