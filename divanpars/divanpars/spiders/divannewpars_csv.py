import scrapy
from scrapy.crawler import CrawlerProcess
import csv
from datetime import datetime


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def __init__(self):
        super().__init__()
        # Создаем файл и записываем заголовки при инициализации паука
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f'divan_results_{timestamp}.csv'
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'URL'])

    def parse(self, response):
        divans = response.css('div.WdR1o')
        for divan in divans:
            block_info = divan.css('div.lsooF')
            name = block_info.css('a span::text').get()
            price = block_info.css('div.pY3d2 span::text').get()
            url = block_info.css('a').attrib['href']

            # Записываем данные в CSV
            with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, price, url])

            # Также возвращаем данные как item (опционально)
            yield {
                'name': name,
                'price': price,
                'url': url
            }


# Настройки и запуск паука
process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'LOG_LEVEL': 'INFO',  # Уменьшаем уровень логгирования
    'FEED_FORMAT': 'csv',  # Дополнительный экспорт в CSV через Scrapy
    'FEED_URI': 'divan_export.csv'  # Файл будет создан автоматически
})

process.crawl(DivannewparsSpider)
process.start()