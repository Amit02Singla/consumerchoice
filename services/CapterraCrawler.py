from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler


class CapterraCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(CapterraCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("Reviews from Capterra.con     ", self.link["url"] )
        # https://www.capterra.com/p/170765/ExpressVPN/
        for node in response.xpath('//div[@class="review-comments  color-text"]'):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='overall-rating-container']/span[@class='overall-rating']/span/text()").extract()
        headings = response.xpath("//div[@class='cell seven-eighths  palm-one-whole']/h3/q/text()").extract()
        dates = response.xpath("//div[@class='grid']/div[@class='cell one-eighth  palm-one-whole']/div[@class='quarter-margin-bottom  micro  color-gray  weight-normal  text-right  palm-text-left']/text()").extract()
        if(response.xpath("//div[@class='spotlight-listing-thumbnail-container']/div[@class='thumbnail  no-hover  listing-thumbnail']/img/@src")):
            img_src = response.xpath("//div[@class='spotlight-listing-thumbnail-container']/div[@class='thumbnail  no-hover  listing-thumbnail']/img/@src").extract()[0]
        else:
            img_src = ""
        website_name = "capterra.com"
        authors = response.xpath("//div[@class='reviewer-details']/div[1]/text()").extract()
        print("Reviews ", len(reviews))
        print "imgsrccccc   ", img_src
        print("ratings ", len(ratings))
        print("Heading ", len(headings))
        print("Dates ", len(dates))
        print("Authors ", len(authors))
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            service1 = ServiceRecord(response.url, ratings[item],headings[item], dates[item], authors[item], self.category,
                          self.servicename, reviews[item], img_src,website_name);
            self.save(service1)
        next_page = response.xpath("//div[@class='base-margin-bottom']/a/@data-url").extract()
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()

