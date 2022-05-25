from Selenium_test import sel_invoke
from sitemapper import *
import itertools

def get_google_results(term):    
    #This func takes a term and appends it to a google search
    GOOGLE_URL = 'https://www.google.com/search?q='
    current_term = GOOGLE_URL + term
    
    #Returns list of href links from a google page search result
    result_pages = sel_invoke(current_term)

    #for href link on a page, return sitemap and then append xml sitemap
    list1 = gen_list_of_sitemaps(result_pages)

    list2 = gen_list_of_sitemap_target_links(list1)

    
    print('list of hits: {}, pages link scraped: {}'.format(len(list1), len(list2)))
    #list_of_sitemaps is a list of interal pages for each page in a list returned by a google
    # search per term
    return None

def gen_list_of_sitemaps(google_results):
    list_of_sitemaps = []

    temp_slice = dict(itertools.islice(google_results, 3))

    for result in temp_slice:
            xml_sitemap = get_sitemap(result)
            list_of_sitemaps.append(xml_sitemap)
    
    return list_of_sitemaps

def gen_list_of_sitemap_target_links(sitemaps):
    list_of_links = []

    for xml_doc in sitemaps:
        if (xml_doc is not None):
            list_of_links = get_child_sitemaps(xml_doc)

    return list_of_links