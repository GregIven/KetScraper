import requests
import re
import logging
import time

from bs4 import BeautifulSoup
from pydoc import classname
from urllib.parse import urlparse

logging.basicConfig(filename='sitemap_output.log', encoding='utf-8', level=logging.DEBUG)
# logging.basicConfig(filename='links.log', encoding='utf-8', level=logging.INFO)
# logging.info(site)


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

def parse_list_source(list):
    list_links = []
    for item in list:
        list_links.append(html_parser(item))
    
    return list_links

#This function parses an html page for links
def html_parser(item):
        page = requests.get(item)
        soup = BeautifulSoup(page, 'html.parser')
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
        return links