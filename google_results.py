from Selenium_test import sel_invoke
from sitemapper import *

def get_google_results(term):    
    list_hits = []
    list_of_links = []
    #This func takes a term and appends it to a google search
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term
    
    #Returns list of href links from a google page search result
    google_result_list = sel_invoke(current_term)

    #parses multiple pages as a list of lists
    for page in google_result_list:
        #for href link on a page, return sitemap and then append xml sitemap
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