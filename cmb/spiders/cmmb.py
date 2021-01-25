import scrapy


class CmmbSpider(scrapy.Spider):
    name = 'cmmb'
    allowed_domains = ['cmb.ro']
    start_urls = ['https://www.cmb.ro/category/noutati/anunturi/']

    def parse(self, response):
        pass
