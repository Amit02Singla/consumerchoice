from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
# http://www.datingwise.com/review/silversingles.com/
class DatingWiseCrawler(Spider):
#Todo: Done
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        #http://www.datingwise.com/review/match.com/
        for node in response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='callout border-callout']"):
            reviews.append(node.xpath('string()').extract());
        dates = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='userDetails']/div[@class='userLocation']/p[1]/span[@class='pIcn']/text()").extract()
        authors =  response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='userDetails']/div[@class='userLocation']/p[1]/span[@class='pIcn']/span/a/text()").extract()
        headings = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='userDetails']/div[@class='userLocation']/p[@class='clear']/span/text()").extract()
        website_name =  response.xpath("/html/head/meta[9]/@content").extract()
        img_src = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, None,headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], img_src,website_name)
            servicename1.save()

