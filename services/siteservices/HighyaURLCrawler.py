from scrapy import Spider, Request
from lxml import etree

from services.HighYaCrawler import HighYaCrawler


urlssss = []
class HighyaURLCrawler(Spider):
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

        url = response.xpath("//div[@class='sided-mob']/h3[@class='title']/a/@href").extract()
        servicelist = response.xpath("//div[@class='sided-mob']/h3[@class='title']/a/text()").extract()


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            if('reviews' in url[i]):
                crawler = HighYaCrawler(self.category, servicelist[i], url[i])
                # yield Request(url=url[i], callback=crawler.parsing)
                yield response.follow(url=url[i], callback=crawler.parsing)
                # print(url[i][j])
            i=i+1
        #     next_page = response.xpath(
        #         "//div[@id='left_column']/div[@class='navigation']/div[@class='paginator_next']/span/a[@class='button outline']/@href").extract()
        # if next_page is not None:
        #     next_page_url = "".join(next_page)
        #     if next_page_url and next_page_url.strip():
        #         print(type(next_page_url))
        #         print(next_page_url)
        #         # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        #         yield response.follow(next_page_url, callback=self.parsing)






