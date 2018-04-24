from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree

class WebHostingHeroCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        #https: // www.webhostinghero.com / reviews / bluehost /
        for node in response.xpath("//div[@class='container']/ul[@class='responsive-grid col-12']/li[@class='box col-12']/div[@class='box col-12 review-detail']/p[2]/span"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='container']/ul[@class='responsive-grid col-12']/li[@class='box col-12']/div[@class='box col-12 review-title']/meta[@itemprop = 'ratingValue']/@content").extract()
        dates = response.xpath("//div[@class='container']/ul[@class='responsive-grid col-12']/li[@class='box col-12']/div[@class='box col-12 review-info']/span[@class='review-date']/text()").extract()
        headings =  response.xpath("//div[@class='container']/ul[@class='responsive-grid col-12']/li[@class='box col-12']/div[@class='box col-12 review-title']/h4/text()").extract()
        authors =  response.xpath("//div[@class='container']/ul[@class='responsive-grid col-12']/li[@class='box col-12']/div[@class='box col-12 review-info']/strong/span/text()").extract()
        website_name =  response.xpath("/html/head/meta[9]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, ratings[item],headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], "",website_name)
            servicename1.save()
        next_page = response.xpath("//div[@class='container']/div[@class='navigator']/a[last()]/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page[0])
            print(next_page_url)
            if next_page_url and next_page_url.strip():
                yield Request(url=next_page_url,  callback=self.parsing)
