from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree

class whtop():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

#TODO rating pending and header not found: heading done rating need to discuss with sandy
    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        #http://www.whtop.com/review/bluehost.com
        authors = response.xpath("//div[@property='author']/span[1]/text()").extract()
        dates = response.xpath("//div[@class='review-date']/time/text()").extract()

        website_name = response.xpath("//div[@id='line']/a[1]/img/@alt").extract()
        headings = response.xpath("//div[@class='review-content']/span/b/i").extract()
        stars = response.xpath("//div[@class='review-rating'][1]/span/span/@class").extract()
        rate = []
        for i in range(0,len(stars)):
            rate.append()
        for node in response.xpath("//div[@class='review-content']"):
            reviews.append(node.xpath('string()').extract());
        if len(reviews) == 0:
            for node in response.xpath('//div[@class="comment pure-u-1 pure-u-lg-2-3 wcc"]'):
                reviews.append(node.xpath('string()').extract())
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], None, website_name);
            servicename1.save()

