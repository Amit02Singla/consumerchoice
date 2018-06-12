from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request



class Hellopeter(Spider):

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
                "//div[@class='mt-0 grid__full py-2']/div[@class='grid']/div[@class='review-card px-0 review-card--verbose']/div[@class='grid__full review-card__info grid__5-6ths--sm m-0 ml-3 p-3 review-card__info--verbose']/h5[@class='text-nowrap-ellipsis mt-1 mb-2 review-card__title']/a"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='mt-0 grid__full py-2']/div[@class='grid']/div[@class='review-card px-0 review-card--verbose']/div[@class='grid__full review-card__info grid__5-6ths--sm m-0 ml-3 p-3 review-card__info--verbose']/div/@title").extract()
        dates = response.xpath("//div[@class='mt-0 grid__full py-2']/div[@class='grid']/div[@class='review-card px-0 review-card--verbose']/div[@class='grid__full review-card__info grid__5-6ths--sm m-0 ml-3 p-3 review-card__info--verbose']/div[@class='mt-1 text-muted text-xsmall text-nowrap review-card__timestamp']/text()").extract()
        authors = response.xpath("//div[@class='mt-0 grid__full py-2']/div[@class='grid']/div[@class='review-card px-0 review-card--verbose']/div[@class='grid__1-6th hidden--xs-down review-card__profile pt-4']/a[@class='text-center text-muted']/div[@class='text-nowrap-ellipsis'][1]/text()").extract()
        img_src = response.xpath(
            "//iv[@class='mt-0 grid__full py-2']/div[@class='grid']/div[@class='review-card px-0 review-card--verbose']/div[@class='grid__1-6th hidden--xs-down review-card__profile pt-4']/a[@class='text-center text-muted']/img[@class='mx-auto review-card__avatar']/@src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@class='container ariane']/ol/li[1]/a/@href").extract()
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                                         servicename, reviews[item], img_src, website_name)
            servicename1.save()





