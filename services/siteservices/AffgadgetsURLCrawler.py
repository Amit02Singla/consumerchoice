from scrapy import Spider, Request
from lxml import etree

from services.affgadgetsCrawler import affgadgetsCrawler


urlssss = []
class AffgadgetsURLCrawler(Spider):
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response)
    def crawl(self, response):
        url = []
        urlnext = []
        servicelistnext = []
        serviceList= []

        url = response.xpath("//ul[@class='listings']/li/div[@class='category-box']/a/@href").extract()
        servicelist = response.xpath("//ul[@class='listings']/li/div[@class='category-box']/a/div[@class='cat-website']/div[@class='category-box-title']/text()").extract()


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = affgadgetsCrawler(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i]+'reviews/', callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
