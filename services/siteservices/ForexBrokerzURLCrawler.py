from scrapy import Spider, Request
from lxml import etree

from services.ForexbrokerzCrawler import ForexbrokerzCrawler


urlssss = []
class ForexbrokerzCrawlerURLCrawler(Spider):
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response)
    def crawl(self, response):
        url = []
        urlnext = []
        servicelistnext = []
        servicelist= []

        url = response.xpath("//td[@class='last']/a[@class='review_btn']/@href").extract()
        servicelist = response.xpath("//a[@class='broker_logo']/@title").extract()

        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = ForexbrokerzCrawler(self.category, servicelist[i], url[i])
            # yield Request(url=url[i], callback=crawler.parsing)
            yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        next_page = response.xpath("//a[@class='frtn']/@href").extract()
        if (len(next_page) > 0):
            if 'page' not in response.url:
                print next_page
            else:
                next_page = response.xpath("//a[@class='frtn'][2]/@href").extract()
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    yield response.follow(url=next_page_url, callback=self.parsing)
                    # yield Request(url=next_page_url, callback=self.parsing)
