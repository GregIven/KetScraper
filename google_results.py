from scraper_definitions import parse_list_source
from Selenium_test import sel_invoke
from sitemapper import *

def get_google_results(term):
    #This func takes a term and appends it to a google search
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term

    #sel_invoke generates list of links per page of google search
    html_source_page_list = sel_invoke(current_term)

    #takes list of html sources, parses for href's and returns links
    compiled_link_list = parse_list_source(html_source_page_list)

    list_hits = []
    #goes through lists of links from google search and grabs the sitemap
    #if no sitemap found, grabs top level url and searches that page for sitemap/links
    #then with the sitemap retrieved, gets all URLs that match keywords
    for page in compiled_link_list:
        # print('list of links: {}'.format(page))
        for link in page:
            xml_sitemap = get_sitemap(link)
            if (xml_sitemap):          
                list_hits.append(get_child_sitemaps(xml_sitemap))
            
    if (len(list_hits) > 100):
        print('over!')
        return None
    #list_hits is a list of interal pages for each page in a list returned by a google
    # search per term
    return list_hits