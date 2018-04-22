from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree

class webshostingFatcow(Spider):
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)
#TODO rating pending
    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("webshostingFatcow.com")
        authors = response.xpath("//div[@class='comment-user-left name']/text()").extract()
        dates = response.xpath("//div[@class='comment-user-left date']/text()").extract()
        print("authors  ", authors)
        print("dates  ", dates)
        website_name = response.xpath("//div[@id='line']/a[1]/img/@alt").extract()
        headings = response.xpath("//div[@class='comments_user_comment']/a").extract()
        ratings1 = response.xpath("//div[@class='user-info pure-u-1']/img[@class='stars overall']/@alt").extract()
        if len(ratings1) == 0 :
            ratings1 = response.xpath("//div[@class='rating pure-u-1 pure-u-lg-1-3']/img[@class='stars overall']/@alt").extract()
        for node in response.xpath('//div[@class="comment-body"]'):
            reviews.append(node.xpath('string()').extract());
        if len(reviews) == 0:
            for node in response.xpath('//div[@class="comment pure-u-1 pure-u-lg-2-3 wcc"]'):
                reviews.append(node.xpath('string()').extract());
        print("  reviews   ", reviews)
        print("  headings   ", headings)
        print("  websitesName   ", website_name)



        for item in range(0, len(reviews)):

            servicename1 = ServiceRecord(response.url, None, headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], None, website_name);
            servicename1.save()

