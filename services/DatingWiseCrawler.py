from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
# http://www.datingwise.com/review/silversingles.com/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class DatingWiseCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(DatingWiseCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #http://www.datingwise.com/review/match.com/
        for node in response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='callout border-callout']"):
            reviews.append(node.xpath('string()').extract());
        dates = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='userDetails']/div[@class='userLocation']/p[1]/span[@class='pIcn']/text()").extract()
        authors =  response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='userDetails']/div[@class='userLocation']/p[1]/span[@class='pIcn']/span/a/text()").extract()
        headings = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='userDetails']/div[@class='userLocation']/p[@class='clear']/span/text()").extract()
        website_name =  "datingwise.com"
        # img_src = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()
        print("Reviews ", len(reviews))
        print("Authors ", len(authors))
        # print("Rating ", len(ratings))
        print("Dates ", len(dates))
        # print("img_src ", len(img_src))
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, None,headings[item], dates[item], authors[item], "",
                          self.servicename, reviews[item], None,website_name)
            self.save(servicename1)
        self.pushToServer()

