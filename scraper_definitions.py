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

def manual_link_parse(link):
    #grabs all a tags with hrefs on a page with no sitemap

    return None

def get_sitemap(URL):
    #uses requests to grab an xml file of all linked pages to main/landing page
    contains_HTTPS = re.findall(r'http', URL)

    if (not contains_HTTPS):
        URL = 'https://' + URL

    print(URL)
    SITEMAP = URL + 'sitemap.xml'
    print(SITEMAP)
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
    #This func takes a term and appends it to a google search
    #sel_invoke returns list of all pages as html list_sources files
    #parse_list_sources takes a list of html pages and parses each page for links that match keywords
    logging.basicConfig(filename='google_links.log', encoding='utf-8', level=logging.DEBUG)
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term

    #sel_invoke retrieves each google search page per terms html source
    # returns a list of html source pages
    list_sources = sel_invoke(current_term)
    #parses each page source returned by a google search for all href links to 
    # pages returned by the search. Returns lists of links
    list_sources_parsed = parse_list_sources(list_sources)

    list_hits = []
    #goes through lists of links and grabs the sitemap
    #if no sitemap found, manually traverses the page for links
    #then with the sitemap retrieved, gets all URLs that match keywords
    for page in list_sources_parsed:
        for link in page:
            xml_sitemap = get_sitemap(link)
            # sitemap_type = get_sitemap_type(xml_sitemap)
            list_child_urls = get_child_sitemaps(xml_sitemap)
            list_hits.append(list_child_urls)
    
    #list_hits is a list of interal pages for each page in a list returned by a google
    # search per term
    return list_hits

def parse_list_sources(list):
    def html_parser(item):
        soup = BeautifulSoup(item, 'html.parser')
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

    list_links = []
    for item in list:
        list_links.append(html_parser(item))
    
    return list_links
