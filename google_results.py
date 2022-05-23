from Selenium_test import sel_invoke
from sitemapper import *

def get_google_results(term):    
    list_of_sitemaps = []
    list_of_links = []
    #This func takes a term and appends it to a google search
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term
    
    #Returns list of href links from a google page search result
    result_pages = sel_invoke(current_term)

    #parses multiple pages as a list of lists
    for page in result_pages:
        #for href link on a page, return sitemap and then append xml sitemap
        for link in page:
            xml_sitemap = get_sitemap(link["redir"])
            list_of_sitemaps.append(xml_sitemap)
    
    for xml_doc in list_of_sitemaps:
        if (xml_doc is not None):
            list_of_links = get_child_sitemaps(xml_doc)
    
    print('list of hits: {}, pages link scraped: {}'.format(len(list_of_sitemaps), len(list_of_links)))
    #list_of_sitemaps is a list of interal pages for each page in a list returned by a google
    # search per term
    return None