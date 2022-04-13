import re
from urllib.parse import urlparse


site = "meet moment at the providers locations"
keyword_filter = ["contact", "about", "location", "provider", "meet", 
            "mission", "team", "who"]
keyword_hits = []
header_filter = ["header", "links", "title", "navigation"]

URL = '/url?q=https://rainfallmedicine.com/ketamine-therapy/&sa=U&ved=2ahUKEwit-Yf344z3AhVmKEQIHSxwAmUQFnoECAkQAg&usg=AOvVaw1yAO5pUwX6q0fM08-4p9a0'

# keyword_hits = re.findall(r"(?=("+'|'.join(keyword_filter)+r"))", str(site))

keyword_hits = re.findall(r'|'.join(keyword_filter), site)

# with open('links.log') as links:
#     lines = links.readlines()

# links.close()


# for item in lines:
#     if (re.findall(r'|'.join(keyword_filter), item)):
#         print(item)

# keyword_hits = re.findall(r'|'.join(keyword_filter), lines)

url = re.search(r'(https?://\S+)', URL)

url_parsed = urlparse(url.group(0))

print(url_parsed.netloc)

# print(urlparse(URL))

#search
