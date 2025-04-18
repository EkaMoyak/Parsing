import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["https://divan.ru"]
    # start_urls = ["https://www.divan.ru/category/divany-i-kresla"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        divans = response.css('div.WdR1o')
        for divan in divans:
            block_info = divan.css('div.lsooF')
            name = block_info.css('a span::text').get()
            price = block_info.css('div.pY3d2 span::text').get()
            url = block_info.css('a').attrib['href']
            yield {
                'name' : name,
                'price' : price,
                'url' : url
            }