from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts


class CoinJabber(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename
        # https: // www.webhostinghero.com / reviews / bluehost /
        for node in response.xpath(
                "//div[@id='review_anchor']/ul[@class='review_list']/li/p[2]"):
            reviews.append(node.xpath('string()').extract());
        ratings1 = response.xpath("//div[@id='review_anchor']/ul[@class='review_list']/li/p[1]/span[@class='ratting_star pull-right']/em/@style").extract()
        dates1 = response.xpath("//div[@id='review_anchor']/ul[@class='review_list']/li/p[1]/text()").extract()
        authors = []
        dates = []
        i=0
        dates2 = []
        while(i<len(dates1)):
            authors.append(dates1[i])
            i = i+1
            dates2.append(dates1[i])
            i= i+1
            authors = map(lambda foo: foo.replace('(', ''), authors)
        j=0

        while(j<len(dates2)):
            c = dates2[j].split(" ")
            dates.append(c[2])
            j = j +1
        ratings = []
        j = 0
        while j < len(ratings1):
            c = int(getStarts(ratings1[j]))
            ratings.append((c) / 20.0)
            j = j + 1
        # authors = response.xpath("//div[@class='content-item review-item']/div[@class='content-item-author-info']/a/div[@class='author-name']/text()").extract()
        # img_src = response.xpath(
        #     "//div[@class='content-item review-item']/div[@class='content-item-author-info']/a/div[@class='avatar avatar-large']/img/@data-lazy-src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name1 = response.xpath("//head/meta[7]/@content").extract()
        website_name2 = website_name1[0].split("|")
        website_name = []
        website_name.append(website_name2[1])
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        # print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], category,
                                         servicename, reviews[item], None, website_name)
            servicename1.save()





