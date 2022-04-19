import logging
from scraper_definitions import *

# logging.basicConfig(filename='scrapeOutput.log', encoding='utf-8', level=logging.DEBUG)

results_of_search = get_google_results('ketamine oregon')

print(results_of_search)

##TODO - is here to check what kind of sitemap the URL has.
# if sitemap_type == 'sitemapindex':
#     all_child_urls = get_child_sitemaps(xml_sitemap)
# else:
#     all_child_urls = [xml_sitemap]

# print(all_child_urls)
