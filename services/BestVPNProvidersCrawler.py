from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts

# https://bestvpnprovider.co/vyprvpn-review/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class BestVPNProvidersCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BestVPNProvidersCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        reviews1 = []


        #TODO: Done
        for node in response.xpath("//div[@class='wpcr3_review_item']/div[@class='wpcr3_item wpcr3_product']/div/blockquote[@class='wpcr3_content']"):
            reviews.append(node.xpath('string()').extract());
        ratings1 = response.xpath("//div[@class='wpcr3_item wpcr3_product']/div/div[@class='wpcr3_review_ratingValue']/div[@class='wpcr3_rating_style1']/div[@class='wpcr3_rating_style1_base ']/div/@style").extract()
        ratings = []
        j = 0
        while j < len(ratings1):
            c = int(getStarts(ratings1[j]))
            ratings.append((c) / 20.0)
            j = j + 1
        dates = response.xpath("//div[@class='wpcr3_item wpcr3_product']/div/div[@class='wpcr3_review_datePublished']/text()").extract()
        authors = response.xpath("//div[@class='wpcr3_item wpcr3_product']/div/div[@class='wpcr3_review_author']/span[@class='wpcr3_caps']/text()").extract()
        img_src = response.xpath(
            "//div[@class='columngrid-3']/div[@class='text-center']/img/@src").extract()[0]
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@class='row'][1]/div[@class='columngrid-8 pad-small text-right']/a/span[@class='color-sec-ft']/text()").extract()[0]
        print("imgsrc   ", img_src)
        print("website name  ", website_name)
        name="bestvpnprovider.co";
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], img_src, website_name, name)
            self.save(servicename1)
        self.pushToServer()





