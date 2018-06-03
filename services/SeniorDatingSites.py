from model.Servicemodel import ServiceRecord
from lxml import etree

from utils.utils import getStarts


class SeniorDatingSites():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from seniordatingsites.com")
        # http://www.top20seniordatingsites.com/product/senior-people-meet/
        #TODO Full website redo
        for node in response.xpath("//div[@id='main-inner']/ul[@id='user-reviews']/li/div[@class='userrev']/div[@class='user-review']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@id='main-inner']/ul[@id='user-reviews']/li/div[@class='userrev']/div[@class='user-stars']/img/@src").extract()
        i = 0
        ratings1 = []
        while i < len(ratings):
            ratings1.append(getStarts(ratings[i]))
            i = i + 1

        # dates = response.xpath("//div[@class='review-sub-cntnr']/div[@class='review-one-all']/div[@class='review-profile']/div[@class='review-mid']/p/text()").extract()
        # img_src = response.xpath("//div[@class='logo-profile']/img/@src").extract()
        authors = response.xpath("//div[@id='main-inner']/ul[@id='user-reviews']/li/div[@class='userrev']/div[@class='user-name']/text()").extract()
        website_name = response.xpath("//div[@id='container']/div[@id='header']/div[@class='left eight columns']/div/a[@class='logo']/img/@title").extract()
        print(" Ratings ", len(ratings1), ratings1)
        # print("dates ", len(dates), dates)
        print(" Reviews ", len(reviews), reviews)
        # print(" headings ", len(headings), headings)
        print(" authors ", len(authors), authors)
        print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings1[item], None, None, authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()


