from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
# https://www.joomlahostingreviews.com/joomla-hosting/bluehost-review.html
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


        for node in response.xpath(
                "//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/div[@class='description jrReviewComment']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrRatingInfo']/div[@class='jrTableGrid jrRatingTable']/div[@class='jrRow'][1]/div[@class='jrCol jrRatingValue']/text()").extract()
        dates = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewInfo']/time/text()").extract()
        authors = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrUserInfo']/span/span/span/text()").extract()
        img_src = response.xpath(
            "//div[@class='jr-detail-row1']/div[@class='jr-detail-row1-col1']/div[@class='jr-detail-row1-col1-image']/img/@src").extract()[0]
        headings = response.xpath("//div[@class='jr-layout-outer jrRoundedPanelLt']/div[@class='jr-layout-inner jrReviewContainer']/div[@class='jrReviewContent']/h4[@class='jrReviewTitle']/text()").extract()
        website_name1 = self.link["url"].split("/")
        website_name1 =  (website_name1[len(website_name1) - 1]).split("-")
        website_name =  'https://' +website_name1[0]+ '.com'
        name="joomlahostingreviews.com"
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], img_src, website_name, name)
            self.save(servicename1)
        self.pushToServer()





