from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.get('https://ficbook.net/readfic/12311968?fragment=part_content')

a = browser.find_element(By.CSS_SELECTOR, "h1.mb-10")

print(a.text)

chapter_links = browser.find_elements(By.CLASS_NAME, "part")

