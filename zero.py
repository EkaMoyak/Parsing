from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import datetime

# Настройки
LOGIN_URL = "https://university.zerocoder.ru/cms/system/login?required=true"
TARGET_URL = "https://university.zerocoder.ru/teach/control/stream/view/id/921295709"
data_set =[
    {"Curs" : 'Программист на Python с нуля с помощью ChatGPT 2.0', "Link" : "https://university.zerocoder.ru/teach/control/stream/view/id/921295699"},
    {"Curs" : 'Курс «Зерокодер на Bubble» 3.0', "Link" : "https://university.zerocoder.ru/teach/control/stream/view/id/889457326"}
]
USERNAME = "Moyeka@gmail.com"
PASSWORD = "Moyeka17101970"

# Инициализация драйвера
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Раскомментируйте для безголового режима

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def get_hw_status(element):
    """Получаем статус ДЗ через вычисление стилей ::after"""
    script = """
    var element = arguments[0];
    return window.getComputedStyle(element, '::after').getPropertyValue('content');
    """
    status = driver.execute_script(script, element)
    return status.strip('"') if status else "Нет данных"


try:
    # Авторизация
    driver.get(LOGIN_URL)

    # Ждем появления формы входа
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Вводим данные
    driver.find_element(By.NAME, "email").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, 'xdgetr6376_1_1_1_1_1_1_1_1_1_1_1').click()

    # Ждем авторизации (проверяем элемент, который появляется после входа)
    time.sleep(10)

    # Переходим на целевую страницу
    driver.get(TARGET_URL)
    time.sleep(3)  # Даем странице загрузиться

    # Создаем CSV файл
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'zero_results_{timestamp}.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)

        for curs_item in data_set:
            # Переходим на целевую страницу
            driver.get(curs_item["Link"])
            time.sleep(3)  # Даем странице загрузиться


            writer.writerow(['курс:', curs_item["Curs"], curs_item["Link"]])
            writer.writerow(['Урок', 'Статус ДЗ', 'URL'])
            #парсим модули курса

            # Находим все элементы <a> внутри таблицы
            links = driver.find_elements(By.CSS_SELECTOR, "table.stream-table tr.training-row a")

            # Извлекаем href из каждого элемента
            modules = [link.get_attribute("href") for link in links]

            for module in modules:
                print(module)
                driver.get(module)

                # Парсим уроки
                lessons = driver.find_elements(By.CSS_SELECTOR, "div.vmiddle")
                for lesson in lessons:
                    try:
                        # Извлекаем данные
                        title = lesson.find_element(By.CSS_SELECTOR, "div.link.title").text
                        url = lesson.find_element(By.CSS_SELECTOR, "div.link.title").get_attribute("href")

                        # Статус ДЗ через ::after
                        hw_status = get_hw_status(lesson)

                        # Записываем в CSV
                        writer.writerow([title,  hw_status, url])
                        print(f"Добавлено: {title} | ДЗ: {hw_status}")

                    except Exception as e:
                        print(f"Ошибка при обработке элемента: {e}")
                        continue

finally:
    driver.quit()
    print("Парсинг завершен. Результаты сохранены в", filename)