from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import time

options = webdriver.ChromeOptions()
# options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

def sel_invoke(url):
    driver.get(url)
    source = driver.page_source
    driver.close()
    return source