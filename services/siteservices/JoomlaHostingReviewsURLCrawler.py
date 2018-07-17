from scrapy import Spider, Request
from lxml import etree

from services.JoomlaHostingReviews import JoomlaHostingReviews


urlssss = []
class JoomlaHostingReviewsURLCrawler(Spider):
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

        url = response.xpath("//h4[@class='result-title ']/a/@href").extract()
        serviceList = response.xpath("//h4[@class='result-title ']/a/text()").extract()
        for content in serviceList:
            servicelist.append(content.strip())


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = JoomlaHostingReviews(self.category, servicelist[i], url[i])
            # yield Request(url=url[i], callback=crawler.parsing)
            yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        next_page = response.xpath("//li[@class='pagination-next']/a[@class='hasTooltip pagenav']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url, callback=self.parsing)
