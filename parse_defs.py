from wsgiref import headers
import re
import logging
import time
import requests_cache
import requests

from bs4 import BeautifulSoup
from pydoc import classname
from urllib.parse import urlparse


logging.basicConfig(filename='sitemap_output.log', encoding='utf-8', level=logging.DEBUG)
# logging.basicConfig(filename='links.log', encoding='utf-8', level=logging.INFO)

session = requests_cache.CachedSession()

#TODO remove the requests/bs4 parsing from this def, it should just get passed a html page
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

#TODO check if the html has a locations/team/contact form on the home page
#TODO see also if there is a profile/directory of providers
#TODO the doctors/providers can be identified by a title/certification
#TODO look for href to tel/mailto

#This function parses an html page for links
def html_parser(item):
    
    response = session.get(item, headers={'Accept': 'application/json','User-Agent': 'Chrome/42.0.2311.135'})

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.HTTPError as err:
        print('{} is the error'.format(err))
        pass
        
        

def parse_page_results(page):
    if (page is None):
        pass

    all_a_tags = page.find_all('a')
    links = []

    for link in all_a_tags:
        if link.has_attr('href'):
            url = re.search(r'(https?://\S+)', link['href'])
            if url:
                url_parsed = urlparse(url.group(0))
                #urlparse returns an object that is the url broken apart
                if url_parsed.netloc not in links:
                    if (not bool(re.search(r'\bgoogle\b', url_parsed.netloc))):
                        links.append(url_parsed.netloc)
    return links