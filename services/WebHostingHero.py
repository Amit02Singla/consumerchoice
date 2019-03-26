from model.Servicemodel import ServiceRecord
from utils.utils import getStarts
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
from lxml import etree
class WebHostingHero(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(WebHostingHero,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("review from webhostinghero.com")
        for node in response.xpath("//div[@class='user-review-box boxed-content']/div[@class='row']/div[@class='col-12 review-description']"):
            reviews.append(node.xpath('string()').extract());
        temp_headings =  response.xpath("//div[@class='user-review-box boxed-content']/div[@class='row']/div[@class='col-12 review-rating']").extract()
        headings = []
        for content in temp_headings:
            root = etree.HTML(content)
            if (len(root.xpath("//h4/text()")) == 0):
                headings.append("")
            else:
                headings.append(root.xpath("//h4/text()")[0])
        ratings1 = response.xpath("//div[@class='user-review-box boxed-content']/div[@class='row']/div[@class='col-12 review-rating']/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@class='user-review-box boxed-content']/div[@class='row']/div[@class='col-12 review-meta'][1]/span[@class='review-date']/text()").extract()
        authors = response.xpath("//div[@class='col-sm-12 user-review-container']/div[@class='user-review-box boxed-content']/div[@class='row']/div[@class='col-12 author']/span/text()").extract()
        website_name = response.xpath("//div[@class='row']/nav[@id='sidebar-reviews']/div[@class='row']/div[@class='col-sm-6 col-lg-12 widget rating-summary']/div[@class='boxed-content']/div[@class='visit-link']/a/@href").extract()[0]
        img_src = response.xpath("//div[@class='row']/nav[@id='sidebar-reviews']/div[@class='row']/div[@class='col-sm-6 col-lg-12 widget rating-summary']/div[@class='boxed-content']/div[@class='visit-link']/a/img/@src").extract()
        ratings = []
        name = "webhostinghero.com"
        for i in range(len(ratings1)):
            c= int(ratings1[i])/2.0
            ratings.append(str(c))
        print("Reviews ", len(reviews))
        print("Headings ", len(headings), )
        print("Authors ", len(authors), )
        print("Rating ", len(ratings),ratings)
        print("Dates ", len(dates), dates)
        print("Img_src ", len(img_src), img_src)
        print("website ", website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], img_src[0], website_name, name)
            self.save(servicename1)

        next_page = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()




