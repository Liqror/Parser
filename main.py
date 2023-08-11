from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ebooklib import epub
import undetected_chromedriver as uc


options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# browser = uc.Chrome(options=options)
browser = uc.Chrome(headless=False,use_subprocess=True, options=options)

# browser = webdriver.Chrome()
# browser.delete_all_cookies()
book_url = 'https://ficbook.net/readfic/10684982'
browser.get(book_url)

wait = WebDriverWait(browser, 35)
title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.mb-10")))

# title = browser.find_element(By.CSS_SELECTOR, "h1.mb-10")
book = epub.EpubBook()
book.set_title(title.text)
book.set_language("ru")

chapter_links = browser.find_elements(By.CLASS_NAME, "part")
# Перебираем ссылки на главы
for index in range(len(chapter_links)):
    chapter_links = browser.find_elements(By.CLASS_NAME, "part")
    chapter_title = chapter_links[index].find_element(By.CSS_SELECTOR, "h3").text

    # Переходим на страницу главы
    browser.delete_all_cookies()
    chapter_links[index].click()

    # Ожидание, пока элемент с id "content" станет видимым
    wait = WebDriverWait(browser, 5)
    chapter_text_element = wait.until(EC.visibility_of_element_located((By.ID, "content")))

    # Находим элемент с текстом главы и извлекаем текст
    # вот тут можно доработать потому что все форматирование уезжает
    chapter_text = chapter_text_element.text

    # Создаем объект главы EPUB
    chapter = epub.EpubHtml(title=chapter_title, file_name=f"chap_{index}.xhtml", lang="ru")
    chapter.set_content(f"<h1>{chapter_title}</h1><br><p>{chapter_text}</p>")
    book.add_item(chapter)
    book.spine.append(chapter)

    browser.back()

# Создаем EPUB-файл
epub.write_epub("2.epub", book, {})
