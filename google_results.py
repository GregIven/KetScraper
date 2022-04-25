from scraper_definitions import parse_list_source, get_sitemap, get_child_sitemaps, manual_link_parse
from Selenium_test import sel_invoke

def get_google_results(term):
    #This func takes a term and appends it to a google search
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