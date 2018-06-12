from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request



class Revex(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename

        for node in response.xpath(
                "//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-content-withreview']/div[@class='user_reviews_view simple_color']/div[@class='user_reviews_view_proscons']/div[@class='comm_text_from_review']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-content-withreview']/div[@class='user_reviews_view simple_color']/div[@class='user_reviews_view_box']/div[@class='user_reviews_view_score']/div[@class='userstar-rating']/span").extract()
        dates = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-author vcard clearfix']/div[@class='comm_meta_wrap']/span[@class='time']/text()").extract()
        authors = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-author vcard clearfix']/div[@class='comm_meta_wrap']/span[@class='fn']/a/text()").extract()
        img_src = response.xpath(
            "//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-author vcard clearfix']/img[@class='func-um_user gravatar avatar avatar-50 um-avatar um-avatar-default']/@src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@class='logo_section_wrap']/div[@class='logo-section header_first_style clearfix']/div[@class='logo']/a/@href").extract()
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], category,
                                         servicename, reviews[item], img_src, website_name)
            servicename1.save()





