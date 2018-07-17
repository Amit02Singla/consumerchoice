from scrapy import Spider, Request
from lxml import etree

from services.PickuphostCrawler import PickuphostCrawler


urlssss = []
class PickuphostURLCrawler(Spider):
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

        url = response.xpath("//h3[@class='nomargin text-left table_host_name']/a/@href").extract()
        url1 = response.xpath("//div[@class='wiz1-col3-inner']/div[@class='wiz-links-block']/a/@href").extract()
        servicelist = response.xpath("//h3[@class='nomargin text-left table_host_name']/a/text()").extract()
        serviceList1 = response.xpath("//div[@class='wiz1-header-col1']/div[@class='wiz1-col1-right']/div[@class='wiz1-col1-host-name']/text()").extract()

        i=0
        while i< len(url1):
            a= url1[i].split('#')
            url.append(a[0])
            servicelist.append(serviceList1[i])
            i = i+1;

        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = PickuphostCrawler(self.category, servicelist[i], url[i])
            # yield Request(url=url[i], callback=crawler.parsing)
            yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        # next_page = response.xpath("//div[@class='uk-width-1-1']/ul[@class='uk-pagination']/li[10]/a/@href").extract()
        # if next_page is not None:
        #     if len(next_page)>0:
        #         next_page_url = "".join(next_page)
        #         if next_page_url and next_page_url.strip():
        #             yield Request(url=next_page_url, callback=self.parsing)
