from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request


#https://alternativeto.net/software/cyberghost/reviews/
class AlterNativeTo(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)
# TODO Done
    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename

        for node in response.xpath(
                "//div[@class='discussionApp']/div/div[@class='col-xs-11']/div[@class='do-not-break forumText wmd']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-content-withreview']/div[@class='user_reviews_view simple_color']/div[@class='user_reviews_view_box']/div[@class='user_reviews_view_score']/div[@class='userstar-rating']/span").extract()
        dates = response.xpath("//div[@class='discussionApp']/div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/div[@class='threadMeta']/span[2]/span/text()").extract()
        authors = response.xpath("//div[@class='discussionApp']/div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/span[@class='threadMeta']/a/text()").extract()
        img_src = response.xpath(
            "//div[@class='row']/div[@class='col-sm-12']/div[@class='like-box-wrapper']/div[@class='image-wrapper']/img/@data-src").extract()
        headings = response.xpath("//div[@class='discussionApp']/div/div[@class='col-xs-11']/h3/text()").extract()
        website_name = response.xpath("//div[@class='row']/div[@class='col-sm-6 col-lg-4 col-md-5 hidden-xs']/a[@class='brand']/img/@alt").extract()
        # print("Reviews ", len(reviews), reviews)
        # print("Authors ", len(authors), authors)
        # print("Heading ", len(headings), headings)
        # print("Dates ", len(dates), dates)
        # print("img_src ", len(img_src), img_src)
        # print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], dates[item], authors[item], category,
                                         servicename, reviews[item], img_src, website_name)
            servicename1.save()





