from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class WhoIsHostingCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(WhoIsHostingCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #print("whoishostingthis.com")
        # https://www.whoishostingthis.com/hosting-reviews/bluehost/
        authors = response.xpath("//div[@class='author']/span[@class='name']/text()").extract()
        img_src = response.xpath("//div[@class='host-info wcc']/a[1]/img[@class=' logo']/@src").extract()
        website_name = response.xpath("//div[@class='mobile']/a[@class='home']/img[@class='logo']/@alt").extract()
        ratings1 = response.xpath("//div[@class='user-info pure-u-1']/img[@class='stars overall']/@alt").extract()
        if len(ratings1) == 0 :
            ratings1 = response.xpath("//div[@class='rating pure-u-1 pure-u-lg-1-3']/img[@class='stars overall']/@alt").extract()
        for node in response.xpath('//div[@class="comment pure-u-1 wcc"]'):
            reviews.append(node.xpath('string()').extract());
        if len(reviews) == 0:
            for node in response.xpath('//div[@class="comment pure-u-1 pure-u-lg-2-3 wcc"]'):
                reviews.append(node.xpath('string()').extract());
        #print("  reviews   ", reviews)
        dates = response.xpath("//div[@class='user-info pure-u-1']/time[@class='published']/text()").extract()
        print("reviews",len(reviews))
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings1[item], None, None, authors[item], "",
                          self.servicename, reviews[item],img_src,website_name);
            self.save(servicename1)

        next_page = response.xpath("//div[@class ='see-more']/a/@ href").extract()
        if len(next_page) == 0:
            next_page = response.xpath("//div[@class ='pure-u-1 pure-u-lg-1-4 next']/a/@ href").extract()
        if next_page is not None:
            next_page_url ="".join(next_page)
            if next_page_url and next_page_url.strip():
                #print(type(next_page_url))
                #print(next_page_url)
                #yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()