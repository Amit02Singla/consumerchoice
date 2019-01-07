from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class webHostingmedia(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(webHostingmedia,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #print("review from webHostingmedia.com")
        # https://webhostingmedia.net/bluehost-reviews/
        for node in response.xpath("//div[@class='testimonial']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='sp_rating']/div[@class='rateit']/@data-rateit-value").extract()
        dates = response.xpath("//div[@class='wpcr_fl wpcr_rname']/span[@class='dtreviewed']/text()").extract()
        # headings = response.xpath("//div[@class='width64 floatleft']/h4[3]").extract()
        authors = response.xpath("//div[@class='wpcr_fl wpcr_rname']/span/span/strong/text()").extract()
        website_name = response.xpath("//div[@class='col span_6']/div[@class='company-button start-button']/a/@href").extract()[0]
        print("reviews ", len(reviews), reviews)
        print("dates ", len(dates), dates)
        print("ratings ", len(ratings), ratings)
        print("authors ", len(authors), authors)
        print "website " , website_name
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()


