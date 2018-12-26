from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
from lxml import etree


class ReviewCentre(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ReviewCentre,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []

        print ("reviews from ReviewCentre.com    ", self.link["url"])
        for node in response.xpath(
                "//div[@id='ItemReviewsContent']/div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']/p[2]"):
            reviews.append(node.xpath('string()').extract());
        ratings1 =  response.xpath("//div[@id='ItemReviewsContent']/div/div[@class='ReviewCommentContent']/div[@class='ReviewBoxLeftContent']/div[1]/@class").extract()
        dates = response.xpath("//div[@id='ItemReviewsContent']/div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']/p/span[1]/text()").extract()
        authors1 = response.xpath("//div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']").extract()
        authors = []
        ratings = []
        j = 0
        while j < len(ratings1):
            ratings.append(getStarts(ratings1[j]))
            j = j + 1
        authors2= []
        for content in authors1:
            root = etree.HTML(content)
            if(len(root.xpath("//p/span[2]/text()"))>0):
                authors.append(root.xpath("//p/span[2]/text()")[0])
            else:
                authors.append("")
        authors = map(lambda foo: foo.replace('\n        \n            ', ' '), authors)
        i=0
        while( i< len(authors)):
            if( authors[i] == '' ):
                authors2.append("")
            else:
                c=authors[i].split(" ");
                authors2.append(c[2])
            i=i+1
        headings = response.xpath("//div[@id='ItemReviewsContent']/div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']/h3/a/text()").extract()
        website_name = "www.reviewcentre.com"

        print("Reviews ", len(reviews), reviews)
        print("Headings ", len(headings), headings)
        print("Authors ", len(authors2), authors2)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)

        print("wenbsite ", website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], None, authors2[item], "",
                                         self.servicename, reviews[item], None, website_name)
            self.save(servicename1)

        next_page = response.xpath("//div[@class='pagination']/ul[@id='yw2']/li[@class='next']/a/@href").extract()
        if next_page is not None:
            if len(next_page)>0 :
                next_page_url = "".join(next_page[0])
                print(next_page_url)
                if next_page_url and next_page_url.strip():
                    yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer();
