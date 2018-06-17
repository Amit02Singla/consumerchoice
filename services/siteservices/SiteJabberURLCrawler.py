from scrapy import Spider, Request
from lxml import etree

from services.SiteJabberCrawler import SiteJabberCrawler
from services.Revex import Revex

urlssss = []
class SiteJabberURLCrawler(Spider):
    def __init__(self):
        self.url_list = []
    def parsing(self, response):
        return self.crawl(response, self.category)
    def crawl(self, response, category):
        url = []
        serviceList= []
        self.category = category
        # https://www.sitejabber.com/reviews/zoosk.com
        url1 = response.xpath("//div[@id='content']/div[@id='search']/div[@id='content_wrapper']/div[@id='left_column']").extract()
        servicelist1 = response.xpath("//div[@id='content']/div[@id='search']/div[@id='content_wrapper']/div[@id='left_column']/div[@class='review']/div[@class='info left']/div[@class='url track-search']").extract()
        for content in url1:
            root =  etree.HTML(content)
            if(len(root.xpath("//div[@class='review']/div[@class='info left']/div[@class='url track-search']/a/@href"))>0):
                url.append(root.xpath("//div[@class='review']/div[@class='info left']/div[@class='url track-search']/a/@href"))


        for content1 in servicelist1:
            content1 = content1.replace('<b>', '')
            content1 = content1.replace('</b>', '')
            # print(content1)
            root = etree.HTML(content1)
            if (len(root.xpath("//a")) > 0):
                serviceList.append(root.xpath("//a/text()"))

        print("serviceList  ", len(serviceList), serviceList)
        print("URL ", len(url), url)
        i=0
        # urlsssssssssss = {"Category": self.category,
        #                   "ServiceName": "",
        #                   "url": 'https://revex.co/internet-of-people/'}
        # crawler = Revex(self.category, "Services", 'https://revex.co/internet-of-people/')
        # yield response.follow(url="https://revex.co/internet-of-people/", callback=crawler.parsing)

        while i< len(url):
            j=0
            while j < len(url[i]):
                urlsssssssssss = {"Category": self.category,
                 "ServiceName": "",
                 "url": 'https://www.sitejabber.com' + url[i][j]}
                crawler = SiteJabberCrawler(self.category, serviceList[j][0], 'https://www.sitejabber.com' + url[i][j])
                yield response.follow(url="https://www.sitejabber.com" + url[i][j], callback=crawler.parsing)
                # print(url[i][j])
                j = j+1
            i=i+1
        next_page = response.xpath("div[@id='left_column']/div[@class='navigation']/div[@class='paginator_next']/span/a[@class='button outline']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)






