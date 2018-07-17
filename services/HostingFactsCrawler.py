from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
from lxml import etree

class HostingFactsCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(HostingFactsCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response1):
        reviews = []
        print("review from Hostingfacts.com                    ", self.link["url"])
        # https://hostingfacts.com/hosting-reviews/hostgator-wordpress-managed/
        data = response1.xpath(".//div[@class='user-review']").extract()

        img_src = response1.xpath(
            "//div[@class='sidebar-padder']/aside/img[@class='img-responsive banner-image center-block']/@src").extract()
        website_name = response1.xpath("//div[@class='navbar-header']/a[@class='navbar-brand']/text()").extract()

        for content in data:
            response = etree.HTML(content)
            etree.dump(response)
            reviews = response.xpath('//div[@class="user-review-content"]/p/text()')
            reviewdata = ""
            for review in reviews:
                reviewdata += review + "/n"
            ratings = response.xpath("//span[@class='user-review-rating']/span[@class='value']/text()")[0]
            dates = response.xpath("//span[@class='user-review-meta']/text()")[0]
            headings = response.xpath("//p[@class='user-review-title']/text()")[0]
            authors = response.xpath("//p[@class='user-review-name']/a/span/text()")[0]
            servicename1 = ServiceRecord(response1.url, ratings, headings, dates, authors,
                                     "category", self.servicename, reviews, img_src, website_name);
            self.save(servicename1)
        # print "reviews ", len(reviews)
        # print(" ratings ", len(ratings))
        #
        # print("headings ", len(headings), headings)
        # print("dates ", len(dates))
        # print("authours ", len(authors))
        # for item in range(0, len(reviews)):

        self.pushToServer()