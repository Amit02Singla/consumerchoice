from model.Servicemodel import ServiceRecord
# http://reviewsdatingsites.com/site/elitesingles
# TODO: need to check Dates
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class ReviewDatingSitesCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ReviewDatingSitesCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("Review Datingsites")
        # http://reviewsdatingsites.com/site/elitesingles
        for node in response.xpath("//div[@id='reviews']/div[@class='review']/div[@class='row']/div[@class='col-md-9']/div[@class='review-content']"):
            reviews.append(node.xpath('string()').extract())
        ratings =  response.xpath("//div[@class='col-md-9']/h4[@class='m-t-0']/span[@class='stars']/span[@itemprop='ratingValue']/@content").extract()
        authors =   response.xpath("//div[@class='media-body text-center']/div/strong/a[@itemprop='author']/text()").extract()
        website_name = "reviewsdatingsites.com"
        dates1 = response.xpath("//div[@id='reviews']/div[@class='review']/div[@class='row']/div[@class='col-md-9']/h4[@class='m-t-0']/strong[@class='text-muted date']/text()").extract()
        dates= []
        for content in dates1:
            dates.append(content.strip())
        print("reviews ", len(reviews), reviews)
        print("ratings ", len(ratings), ratings)
        print("authors ", len(authors), authors)
        print("dates ", len(dates), dates)
        print("websites ", website_name)

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], self.category,
                          self.servicename, reviews[item],None,website_name);
            self.save(servicename1)
        self.pushToServer()