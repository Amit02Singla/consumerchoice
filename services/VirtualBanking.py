from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
# https://www.virtualbanking.com/reviews/localbitcoins-review/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class VirtualBanking(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(VirtualBanking,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
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
            dates.append(dates2[len(dates2)-1].strip())
            authors.append(dates2[2])
            j = j+1
        # website_name =  response.xpath("//header/div[@class='wrapper']/a[@id='logo']/@href").extract()
        website_name = response.xpath("//article[@class='offer9']/div/div[@id='review-body']/div[@class='visitouter clearfix'][1]/div[@class='visitsite']/a[@class='button visit outbound']/@href").extract()[0]
        print("dates", len(dates), dates)
        print("websites  ", website_name)
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, ratings[item],None, dates[item], authors[item], "",
                          self.servicename, reviews[item], None,website_name)
            self.save(servicename1)
        self.pushToServer()

