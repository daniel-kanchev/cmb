import scrapy
from cmb.items import Article
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime


class CmmbSpider(scrapy.Spider):
    name = 'cmmb'
    allowed_domains = ['cmb.ro']
    start_urls = ['https://www.cmb.ro/category/noutati/anunturi/']

    def parse(self, response):
        articles = response.xpath("//article")
        for article in articles:
            link = article.xpath(".//a[@class='elementor-post__read-more']/@href").get()
            date = article.xpath(".//span[@class='elementor-post-date']//text()").getall()
            yield response.follow(link, self.parse_article, cb_kwargs=dict(date=date))

        next_page = response.xpath("//a[@class='page-numbers next']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response, date):
        title = response.xpath("//h1[@class='elementor-heading-title elementor-size-default']//text()").get()

        content = response.xpath("//section[@class='elementor-section elementor-top-section elementor-element "
                                 "elementor-element-71f6384 elementor-section-boxed elementor-section-height-default "
                                 "elementor-section-height-default']//text()").getall()
        content = [text for text in content if text.strip()]
        content = " ".join(content)

        date = format_date(date[0].strip())

        item = ItemLoader(Article(), response)
        item.default_output_processor = TakeFirst()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('content', content)
        item.add_value('link', response.url)

        return item.load_item()


def format_date(date):
    date_dict = {
        "ianuarie": "January",
        "februarie": "February",
        "martie": "March",
        "aprilie": "April",
        "mai": "May",
        "iunie": "June",
        "iulie": "July",
        "august": "August",
        "septembrie": "September",
        "octombrie": "October",
        "noiembrie": "November",
        "decembrie": "December",
    }

    date = date.split(" ")
    date[1] = date[1][:-1]
    for key in date_dict.keys():
        if date[0] == key:
            date[0] = date_dict[key]
    date = " ".join(date)
    date_time_obj = datetime.strptime(date, '%B %d %Y')
    date = date_time_obj.strftime("%Y/%m/%d")
    return date
