from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts

# https://bestvpnprovider.co/vyprvpn-review/

class BestVPNProvidersCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename

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
            "//div[@class='columngrid-9']/div[@id='quick']/div[@class='columngrid-3']/div[@class='text-center']/img/@src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("///head/meta[10]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], category,
                                         servicename, reviews[item], img_src, website_name)
            servicename1.save()





