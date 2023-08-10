from ebooklib import epub
from main import title, chapter_links
from selenium.webdriver.common.by import By

book = epub.EpubBook()
book.set_title("" + title.text)
book.set_language("ru")


# Перебираем ссылки на главы
for index, link in enumerate(chapter_links):
    chapter_title = link.find_element(By.TAG_NAME, "h3").text
    chapter_url = link.find_element(By.TAG_NAME, "a").get_attribute("href")

    # Создаем объект главы EPUB
    chapter = epub.EpubHtml(title=chapter_title, file_name=f"chap_{index}.xhtml", lang="ru")

    # Добавляем название главы в книгу
    chapter.content = f"<h1>{chapter_title}</h1>".encode("utf-8")
    book.add_item(chapter)
    book.spine.append(chapter)


# Создаем EPUB-файл
epub.write_epub("1.epub", book, {})

