import random
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


query = input('Что хотите найти в Wikipedia: ')
browser = webdriver.Chrome()


def search_wikipedia(query):
    """Поиск статьи в Википедии"""
    browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    search_box = browser.find_element(By.ID, "searchInput")

    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    return


def get_paragraphs(one = False):
    """Получение всех параграфов статьи"""
    hatnotes = []
    if one:
        for element in browser.find_elements(By.CLASS_NAME, "searchresult"):
            hatnotes.append(element)
    else:
        for element in browser.find_elements(By.TAG_NAME, "p"):
            hatnotes.append(element)
    return hatnotes



def get_links(one = False):
    """Получение всех внутренних ссылок статьи"""
    links = []
    if one:
        for element in browser.find_elements(By.CLASS_NAME, "mw-search-result-heading"):
            l = element.find_element(By.TAG_NAME, "a")
            links.append(l.get_attribute("href"))

    else:
        for element in browser.find_elements(By.TAG_NAME, "a"):
            links.append(element.get_attribute("href"))
    return links


def display_paragraphs(paragraphs):
    """Постраничный вывод параграфов"""
    for paragraph in paragraphs:
        print(paragraph.text)
        print()
        wq = input("Для продолжения нажмите д/н...")
        if wq != "д":
            break


def main():
    search_wikipedia(query)
    paragraphs = get_paragraphs(True)
    links = get_links(True)

    while True:

        # Шаг 3: Меню действий
        print("\nДоступные действия:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")

        choice = input("Выберите действие (1-3): ")

        if choice == '1':
            # Листать параграфы

            if paragraphs:
                display_paragraphs(paragraphs)
            else:
                print("В статье нет параграфов для отображения.")

        elif choice == '2':
            # Переход на связанные страницы

            if not links:
                print("Нет доступных связанных страниц.")
                continue

            link_choice = random.choice(links)

            browser.get(link_choice)
            print(f"\nПерешли на страницу: {link_choice}")
            paragraphs = get_paragraphs()
            links = get_links()


        elif choice == '3':
            # Выход из программы
            print("Завершение программы...")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите 1, 2 или 3.")

    browser.quit()


if __name__ == "__main__":
    main()