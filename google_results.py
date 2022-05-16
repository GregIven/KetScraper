from Selenium_test import sel_invoke
from sitemapper import *

def get_google_results(term):    
    list_hits = []
    list_of_links = []
    #This func takes a term and appends it to a google search
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term
    
    #sel_invoke generates list of links per page of google search
    google_result_list = sel_invoke(current_term)

    #goes through lists of links from google search and grabs the sitemap
    #if no sitemap found, grabs top level url and searches that page for sitemap/links
    #then with the sitemap retrieved, gets all URLs that match keywords
    for page in google_result_list:
        for link in page:
            xml_sitemap = get_sitemap(link)
            list_hits.append(xml_sitemap)
    
    for page in list_hits:
        if (page is not None):
            list_of_links = get_child_sitemaps(page)
    
    print('list of hits: {}, pages link scraped: {}'.format(len(list_hits), len(list_of_links)))
    #list_hits is a list of interal pages for each page in a list returned by a google
    # search per term
    return None