import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree



# class QuotesSpider(scrapy.Spider):
#     name = 'quotes'
#     start_urls = ['http://quotes.toscrape.com/page/1/',]
#
#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 #'text': quote.css('span.text::text').extract_first(),
#                 'author': quote.css('span small::text').extract_first(),
#                 #'tags': quote.css('div.tags a.tag::text').extract(),
#             }
#
#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             print(type(next_page))
#             print(next_page)
#             yield response.follow(next_page, callback=self.parse)



# if name == '__main__':
#        process = CrawlerProcess(get_project_settings())
#        process.crawl(QuotesSpider)
#        process.start()

class HostadviceSpider(scrapy.Spider):
    name = 'Hostadvice'
    allowed_domains = ['hostadvice.com']
    start_urls = ['https://hostadvice.com/hosting-company/godaddy-reviews/page/2/']

    def parse(self, response):
        authors = response.xpath("//div[@class='review-author']").extract()
        for content in authors:
            root = etree.fromstring(content)
            for element in root:
                for i in (element.xpath("//strong")):
                    print (i.text().encode("utf-8"))

if __name__ == '__main__':
       process = CrawlerProcess(get_project_settings())
       process.crawl(HostadviceSpider)
       process.start()