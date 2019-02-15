from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
from lxml import etree
#Todo: WIP giving error : Done
class ReviewCentreCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        # https://www.reviewcentre.com/Dating-Sites/Elite-Singles-www-elitesingles-co-uk-www-hospiconsultant-com-reviews_3802989#Reviews
        for node in response.xpath("//div[@id='ItemReviewsContent']/div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']/p[2]"):
            reviews.append(node.xpath('string()').extract());
        authors1 = response.xpath("//div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']").extract()
        headings = response.xpath("//div[@id='ItemReviewsContent']/div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']/h3/a/text()").extract()
        website_name = response.xpath("/html/head/meta[9]/@content").extract()
        img_src = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()
        dates = response.xpath("//div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']/p/span[1]/text()").extract()
        ratings1 = response.xpath("//div[@class='ReviewCommentContent']/div[@class='ReviewBoxLeftContent']/div[1]/@class").extract()
        ratings1 = map(lambda foo: foo.replace('starsLarge RatingStarsLarge_', ''), ratings1)
        ratings1 = map(lambda foo: foo.replace('-', ''), ratings1)
        i=0
        ratings= []
        authors = []
        authors2 = []
        for content in authors1:
            root = etree.HTML(content)
            # print(content)
            if(len(root.xpath("//p/span[2]"))>0):
                authors.append(root.xpath("//p/span[2]/text()")[0])
            else:
                authors.append("")
            authors = map(lambda foo: foo.replace('\n', ''), authors)
            authors = map(lambda foo: foo.replace('by', ''), authors)
            authors = map(lambda foo: foo.replace('                     ', ''), authors)
            authors = map(lambda foo: foo.replace('                ', ''), authors)
        i=0
        while(i < len(authors)):
            auth = authors[i].split(" (")
            authors2.append(auth[0])
            i =i +1

        i=0
        while i< len(ratings1):
            ratings.append(round(float(ratings1[i])/10.0, 1))
            i= i+1

        # print("img ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates, authors2[item], self.category,
                                         self.servicename, reviews[item], None, website_name)
            servicename1.save()

        # next_page = response.xpath("//div[@class='pagination']/ul[@id='yw2']/li[@class='next']/a/@href").extract()
        # if next_page is not None:
        #     next_page_url = "".join(next_page[0])
        #     print(next_page_url)
        #     if next_page_url and next_page_url.strip():
        #         yield response.follow(url=next_page_url, callback=self.parsing)
