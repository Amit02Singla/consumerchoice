from scrapy import Spider, Request
from lxml import etree
from product.amazon.helpers import make_request
from services.BestBitcoinExchange import BestBitcoinExchange


urlssss = []
class BestBitcoinExchangeURLCrawler():
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response)
    def crawl(self, response):

        servicelist= []
        root = etree.HTML(response)
        url = root.xpath(".//div[@class='entry overview provider']/a[@class='title']/@href")
        serviceList = root.xpath(".//div[@class='entry overview provider']/a[@class='title']/text()")
        for content in serviceList:
            c= content.split(' ')
            servicelist.append(c[0])



        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = BestBitcoinExchange(self.category, servicelist[i], url[i])
            r = make_request(url[i], False, False)
            crawler.crawl(r.content)
            i=i+1
        next_page = root.xpath(".//nav[@class='navi postnavi']/div[@class='next']/a/@href")
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    r = make_request(next_page_url, False, False)
                    self.crawl(r.content)
