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
        #https://www.joomlahostingreviews.com/joomla-hosting/bluehost-review.html
        for node in response.xpath(
                "//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/div[@class='description jrReviewComment']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrRatingInfo']/div[@class='jrTableGrid jrRatingTable']/div[@class='jrRow'][1]/div[@class='jrCol jrRatingValue']/text()").extract()
        dates = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewInfo']/time/text()").extract()
        authors = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrUserInfo']/span/span/span/text()").extract()
        headings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/h4[@class='jrReviewTitle']/text()").extract()
        website_name = response.xpath("//div[@class='platform-content']/div[@class='moduletable -footer']/div[@class='custom-footer']/p/a/text()").extract()[0].split(".")[1]
        name="oomlahostingreviews.com"
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], None, website_name, name)
            servicename1.save()





