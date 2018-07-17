from lxml import etree
from scrapy import Spider
class BestDatingReviewsCrawlURL(Spider):
    URLXPATH = ".//dt/div[@class='all_sites_list_a']/a/text()"
    HREFPATH =  ".//dt/div[@class='all_sites_list_a']/a/@href"
    def __init__(self,category):
        self.url_list = []
        self.category = category

    def parsing(self, response):
        return self.crawl(response)

    def crawl(self, response):

        nodes = response.xpath("//div[@class='all_sites_list']/dl").extract()
        for node in nodes:
            root = etree.HTML(node)
            yield response.follow(root.xpath(self.URLXPATH)[0], callback=self.parsing)
