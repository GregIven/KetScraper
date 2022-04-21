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
    all_page_links = html_parser(link)
    print('{} as main link'.format(all_page_links))
    return None

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
        print(soup_sitemap_pretty[0:50])
        # print('len on soup: {}'.format(soup_sitemap))
        return soup_sitemap
    except ConnectionError as err:
        print('{} is the error'.format(err))
        return None

    

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
    logging.basicConfig(filename='google_links.log', encoding='utf-8', level=logging.DEBUG)
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term

    #sel_invoke generates list of links per page of google search
    html_source_page_list = sel_invoke(current_term)

    #takes list of html sources, parses for href's and returns links
    compiled_link_list = parse_list_source(html_source_page_list)

    list_hits = []
    #goes through lists of links and grabs the sitemap
    #if no sitemap found, manually traverses the page for links
    #then with the sitemap retrieved, gets all URLs that match keywords
    for page in compiled_link_list:
        print('list of links: {}'.format(page))
        for link in page:
            xml_sitemap = get_sitemap(link)
            if (xml_sitemap):          
                list_hits.append(get_child_sitemaps(xml_sitemap))
            elif (not xml_sitemap):
                print('no site map')
                list_hits.append(manual_link_parse(link))
            # sitemap_type = get_sitemap_type(xml_sitemap)
            
    
    #list_hits is a list of interal pages for each page in a list returned by a google
    # search per term
    return list_hits

def parse_list_source(list):

    list_links = []
    for item in list:
        list_links.append(html_parser(item))
    
    return list_links

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