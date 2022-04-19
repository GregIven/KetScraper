import re
from urllib.parse import urlparse


site = "meet moment at the providers locations"
keyword_filter = ["contact", "about", "location", "provider", "meet", 
            "mission", "team", "who"]
keyword_hits = []
header_filter = ["header", "links", "title", "navigation"]

URL = 'https://ww.took.com'

find_www = re.findall(r'w{3}', URL)
find_https = re.findall(r'http', URL)

print('found https?: {}, found www?: {} '.format(find_https,find_www))

# with open('links.log') as links:
#     lines = links.readlines()

# links.close()
