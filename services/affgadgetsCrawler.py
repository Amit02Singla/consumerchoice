from model.Servicemodel import ServiceRecord

from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from utils.utils import getStarts
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
from urlparse import urlparse

class affgadgetsCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(affgadgetsCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # http://affgadgets.com/binance
        for node in response.xpath('//div[@class="comment-info"]'):
            reviews.append(node.xpath('string()').extract());
        ratings1 = response.xpath("//div[@class='comment-author-main-meta-info']/div/@class").extract()

        author =  response.xpath("//div[@class='comment-author-main-meta']").extract()
        authors = []
        for content in author:
            root = etree.HTML(content)
            if(root.xpath("//div[@class='comname']")):
                authors.append(root.xpath("//div[@class='comname']/cite[@class='fn']/text()")[0])
            else:
                authors.append("")
        dates = response.xpath("//div[@class='comment-author-main-meta-info']/ cite[ @class ='timed'] / text()").extract()
        website_name = response.xpath("//section[@class='top-link first-top-link sidebar-clear']/div[@class='sidebar-inner']/a/@href").extract()[0]
        parsedURL = urlparse(website_name)
        name = "affgadgets.com"
        # website_name = parsedURL.scheme + '://' + parsedURL.hostname
        ratings = []
        j = 0
        while j < len(ratings1):
            c = int(getStarts(ratings1[j]))
            ratings.append((c))
            j = j + 1

        print("Reviews ", len(reviews))
        print("Authors ", len(authors), )
        print("ratings ", len(ratings), )

        print("Dates ", len(dates), dates)

        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url,ratings[item],None,dates[item],authors[item],self.category,self.servicename,reviews[item],"",website_name, name);
            self.save(servicename1)
        self.pushToServer()