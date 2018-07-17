from scrapy import Spider, Request
from lxml import etree

from services.ReviewCentre import ReviewCentre
from services.siteservices.ReviewCentreURLCategory import ReviewCentreURLCategory


urlssss = []
class ReviewCentreURLCrawler(Spider):
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

        url1 = response.xpath(
            "//div[@id='SearchResults']").extract()
        urlNew = response.xpath("//div[@class='FirstSection']/h2/a/@href").extract()
        serviceList = response.xpath("//div[@class='FirstSection']/h2/a/text()").extract()
        urlnext = response.xpath("//div[@class='ItemCardSlim Category TopMatchItem']/div[@class='FirstSection']/h2/a/@href").extract();
        serviceListnext = response.xpath("//div[@class='ItemCardSlim Category TopMatchItem']/div[@class='FirstSection']/h2/a/text()").extract();
        urlNew  =list(set(urlNew)-set(urlnext))
        service = list(set(serviceList)-set(serviceListnext))
        print("urlnew   ", len(urlNew), urlNew)
        print("urlnext   ", len(urlnext), urlnext)
        url = 0
        while url < len(urlNew):
            crawler = ReviewCentre(self.category, service[url], urlNew[url])
            yield response.follow(url=urlNew[url], callback=crawler.parsing)
            url = url+1
        url = 0
        while url < len(urlnext):
            sss = ReviewCentreURLCategory(self.category)
            yield Request(urlnext[url], callback=sss.parsing)
            url= url+1
        # for content in url1:
        #     root = etree.HTML(content)
        #     if (len(root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/@href")) > 0):
        #         url.append(root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/@href"))
        #         if (len(root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/text()")) > 0):
        #             serviceList.append(root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/text()"))
        #     elif (len(root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/@href")) > 0):
        #         url.append(root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/@href"))
        #         if (len(root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/text()")) > 0):
        #             serviceList.append(
        #                 root.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/text()"))
        #
        #     if (len(root.xpath("//div[@class='ItemCardSlim Category TopMatchItem']/div[@class='FirstSection']/h2/a/@href")) > 0):
        #         page = root.xpath("//div[@class='ItemCardSlim Category TopMatchItem']/div[@class='FirstSection']/h2/a/@href")[0]
        #         print("pageeeeee   ", page)
        #         sss = ReviewCentreURLCategory(self.category)
        #         yield Request(page, callback=sss.parsing)
        #
        #
        # if(len(serviceList)>0):
        #     print("serviceList  ", len(serviceList[0]), serviceList[0])
        #     print("URL ", len(url[0]), url[0])
        # i = 0

        # while i < len(url):
        #     j = 0
        #     while j < len(url[i]):
        #         crawler = ReviewCentre(self.category, serviceList[0][j], url[i][j])
        #         yield response.follow(url=url[i][j], callback=crawler.parsing)
        #         # print(url[i][j])
        #         j = j + 1
        #     i = i + 1
        next_page = response.xpath(
                "//div[@class='Pagination Pagination-SearchPagination'][2]/a[@class='PaginationLink PaginationNext-SearchPagination']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)


