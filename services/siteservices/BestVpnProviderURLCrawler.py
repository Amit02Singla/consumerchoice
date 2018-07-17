from scrapy import Spider, Request
from lxml import etree

from services.BestVPNProvidersCrawler import BestVPNProvidersCrawler


urlssss = []
class BestVpnProviderURLCrawler(Spider):
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

        url = response.xpath("//div/div[@class='columngrid-4 pad-top']/a[2]/@href").extract()

        for content in url:
            c= content.split('/')
            servicelist.append(c[len(c)-2])


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = BestVPNProvidersCrawler(self.category, servicelist[i], url[i])
            # yield Request(url=url[i], callback=crawler.parsing)
            yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        # next_page = response.xpath("//div[@class='masonry-load-more load-more']/a[@class='button']/@data-link").extract()
        # if next_page is not None:
        #     if len(next_page)>0:
        #         next_page_url = "".join(next_page)
        #         if next_page_url and next_page_url.strip():
        #             yield Request(url=next_page_url, callback=self.parsing)
