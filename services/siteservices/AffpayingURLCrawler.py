from scrapy import Spider, Request
from lxml import etree

from services.affPaying import affPaying


urlssss = []
class AffPayingURLCrawler(Spider):
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

        url = response.xpath("//div[@class='title']/div[@class='title-right']/h2/a/@href").extract()
        servicelist = response.xpath("//div[@class='title']/div[@class='title-right']/h2/a/text()").extract()


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = affPaying(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i]+'reviews/', callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
