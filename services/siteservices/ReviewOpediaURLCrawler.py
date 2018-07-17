from scrapy import Spider, Request
from lxml import etree

from services.ReviewOpedia import ReviewOpedia


urlssss = []
class ReviewOpediaURLCrawler(Spider):
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
        url = response.xpath("//div[@class='item-info-text']/a[@class='item-title']/@href").extract()
        serviceList = response.xpath("//div[@class='item-info-text']/a[@class='item-title']/text()").extract()
        i=0
        while i < len(serviceList):
            servicelist.append(serviceList[i].strip())
            i = i+1


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = ReviewOpedia(self.category, servicelist[i], url[i])
            # yield Request(url=url[i], callback=crawler.parsing)
            yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        next_page = response.xpath(
                "//div[@class='pagination']/div[@id='next-last']/a[@id='pagin-next']/@href").extract()
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    print(type(next_page_url))
                    print(next_page_url)
                    # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                    yield response.follow(next_page_url, callback=self.parsing)






