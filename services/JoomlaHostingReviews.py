from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request

from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler

class JoomlaHostingReviews(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(JoomlaHostingReviews,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        reviews1 = []

        # https: // www.webhostinghero.com / reviews / bluehost /
        for node in response.xpath(
                "//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/div[@class='description jrReviewComment']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrRatingInfo']/div[@class='jrTableGrid jrRatingTable']/div[@class='jrRow'][1]/div[@class='jrCol jrRatingValue']/text()").extract()
        dates = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewInfo']/time/text()").extract()
        authors = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrUserInfo']/span/span/span/text()").extract()
        img_src = response.xpath(
            "//div[@class='jr-detail-row1']/div[@class='jr-detail-row1-col1']/div[@class='jr-detail-row1-col1-image']/img/@src").extract()[0]
        headings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/h4[@class='jrReviewTitle']/text()").extract()
        website_name = response.xpath("//div[@class='platform-content']/div[@class='moduletable -footer']/div[@class='custom-footer']/p/a/text()").extract()
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], img_src, website_name[0])
            self.save(servicename1)
        self.pushToServer()





