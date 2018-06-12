from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
# https://www.virtualbanking.com/reviews/localbitcoins-review/

class VirtualBanking(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename

        for node in response.xpath("//div[@id='user-reviews-wrap']/ul[@id='user-reviews']/li/div[@class='user-review']"):
            reviews.append(node.xpath('string()').extract());
        ratings1 = response.xpath("//div[@id='user-reviews-wrap']/ul[@id='user-reviews']/li/div[@class='user-stars']/img/@src").extract()
        ratings = []
        i = 0
        while i < len(ratings1):
            ratings.append(getStarts(ratings1[i]))
            i = i + 1
        ratings = map(lambda foo: foo.replace('.', ''), ratings)
        dates1 = response.xpath("//div[@id='user-reviews-wrap']/ul[@id='user-reviews']/li/div[@class='user-name']/text()").extract()
        dates = []
        dates2= []
        authors = []
        j = 0
        while j < len(dates1):
            dates2 = (dates1[j].split(" "))
            dates.append(dates2[5])
            authors.append(dates2[2])
            j = j+1
        website_name =  response.xpath("//header/div[@class='wrapper']/a[@id='logo']/@href").extract()
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, ratings[item],None, dates[item], authors[item], category,
                          servicename, reviews[item], None,website_name)
            servicename1.save()

