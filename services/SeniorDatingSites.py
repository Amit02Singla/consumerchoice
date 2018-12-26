from model.Servicemodel import ServiceRecord
from lxml import etree

from utils.utils import getStarts

# http://www.top20seniordatingsites.com/product/senior-people-meet/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class SeniorDatingSites(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(SeniorDatingSites,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        authors = []
        ratings = []
        print("review from seniordatingsites.com")
        # http://www.top20seniordatingsites.com/product/senior-people-meet/
        node = response.xpath("//div[@class='commentlist']/div[@class='review']").extract()
        for content in node:
            root = etree.HTML(content)
            reviews.append(root.xpath("//div[@class='review-content']/p/text()"))
            if(len(root.xpath("//div[@class='review-author']/text()"))>0):
                authors.append(root.xpath("//div[@class='review-author']/text()")[0])
            else:
                authors.append("")
            if(len(root.xpath("//div[@class='review-ratings']/div[@class='star-review']/span/@class"))>0):
                ratings1 = root.xpath("//div[@class='review-ratings']/div[@class='star-review']/span/@class")
            i=0
            rat = 0
            while i < len(ratings1):
                c= ratings1[i].split(' ')
                c= c[2].replace('-','')
                stars = float(getStarts(c))
                rat = rat + stars
                if(i==5):
                    if rat > 0.0:
                        ratings.append((round(float(rat/6.0)), 1))
                    else:
                        ratings.append("0.0")
                i = i+1



        # for node in response.xpath("//div[@class='commentlist']/div/div[@class='review-content']"):
        #     reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='review-ratings']/div[@class='star-review']/span/@class").extract()
        # i = 0
        # c = 0
        # j = 0
        # ratings1 = []
        # while i < len(ratings):
        #     j = j+1;
        #     if(j/6==1):
        #         c= c + int(ratings[1]);
        #         ratings1.append(c/6.0)
        #         j=0;
        #     else:
        #         c= c + int(ratings[i])
        #
        #     i = i + 1
        #
        # authors = response.xpath("//div[@class='commentlist']/div/div[@class='review-author']/text()").extract()
        website_name = "top20seniordatingsites.com"
        print("reviews ", len(reviews), reviews)
        print("ratings  ", len(ratings), ratings)
        print("authors ", len(authors), authors)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, None, authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()


