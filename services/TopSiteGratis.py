from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request


from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class TopSiteGratis(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(TopSiteGratis,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []



        for node in response.xpath(
                "//div[@class='reviews product-reviews']/div[@class='item']/p[@class='excerpt']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/div[@class='right-block']/div[@class='ratings']/span[@class='rate_False']/span").extract()
        dates = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/meta[@itemprop='datePublished']/@content").extract()
        authors = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/div[@class='author-info']/a/text()").extract()
        img_src = response.xpath(
            "//div[@class='row product']/div[@class='col-md-3 text-center']/img[@class='log_img']/@src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name1 = response.xpath("//div[@class='footer']/div[@class='row']/div[@class='col-md-7 text-right']/text()").extract()
        website_name = []
        i = 0
        while(i< len(website_name1)):
            c = website_name1[1].split(" ")
            website_name.append(c[12])
            break
            i = i+1

        print("Reviews ", len(reviews))
        print("Authors ", len(authors))
        print("Rating ", len(ratings))
        print("Dates ", len(dates))
        print("img_src ", len(img_src))
        print("websites ", len(website_name), website_name[0])
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], "",
                                         self.servicename, reviews[item], img_src[0], website_name[0])
            self.save(servicename1)
        self.pushToServer()





