from scrapy import Spider, Request
from lxml import etree

from services.RevexCrawler import RevexCrawler


urlssss = []
class RevexURLCrawler(Spider):
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

        url = response.xpath("//div[@class='detail']/h3/a/@href").extract()
        servicelist = response.xpath("//div[@class='detail']/h3/a/text()").extract()


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = RevexCrawler(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i]+'reviews/', callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        next_page = response.xpath(
                "//ul[@class='page-numbers']/li[@class='next_paginate_link']/a/@href").extract()
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    print(type(next_page_url))
                    print(next_page_url)
                    # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                    yield response.follow(next_page_url, callback=self.parsing)






