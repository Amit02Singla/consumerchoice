from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
# https://www.trustpilot.com/review/kiwi.com
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class TrustPilot(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(TrustPilot,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []

        for node in response.xpath(
                "//section[@class='review__content']/div[@class='review-content']/div[@class='review-content__body']/p[@class='review-content__text']"):
            reviews.append(node.xpath('string()').extract());
        ratings1 =  response.xpath("//div[@class='review-content']/div[@class='review-content__header']/div[@class='review-content-header']/div/@class").extract()
        # dates = response.xpath("//div[@class='review-content-header']/div[@class='review-content-header__dates']/div[@class='v-popover']/span[@class='trigger']/time/@title").extract()
        authors = response.xpath("//aside[@class='review__consumer-information']/a[@class='consumer-information']/div[@class='consumer-information__details']/div[@class='consumer-information__name']/text()").extract()
        headings = response.xpath("//section[@class='review__content']/div[@class='review-content']/div[@class='review-content__body']/h2[@class='review-content__title']/a[@class='link link--large link--dark']/text()").extract()
        website_name = "trustpilot.com"
        # img_src = response.xpath(
        #     "//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()
        ratings = []
        i = 0
        while i < len(ratings1):
            ratings.append(getStarts(ratings1[i]))
            i = i + 3
        ratings = map(lambda foo: foo.replace('-', ''), ratings)

        # print("Img_src ", len(img_src), img_src)
        print("reviews count ", len(reviews))
        print("authors", len(authors))
        print("ratings ", len(ratings))
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], None, authors[item], self.category,
                                         self.servicename, reviews[item], None, website_name)
            self.save(servicename1)

        next_page = response.xpath("//nav[@class='pagination-container AjaxPager']/a[@class='button button--primary next-page']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()
