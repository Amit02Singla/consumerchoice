from scrapy import Spider, Request
from lxml import etree

from services.VPNpickCrawler import VPNpickCrawler


urlssss = []
class VpnPickURLCrawler(Spider):
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

        print("url ", response.url)
        ur = response.url.split('/?s=')
        next = ur[0]+'/page/2/?s='+ur[1]
        print(next)
        url = response.xpath("//header/h2[@class='title front-view-title']/a/@href").extract()
        servicelist = response.xpath("//header/h2[@class='title front-view-title']/a/text()").extract()




        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = VPNpickCrawler(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        # next_page = response.xpath("//div[@class='uk-width-1-1']/ul[@class='uk-pagination']/li[10]/a/@href").extract()
        # if next_page is not None:
        #     if len(next_page)>0:
        #         next_page_url = "".join(next_page)
        #         if next_page_url and next_page_url.strip():
        #             yield Request(url=next_page_url, callback=self.parsing)
