from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree

class whtop():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

#TODO rating pending and header not found
    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("whtop.com")
        authors = response.xpath("//div[@property='author']/span[1]/text()").extract()
        dates = response.xpath("//div[@class='review-date']/time/text()").extract()
        #print("authors  ", len(authors), authors)
        #print("dates  ", len(dates), dates)
        website_name = response.xpath("//div[@id='line']/a[1]/img/@alt").extract()
        # headings = response.xpath("//div[@class='review-content']/span/b/i").extract()
        ratings1 = response.xpath("//div[@class='user-info pure-u-1']/img[@class='stars overall']/@alt").extract()
        if len(ratings1) == 0 :
            ratings1 = response.xpath("//div[@class='rating pure-u-1 pure-u-lg-1-3']/img[@class='stars overall']/@alt").extract()
        for node in response.xpath("//div[@class='review-content']"):
            reviews.append(node.xpath('string()').extract());
        if len(reviews) == 0:
            for node in response.xpath('//div[@class="comment pure-u-1 pure-u-lg-2-3 wcc"]'):
                reviews.append(node.xpath('string()').extract());
        #print("  reviews   ", len(reviews), reviews)
        #print("  websitesName   ",len(website_name), website_name)
        # print("headings ", len(headings), headings)


        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                          servicename, reviews[item], None, website_name);
            servicename1.save()

