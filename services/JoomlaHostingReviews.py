from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request



class JoomlaHostingReviews(Spider):

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
                "//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/div[@class='description jrReviewComment']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrRatingInfo']/div[@class='jrTableGrid jrRatingTable']/div[@class='jrRow'][1]/div[@class='jrCol jrRatingValue']/text()").extract()
        dates = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewInfo']/time/text()").extract()
        authors = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrUserInfo']/span/span/span/text()").extract()
        # img_src = response.xpath(
        #     "//div[@id='posted']/div[@class='blc']/div[@class='mc'][1]/a[@class='blcAvatar']/img/@src").extract()
        headings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/h4[@class='jrReviewTitle']/text()").extract()
        website_name = response.xpath("//div[@class='platform-content']/div[@class='moduletable -footer']/div[@class='custom-footer']/p/a/text()").extract()
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        # print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], category,
                                         servicename, reviews[item], None, website_name)
            servicename1.save()





