from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--disable-software-rasterizer")
driver = webdriver.Chrome(options=options)

def sel_invoke(url):
    page_list = []
    driver.get('https://www.google.com/search?q=ketamine+oregon&ei=kLlZYsrYCtWfkPIPoL2g6AU&start=180&sa=N&ved=2ahUKEwjK4OC92Zb3AhXVD0QIHaAeCF04qgEQ8NMDegQIARBL&biw=1396&bih=678&dpr=1.38')
    driver.implicitly_wait(0.5)
    next_page = driver.find_elements(By.CLASS_NAME, value="fl")
    
    print(next_page)

    # while (next_page):
    #     source = driver.page_source
    #     # next_page.click()
    #     page_list.append(source)
    #     driver.implicitly_wait(3)
    
    driver.implicitly_wait(3)
    driver.close()
    return page_list

