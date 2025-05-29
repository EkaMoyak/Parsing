import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


# 1. Гистограмма для нормального распределения
def task1():
    # Параметры нормального распределения
    mean = 0  # Среднее значение
    std_dev = 1  # Стандартное отклонение
    num_samples = 1000  # Количество образцов

    # Генерация случайных чисел
    data = np.random.normal(mean, std_dev, num_samples)

    # Построение гистограммы
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
    plt.title('Гистограмма нормального распределения')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()


# 2. Диаграмма рассеяния для случайных данных
def task2():
    # Генерация двух наборов случайных данных
    x = np.random.rand(50)
    y = np.random.rand(50)

    # Построение диаграммы рассеяния
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', alpha=0.6)
    plt.title('Диаграмма рассеяния для случайных данных')
    plt.xlabel('X значения')
    plt.ylabel('Y значения')
    plt.grid(True)
    plt.show()


# 3. Парсинг цен с divan.ru и анализ данных
def task3():

    driver = webdriver.Chrome()

    try:
        # Открываем страницу с диванами
        url = "https://www.divan.ru/category/sadovaya-mebel"
        driver.get(url)

        # Ждем загрузки страницы
        time.sleep(5)

        # Прокрутка для загрузки всех товаров
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Парсинг данных
        products = driver.find_elements(By.CSS_SELECTOR, "div.lsooF")
        prices = []

        for product in products:
            try:
                # Извлекаем имя товара
                name = product.find_element(By.CSS_SELECTOR, "a span[itemprop='name']").text

                # Извлекаем блок с ценами
                price_container = product.find_element(By.CSS_SELECTOR, "div.q5Uds")

                # Текущая цена (первый элемент с data-testid="price")
                current_price_element = price_container.find_elements(By.CSS_SELECTOR, "span[data-testid='price']")[0]
                current_price = current_price_element.text.replace(' ', '').replace('₽', '').replace('руб.', '')

                # Старая цена (второй элемент с data-testid="price"), если есть
                old_price = None
                price_elements = price_container.find_elements(By.CSS_SELECTOR, "span[data-testid='price']")
                if len(price_elements) > 1:
                    old_price_element = price_elements[1]
                    old_price = old_price_element.text.replace(' ', '').replace('₽', '').replace('руб.', '')

                prices.append({
                    'name': name,
                    'current_price': int(current_price),
                    'old_price': int(old_price) if old_price else None
                })
            except Exception as e:
                print(f"Ошибка при парсинге товара: {e}")
                continue

        import csv

        # ... ваш код парсинга ...

        # Сохранение в CSV
        with open('divan_prices.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Product Name', 'Current Price', 'Old Price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for item in prices:
                writer.writerow({
                    'Product Name': item['name'],
                    'Current Price': item['current_price'],
                    'Old Price': item['old_price'] if item['old_price'] is not None else ''
                })

        # # Анализ данных
        # if prices:
        #     df = pd.DataFrame(prices, columns=['Price'])
        #     average_price = df['Price'].mean()
        #     print(f"Средняя цена на диваны: {average_price:.2f} руб.")
        #
        #     # Гистограмма цен
        #     plt.figure(figsize=(10, 6))
        #     plt.hist(df['Price'], bins=20, edgecolor='black', alpha=0.7)
        #     plt.title('Распределение цен на диваны')
        #     plt.xlabel('Цена (руб)')
        #     plt.ylabel('Количество')
        #     plt.grid(True)
        #     plt.show()
        # else:
        #     print("Не удалось получить цены")

    except Exception as ex:
        print(f"Ошибка: {ex}")
    finally:
        driver.quit()


import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def analyze_prices(csv_file):
    # Чтение данных из CSV
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Файл {csv_file} не найден!")
        return

    # Основной анализ
    print("\n=== Анализ цен ===")
    print(f"Всего товаров: {len(df)}")

    # Анализ текущих цен
    current_prices = df['Current Price'].dropna()
    print(f"\nСредняя текущая цена: {current_prices.mean():.2f} руб.")
    print(f"Минимальная цена: {current_prices.min()} руб.")
    print(f"Максимальная цена: {current_prices.max()} руб.")
    print(f"Медианная цена: {current_prices.median()} руб.")

    # Анализ скидок (если есть данные о старых ценах)
    if 'Old Price' in df.columns and not df['Old Price'].isnull().all():
        discount_df = df.dropna(subset=['Old Price'])
        discount_df['Discount'] = ((discount_df['Old Price'] - discount_df['Current Price']) /
                                   discount_df['Old Price'] * 100)

        print(f"\nТоваров со скидкой: {len(discount_df)}")
        print(f"Средний размер скидки: {discount_df['Discount'].mean():.1f}%")
        print(f"Максимальная скидка: {discount_df['Discount'].max():.1f}%")

    # Построение гистограммы
    plt.figure(figsize=(12, 6))

    # Гистограмма текущих цен
    plt.subplot(1, 2, 1)
    bins = np.linspace(current_prices.min(), current_prices.max(), 20)
    plt.hist(current_prices, bins=bins, edgecolor='black', alpha=0.7)
    plt.title('Распределение текущих цен')
    plt.xlabel('Цена (руб)')
    plt.ylabel('Количество товаров')
    plt.grid(True)

    # Гистограмма скидок (если есть данные)
    if 'Old Price' in df.columns and not df['Old Price'].isnull().all():
        plt.subplot(1, 2, 2)
        plt.hist(discount_df['Discount'], bins=20, edgecolor='black', color='orange', alpha=0.7)
        plt.title('Распределение размеров скидок')
        plt.xlabel('Размер скидки (%)')
        plt.ylabel('Количество товаров')
        plt.grid(True)

    plt.tight_layout()
    plt.show()




# Выполнение всех задач
if __name__ == "__main__":
    print("Задача 1: Гистограмма нормального распределения")
    task1()

    print("\nЗадача 2: Диаграмма рассеяния случайных данных")
    task2()

    print("\nЗадача 3: Парсинг цен на диваны с divan.ru")
    task3()

    print("\nЗадача 3`: Анализ цен на товары")
    analyze_prices('divan_prices.csv')