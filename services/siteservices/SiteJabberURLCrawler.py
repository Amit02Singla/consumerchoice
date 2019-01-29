from scrapy import Spider, Request
from lxml import etree

from services.SiteJabberCrawler import SiteJabberCrawler
from services.Revex import Revex
from services.siteservices.SiteJabberURLWebHosting import SiteJabberURLWebHosting

urlssss = []
class SiteJabberURLCrawler(Spider):
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response)
    def crawl(self, response):
        url = []
        serviceList= []
        url1 = response.xpath("//div[@id='content']/div[@id='search']/div[@id='content_wrapper']/div[@id='left_column']").extract()
        servicelist1 = response.xpath("//div[@id='content']/div[@id='search']/div[@id='content_wrapper']/div[@id='left_column']/div[@class='review']/div[@class='info left']/div[@class='url track-search']").extract()

        for content in url1:
            root =  etree.HTML(content)
            if(len(root.xpath("//div[@class='review']/div[@class='info left']/div[@class='url track-search']/a/@href"))>0):
                url.append(root.xpath("//div[@class='review']/div[@class='info left']/div[@class='url track-search']/a/@href"))
            if (len(root.xpath(
                "//div[@class='categories ']/div[@class='category']/div[@class='info_cat']/div[@class='name']/a/@href")) > 0):
                page = root.xpath(
                "//div[@class='categories ']/div[@class='category']/div[@class='info_cat']/div[@class='name']/a/@href")[
                0]
                print("[pageeeeee   ", page)
                sss = SiteJabberURLWebHosting(self.category)
                yield response.follow(page, callback=sss.parsing)

        for content1 in servicelist1:
            content1 = content1.replace('<b>', '')
            content1 = content1.replace('</b>', '')
            # print(content1)
            root = etree.HTML(content1)
            if (len(root.xpath("//a")) > 0):
                serviceList.append(root.xpath("//a/text()"))
        # print("serviceList  ", len(serviceList), serviceList)
        # print("URL ", len(url), url)
        i=0
        while i< len(url):
            j=0
            while j < len(url[i]):
                self.url_list.append('https://www.sitejabber.com' + url[i][j])
                j = j+1
            i=i+1
        next_page = response.xpath(
                "//div[@id='left_column']/div[@class='navigation']/div[@class='paginator_next']/span/a[@class='button outline']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
    def closed(self, reason):
        print("in close metthod url List ", len(self.url_list), "   url list   ",self.url_list)






