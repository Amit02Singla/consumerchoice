from scrapy import Spider, Request
from lxml import etree

from services.HostingFactsCrawler import HostingFactsCrawler
# TODO: need to get next page url from javascript

urlssss = []
class HostingFactsURLCrawler(Spider):
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

        url1 = response.xpath(".//table[@class='table-blue table-rating']/tbody/tr/td[2]").extract()
        servicelist1 = response.xpath("//div[@id='content']/div[@id='search']/div[@id='content_wrapper']/div[@id='left_column']/div[@class='review']/div[@class='info left']/div[@class='url track-search']").extract()

        for content in url1:
            root =  etree.HTML(content)
            if(len(root.xpath("//strong/a"))>0):
                url.append(root.xpath("//strong/a/@href")[0])
                serviceList.append(root.xpath("//strong/a/text()")[0])
            elif(len(root.xpath("//strong/u/a"))>0):
                url.append(root.xpath("//strong/u/a/@href")[0])
                serviceList.append(root.xpath("//strong/u/a/text()")[0])
            elif (len(root.xpath("//a")) > 0):
                url.append(root.xpath("//a/@href")[0])
                if(len(root.xpath("//a/strong/text()"))>0):
                    serviceList.append(root.xpath("//a/strong/text()")[0])
                elif(len(root.xpath("//a/span/text()"))>0):
                    serviceList.append(root.xpath("//a/span/text()")[0])
                else:
                    serviceList.append(root.xpath("//a/text()")[0])
            elif (len(root.xpath("//u/strong/a")) > 0):
                url.append(root.xpath("//u/strong/a/@href")[0])
                serviceList.append(root.xpath("//u/strong/a/text()")[0])
            elif (len(root.xpath("//span/strong/u/a")) > 0):
                url.append(root.xpath("//span/strong/u/a/@href")[0])
                serviceList.append(root.xpath("//span/strong/u/a/text()")[0])
            elif (len(root.xpath("//u/a")) > 0):
                url.append(root.xpath("//u/a/@href")[0])
                serviceList.append(root.xpath("//u/a/text()")[0])




        #
        # for content1 in servicelist1:
        #     content1 = content1.replace('<b>', '')
        #     content1 = content1.replace('</b>', '')
        #     # print(content1)
        #     root = etree.HTML(content1)
        #     if (len(root.xpath("//a")) > 0):
        #         serviceList.append(root.xpath("//a/text()"))

        print("serviceList  ", len(serviceList), serviceList)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            if('reviews' in url[i]):
                crawler = HostingFactsCrawler(self.category, serviceList[i], url[i])
                yield Request(url=url[i], callback=crawler.parsing)
                # yield response.follow(url=url[i], callback=crawler.parsing)
                # print(url[i][j])
            i=i+1
        #     next_page = response.xpath(
        #         "//div[@id='left_column']/div[@class='navigation']/div[@class='paginator_next']/span/a[@class='button outline']/@href").extract()
        # if next_page is not None:
        #     next_page_url = "".join(next_page)
        #     if next_page_url and next_page_url.strip():
        #         print(type(next_page_url))
        #         print(next_page_url)
        #         # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        #         yield response.follow(next_page_url, callback=self.parsing)






