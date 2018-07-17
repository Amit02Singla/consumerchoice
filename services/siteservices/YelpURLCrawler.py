from scrapy import Spider, Request
from lxml import etree

from services.yelpCrawler import yelpCrawler


urlssss = []
class YelpURLCrawler(Spider):
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

        url1 = response.xpath("//h3[@class='search-result-title']/span[@class='indexed-biz-name']/a[@class='biz-name js-analytics-click']/@href").extract()
        servicelist = response.xpath("//h3[@class='search-result-title']/span[@class='indexed-biz-name']/a[@class='biz-name js-analytics-click']/span/text()").extract()

        for content in url1:
            c = content.split("?")
            url.append(c[0])
        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = yelpCrawler(self.category, servicelist[i], url[i])
            # yield Request(url=url[i], callback=crawler.parsing)
            yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        next_page = response.xpath(
                "//div[@class='arrange_unit']/a[@class='u-decoration-none next pagination-links_anchor']/@href").extract()
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    print(type(next_page_url))
                    print(next_page_url)
                    # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                    yield response.follow(next_page_url, callback=self.parsing)






