from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
# https://www.influenster.com/reviews/hotwire
#Todo: need to get rating : Done

class InfluensterCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(InfluensterCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        reviews1 = []
        ratings1 = []
        ratings = []


        for node in response.xpath("//div[@class='content-item review-item']/div[@class='content-item-body review-item-body']/div[@class='content-item-text review-text']"):
            reviews.append(node.xpath('string()').extract());
        ratings1 = response.xpath("//div[@class='review-item-stars']/div[@class='avg-stars  ']/div/@content").extract();
        dates1 = response.xpath("//div[@class='content-item review-item']/div[@class='content-item-body review-item-body']/div[@class='content-item-header review-item-header']/a[@class='date']/text()").extract()
        authors = response.xpath("//div[@class='content-item review-item']/div[@class='content-item-author-info']/a/div[@class='author-name']/text()").extract()
        img_src = response.xpath("//div[@class='product-images']/div[@class='product-ugc']/a[@class='product-ugc-media']/img/@src").extract()[0]
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name1 = self.link["url"].split("/")
        website_name = 'https://' + website_name1[len(website_name1) - 1] + '.com'

        name="influenster.com"
        dates = []
        i=0
        while i< len(dates1):
            dat =  dates1[i].split(',')
            dates.append(dat[0].strip())
            i= i+1
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings1), ratings1)
        print("Dates ", len(dates), dates)
        print("reviews ", len(reviews))
        print("websites ", len(website_name), website_name)
        print('imgsrc ', img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings1[item], None, dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], img_src, website_name, name)
            self.save(servicename1)

        next_page = response.xpath(
            "//div[@class='reviews-list-content']/div[@class='paginator']/a[@class='review-pagination next']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()



