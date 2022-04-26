from lib2to3.pgen2 import driver
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

page = requests.get("https://www.advancingsurgicalcare.com/asc/findanasc")
soup = BeautifulSoup(page)

driver = webdriver.Chrome()
driver.get(page)

driver.find_elements(By.ID, value="state")


