from scrapy import Spider, Request
from lxml import etree

from services.ReviewCentre import ReviewCentre

urlListt =[]
urlssss = []
class ReviewCentreURLCategory(Spider):
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response, self.category)
    def crawl(self, response, category):
        def __init__(self, category):
            self.url_list = []
            self.category = category

        def parsing(self, response):
            return self.crawl(response, self.category)

        def crawl(self, response, category):
            url = []
            serviceList = []

            self.category = category
            url = response.xpath(
                "//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/@href").extract()
            serviceList = response.xpath("//div[@class='ItemCardSlim']/div[@class='FirstSection']/h2/a/text()").extract()
            # for content in url1:
            #     root = etree.HTML(content)
            #     if (len(root.xpath("//div[@class='site_item_content']/div[@class='content']/h3/a")) > 0):
            #         url.append(root.xpath("//div[@class='site_item_content']/div[@class='content']/h3/a/@href"))
            #     if (len(root.xpath("//div[@class='site_item_content last']/div[@class='content']/h3/a")) > 0):
            #         url.append(root.xpath("//div[@class='site_item_content last']/div[@class='content']/h3/a/@href"))
            # for content1 in servicelist1:
            #     root = etree.HTML(content1)
            #     if (len(root.xpath("//div[@class='site_item_content']/div[@class='content']/h3/a")) > 0):
            #         serviceList.append(
            #             root.xpath("//div[@class='site_item_content']/div[@class='content']/h3/a/text()"))
            #     if (len(root.xpath("//div[@class='site_item_content last']/div[@class='content']/h3/a")) > 0):
            #         serviceList.append(
            #             root.xpath("//div[@class='site_item_content last']/div[@class='content']/h3/a/text()"))
            print(len(url), url)
            print(len(serviceList), serviceList)
            # i = 0
            # while i < len(url):
            #     j = 0
            #     while j < len(url[i]):
            #         crawler = ReviewCentre(self.category, serviceList[i][j],
            #                                      url[i][j])
            #         yield response.follow(url=url[i][j], callback=crawler.parsing)
            #         # print(url[i][j])
            #         # print(serviceList[i][j])
            #         j = j + 1
            #     i = i + 1
            next_page = response.xpath(
                "//div[@class='navigation']/div[@class='paginator_next']/span/a[@class='button outline']/@href").extract()
            if next_page is not None:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    print(type(next_page_url))
                    print(next_page_url)
                    # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                    yield response.follow(next_page_url, callback=self.parsing)