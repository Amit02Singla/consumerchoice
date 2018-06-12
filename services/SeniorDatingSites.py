from model.Servicemodel import ServiceRecord
from lxml import etree

from utils.utils import getStarts

# http://www.top20seniordatingsites.com/product/senior-people-meet/
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
        #TODO Done
        for node in response.xpath("//div[@class='commentlist']/div/div[@class='review-content']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='commentlist']/div/div[@class='review-ratings']/div[@class='star-review']/span/text()").extract()
        i = 0
        c = 0
        j = 0
        ratings1 = []
        while i < len(ratings):
            j = j+1;
            if(j/6==1):
                c= c + int(ratings[1]);
                ratings1.append(c/6.0)
                j=0;
            else:
                c= c + int(ratings[i])

            i = i + 1

        authors = response.xpath("//div[@class='commentlist']/div/div[@class='review-author']/text()").extract()
        website_name = response.xpath("//div[@id='container']/div[@id='header']/div[@class='left eight columns']/div/a[@class='logo']/img/@title").extract()

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings1[item], None, None, authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()


