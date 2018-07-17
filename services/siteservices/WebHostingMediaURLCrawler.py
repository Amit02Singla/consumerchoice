from scrapy import Spider, Request
from lxml import etree

from services.webHostingmedia import webHostingmedia


urlssss = []
class WebHostingMediaURLCrawler(Spider):
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

        url = response.xpath("//div[@class='the-content']/h2[@class='title']/a/@href").extract()
        serviceList = response.xpath("//div[@class='the-content']/h2[@class='title']/a/text()").extract()
        for content in serviceList:
            servicelist.append(content.strip())



        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = webHostingmedia(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        next_page = response.xpath("//div[@id='nav-below']/div[@class='blog-pagination']/a[5]/@href").extract()
        if (len(next_page) > 0):
            if 'page' not in response.url:
                print next_page
            else:
                next_page = response.xpath("//div[@id='nav-below']/div[@class='blog-pagination']/a[7]/@href").extract()
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    yield Request(url=next_page_url, callback=self.parsing)
