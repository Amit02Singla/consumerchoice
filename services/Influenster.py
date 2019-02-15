from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request



class Influenster(Spider):

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
                "//div[@class='content-item review-item']/div[@class='content-item-body review-item-body']/div[@class='content-item-text review-text']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='content-item review-item']/div[@class='content-item-body review-item-body']/div[@class='review-item-stars']/div[@class='avg-stars ']/div/@content").extract()
        dates = response.xpath("//div[@class='content-item review-item']/div[@class='content-item-body review-item-body']/div[@class='content-item-header review-item-header']/a[@class='date']/text()").extract()
        authors = response.xpath("//div[@class='content-item review-item']/div[@class='content-item-author-info']/a/div[@class='author-name']/text()").extract()
        img_src = response.xpath(
            "//div[@class='content-item review-item']/div[@class='content-item-author-info']/a/div[@class='avatar avatar-large']/img/@data-lazy-src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//head/meta[7]/@content").extract()
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], img_src, website_name)
            servicename1.save()

        next_page = response.xpath(
            "//div[@class='reviews-list-content']/div[@class='paginator']/a[@class='review-pagination next']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)



