from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request



class RevexCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename
        # https://revex.co/bittrex/
        for node in response.xpath(
                "//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-content-withreview']/div[@class='user_reviews_view simple_color']/div[@class='user_reviews_view_proscons']/div[@class='comm_text_from_review']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-content-withreview']/div[@class='user_reviews_view simple_color']/div[@class='user_reviews_view_box']/div[@class='user_reviews_view_score']/div[@class='userstar-rating']/span").extract()
        dates = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-author vcard clearfix']/div[@class='comm_meta_wrap']/span[@class='time']/text()").extract()
        authors = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-author vcard clearfix']/div[@class='comm_meta_wrap']/span[@class='fn']/a/text()").extract()
        website_name = response.xpath("//div[@class='logo_section_wrap']/div[@class='logo-section header_first_style clearfix']/div[@class='logo']/a/@href").extract()[0].split("//")[1]
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], category,
                                         servicename, reviews[item], None, website_name)
            servicename1.save()





