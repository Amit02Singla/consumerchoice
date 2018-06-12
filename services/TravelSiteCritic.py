from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
from lxml import etree
# http://travelsitecritic.com/reviews/1-2/smartfares-reviews/
class TravelSiteCritic(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename
        print(" travelsitecritic.com")
        for node in response.xpath(
                "//div[@id='comments']/ol[@class='comment-list']/li/div[@class='comment-content']"):
            reviews1.append(node.xpath('string()').extract());
        ratings1 = response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/div[@class='comment-content']/div[@class='ratingblock ']/div[@class='ratingstars ']/div/div[@class='starsbar gdsr-size-20']/div[@class='gdouter gdheight']/div/@style").extract()
        dates = response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/div[@class='comment-header']/div[@class='comment-meta commentmetadata']/a/text()").extract()
        authors1 = response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/div[@class='comment-header']/div[@class='comment-author vcard']").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@id='title-area']/p[@id='title']/a/@href").extract()
        # img_src = response.xpath(
        #     "//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()
        i=0
        rev = []
        authors = []
        for content in authors1:
            root = etree.HTML(content)
            # print(len(root.xpath("//cite[@class='fn']")))
            if(len(root.xpath("//cite[@class='fn']/a"))>0):
                authors.append(root.xpath("//cite[@class='fn']/a/text()")[0])

            else:
                authors.append(root.xpath("//cite[@class='fn']/text()")[0])
            # print(content)
        while(i<len(reviews1)):
            rev = (reviews1[i][0].split("cast)"))
            # print("rev ", rev)
            reviews.append(rev[1])
            i = i+1
        ratings = []
        j = 0
        while j < len(ratings1):
            c= int(getStarts(ratings1[j]))
            ratings.append((c)/20.0)
            j = j + 1

        # print("Reviews ", len(reviews), reviews)
        # # print("Headings ", len(headings), headings)
        # print("Authors ", len(authors), authors)
        # print("Rating ", len(ratings), ratings)
        # print("Dates ", len(dates), dates)
        # print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], category,
                                         servicename, reviews[item], None, website_name)
            servicename1.save()



