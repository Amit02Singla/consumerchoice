from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts

# http://www.viewpoints.com/Kayak-com-reviews
class ViewPoints(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename

        for node in response.xpath(
                "//div[@class='pr-contents-wrapper']/div[@class='pr-review-wrap']/div[@class='pr-review-main-wrapper']/div[@class='pr-review-text']/p[@class='pr-comments']"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/span[@class='pr-rating pr-rounded']/text()").extract()
        dates = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-author-date pr-rounded']/text()").extract()
        authors = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-author']/div[@class='pr-review-author-info-wrapper']/p[@class='pr-review-author-name']/span/text()").extract()
        headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@class='grid-container']/div[@class='grid-featured']/div[@class='globalNav']/a[@class='logo header']/img/@alt").extract()
        # img_src = response.xpath(
        #     "//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()


        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], None, authors[item], category,
                                         servicename, reviews[item], None, website_name)
            servicename1.save()
        next_page = response.xpath(
            "//div[@class='pr-page-nav-wrapper']/p[@class='pr-page-nav']/span[@class='pr-page-next']/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)


