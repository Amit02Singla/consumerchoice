from model.Servicemodel import ServiceRecord
from utils.utils import getStarts
from scrapy import Spider, Request
from lxml import etree

# https://www.webshosting.review/fatcow-reviews
class webshostingFatcow(Spider):
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)
#TODO Done
    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        #print("webshostingFatcow.com")
        authors = response.xpath("//div[@class='comment-user-left name']/text()").extract()
        dates = response.xpath("//div[@class='comment-user-left date']/text()").extract()
        website_name = response.xpath("//div[@id='line']/a[1]/img/@alt").extract()
        headings = response.xpath("//div[@class='comments_user_comment']/a/text()").extract()
        ratings1 = response.xpath("//div[@class='comment_user_star_rate']/div[@class='comment_user_stars']/img/@src").extract()
        if len(ratings1) == 0:
            ratings1 = response.xpath("//div[@class='rating pure-u-1 pure-u-lg-1-3']/img[@class='stars overall']/@alt").extract()
        ratings = []
        i=0
        while i < len(ratings1):
            ratings.append(getStarts(ratings1[i]))
            # print(getStarts(ratings1[i]))
            i = i+1
        ratings = map(lambda foo: foo.replace('-', ''), ratings)
        ratings = map(lambda foo: foo.replace('.', ''), ratings)
        sum = 0
        ratings2 = []
        i = 0
        c = 0
        j = 0
        ratings1 = []
        while i < len(ratings):
            j = j + 1;
            if (j / 5 == 1):
                c = c + int(ratings[1]);
                ratings1.append(c / 5.0)
                j = 0;
            else:
                c = c + int(ratings[i])

            i = i + 1


        for node in response.xpath('//div[@class="comment-body"]'):
            reviews.append(node.xpath('string()').extract());
        if len(reviews) == 0:
            for node in response.xpath('//div[@class="comment pure-u-1 pure-u-lg-2-3 wcc"]'):
                reviews.append(node.xpath('string()').extract());


        for item in range(0, len(reviews)):

            servicename1 = ServiceRecord(response.url, ratings1[item], headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], None, website_name);
            servicename1.save()

