from scrapy import Spider, Request
from lxml import etree

from services.SeniorDatingSites import SeniorDatingSites


urlssss = []
class Top20SeniorDatingSitesURLCrawler(Spider):
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

        url = response.xpath("///div[@class='content']/h2[@class='title']/a/@href").extract()
        url1 = response.xpath("//div[@class='content']/ul/li/a/@href").extract()
        servicelist = response.xpath("//div[@class='content']/h2[@class='title']/a/text()").extract()
        servicelist1 = response.xpath("//div[@class='content']/ul/li/a/text()").extract()
        for cont in url1:
            url.append(cont)
        for content in servicelist1:
            servicelist.append(content)



        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = SeniorDatingSites(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        # next_page = response.xpath("//div[@class='masonry-load-more load-more']/a[@class='button']/@data-link").extract()
        # if next_page is not None:
        #     if len(next_page)>0:
        #         next_page_url = "".join(next_page)
        #         if next_page_url and next_page_url.strip():
        #             yield Request(url=next_page_url, callback=self.parsing)
