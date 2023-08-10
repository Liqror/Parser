from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from ebooklib import epub

browser = webdriver.Chrome()

book_url = 'https://ficbook.net/readfic/10684982'
browser.get(book_url)

time.sleep(50)

title = browser.find_element(By.CSS_SELECTOR, "h1.mb-10")

chapter_links = browser.find_elements(By.CLASS_NAME, "part")

book = epub.EpubBook()
book.set_title("" + title.text)
book.set_language("ru")

# Перебираем ссылки на главы
for index, link in enumerate(chapter_links):
    chapter_title = link.find_element(By.CSS_SELECTOR, "div.part-title h3").text
    chapter_url = link.find_element(By.TAG_NAME, "a").get_attribute("href")

    # Переходим на страницу главы
    browser.get(chapter_url)
    time.sleep(20)

    # Ожидание, пока элемент с id "content" станет видимым
    wait = WebDriverWait(browser, 10)  # Максимальное время ожидания в секундах
    chapter_text_element = wait.until(EC.visibility_of_element_located((By.ID, "content")))

    # Находим элемент с текстом главы и извлекаем текст
    chapter_text_element = browser.find_element(By.ID, "content")
    chapter_text = chapter_text_element.text

    # Создаем объект главы EPUB
    chapter = epub.EpubHtml(title=chapter_title, file_name=f"chap_{index}.xhtml", lang="ru")

    # Добавляем текст главы в объект главы EPUB
    chapter.content = f"<h1>{chapter_title}</h1><br>{chapter_text}".encode("utf-8")
    book.add_item(chapter)
    book.spine.append(chapter)

# Создаем EPUB-файл
epub.write_epub("1.epub", book, {})
