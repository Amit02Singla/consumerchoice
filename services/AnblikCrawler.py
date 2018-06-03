from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request



class AnblikCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename
        # http://www.anblik.com/reviews/sitebuilder-com/
        for node in response.xpath("//ol[@class='commentlist']/li/div/div[@class='comment-text']/div[@class='description']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@id='comments']/ol[@class='commentlist']/li/div/div[@class='comment-text']/div[@class='star-rating']/span/strong/text()").extract()
        dates = response.xpath("//ol[@class='commentlist']/li/div/div[@class='comment-text']/p[@class='meta']/time[@class='woocommerce-review__published-date']/text()").extract()
        authors = response.xpath("//ol[@class='commentlist']/li/div/div[@class='comment-text']/p[@class='meta']/strong[@class='woocommerce-review__author']/text()").extract()
       # img_src = response.xpath("//ol[@class='commentlist']/li/div/div[@class='img-thumbnail']/img/@src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@class='header-main']/div[@class='container']/div[@class='header-center']/div[@class='logo']/a/@href").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], category,
                                         servicename, reviews[item], None, website_name)
            servicename1.save()





