from email import header
import re
from urllib.parse import urlparse
import requests


site = "meet moment at the providers locations"
keyword_filter = ["contact", "about", "location", "provider", "meet", 
            "mission", "team", "who"]
keyword_hits = []
header_filter = ["header", "links", "title", "navigation"]

# URL = 'https://portlandketamineclinic.com'
# SITEMAP = URL + '/sitemap.xml'
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
# page = requests.get(SITEMAP, headers=headers)
# find_www = re.findall(r'w{3}', URL)
# find_https = re.findall(r'http', URL)

# print('found https?: {}, found www?: {} '.format(find_https,find_www))

string1 = 'https://policies.gogle.com'

print('google' not in string1)

page = requests.get('https://portlandketamineclinic.com/sitemap.xml')

# print(page.status_code)
# with open('links.log') as links:
#     lines = links.readlines()

# links.close()
