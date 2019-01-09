from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
# http://www.whtop.com/review/bluehost.com#reviews
#TODO rating pending and header not found: heading done rating need to discuss with sandy : Done
class whtop(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(whtop,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #http://www.whtop.com/review/bluehost.com#reviews
        authors = response.xpath("//div[@property='author']/span[1]/text()").extract()
        dates = response.xpath("//div[@class='review-date']/time/text()").extract()

        website_name = response.xpath("//div[@id='container']/div[@id='main']/div/div[@id='server']/a/@href").extract()[0]
        head = response.xpath("//div[@class='review-main']").extract()
        headings = []
        for content in head:
            root = etree.HTML(content)
            if(len(root.xpath("//div[@class='review-content']/span/b/i"))>0):
                headings.append(root.xpath("//div[@class='review-content']/span/b/i/text()")[0])
            else:
                headings.append(root.xpath("//div[@class='review-content']/text()"))

        # stars = response.xpath("//div[@class='review-rating'][1]/span/span/@class").extract()
        # rate = []
        stars = response.xpath(
            "//div[@class='review-ratings']").extract()
        rate = []
        for content in stars:
            root = etree.HTML(content)
            # print(content)
            if (len(root.xpath("//div[@class='review-rating']/span/@class")) > 0):
                rate.append(root.xpath("//div[@class='review-rating']/span/@class"))
            else :
                rate.append("");
            if (len(root.xpath("//div[@class='review-rating']/span/span/@class")) > 0):
                rate.append(root.xpath("//div[@class='review-rating']/span/span/@class"))
        i = 0

        c = 0
        sum = 0
        ratings = []
        # print(" length ", len(rate))
        while i < len(rate):
            j = 0
            rate[i] = map(lambda foo: foo.replace('-', ''), rate[i])
            rate[i] = map(lambda foo: foo.replace('stars stars', ''), rate[i])
            # print rate[i]
            while j < len(rate[i]):
                if (float(rate[i][j]) > 5.0):
                    c = float(rate[i][j]) / 10.0
                    sum = sum + c
                else:
                    sum = sum + float(rate[i][j])
                if (i % 2 == 1):
                    sum = sum / 5.0
                    ratings.append(sum)
                    sum = 0;
                j = j + 1
            i = i + 1
        print("website ", website_name)
        for node in response.xpath("//div[@class='review-content']"):
            reviews.append(node.xpath('string()').extract());
        if len(reviews) == 0:
            for node in response.xpath('//div[@class="comment pure-u-1 pure-u-lg-2-3 wcc"]'):
                reviews.append(node.xpath('string()').extract())

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], "",
                          self.servicename, reviews[item], None, website_name);
            self.save(servicename1)
        self.pushToServer()

