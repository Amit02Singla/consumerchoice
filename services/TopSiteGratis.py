from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request



class TopSiteGratis(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename

        for node in response.xpath(
                "//div[@class='reviews product-reviews']/div[@class='item']/p[@class='excerpt']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/div[@class='right-block']/div[@class='ratings']/span[@class='rate_False']/span").extract()
        dates = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/meta[@itemprop='datePublished']/@content").extract()
        authors = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/div[@class='author-info']/a/text()").extract()
        img_src = response.xpath(
            "//div[@class='reviews product-reviews']/div[@class='item']/div[@class='left-block']/div[@class='product-info']/div[@class='img pull-left']/img/@src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name1 = response.xpath("//div[@class='footer']/div[@class='row']/div[@class='col-md-7 text-right']/text()").extract()
        website_name = []
        i = 0
        while(i< len(website_name1)):
            c = website_name1[1].split(" ")
            website_name.append(c[12])
            break
            i = i+1

        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], category,
                                         servicename, reviews[item], img_src, website_name)
            servicename1.save()





