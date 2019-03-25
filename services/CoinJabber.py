from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler

class CoinJabber(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(CoinJabber,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        reviews1 = []

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
        website_name1 = self.link["url"].split("/")
        website_name = 'https://' + website_name1[len(website_name1) - 1]
        name = "coinjabber.com"
        print("Reviews ", len(reviews))
        print("Authors ", len(authors))
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates))
        # print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], None, website_name, name)
            self.save(servicename1)
        self.pushToServer()





