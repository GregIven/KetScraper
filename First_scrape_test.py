import logging
from lxml import etree
from scraper_definitions import *


# Logging section

# logging.basicConfig(filename='scrapeOutput.log', encoding='utf-8', level=logging.DEBUG)

# Scarping section

URL = "https://www.cedarpsychiatry.com/"

all_html_text = []

xml_sitemap = get_sitemap(URL)
sitemap_type = get_sitemap_type(xml_sitemap)
all_child_urls = get_child_sitemaps(xml_sitemap)

get_google_results('ketamine oregon')

##TODO - is here to check what kind of sitemap the URL has.
# if sitemap_type == 'sitemapindex':
#     all_child_urls = get_child_sitemaps(xml_sitemap)
# else:
#     all_child_urls = [xml_sitemap]

# print(all_child_urls)
