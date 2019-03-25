from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts


class CoinJabberCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename
        # https://www.coinjabber.com/site/coinmama.com
        for node in response.xpath("//div[@id='review_anchor']/ul[@class='review_list']/li/p[2]"):
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
            c = int(getStarts(str(ratings1[j]).split(":")[1].split("%")[0]))
            ratings.append((c) / 20.0)
            j = j + 1
        website_name1 = response.xpath("//head/meta[7]/@content").extract()
        website_name2 = website_name1[0].split("|")
        website_name = []
        website_name.append(website_name2[1])
        name="coinjabber.com"
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], None, website_name, name)
            servicename1.save()





