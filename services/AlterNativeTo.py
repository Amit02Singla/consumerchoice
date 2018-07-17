from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
from lxml import etree

# TODO: need to get next page url from javascript
#https://alternativeto.net/software/cyberghost/reviews/
class AlterNativeTo(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(AlterNativeTo,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        headings = []
        ratings = []
        dates = []
        authors = []
        reviews1 = []
        data = response.xpath("//div[@id='discussionsList']/div[@class='discussionApp']").extract()
        print("review from   ", self.link["url"])
        for content in data:
            root = etree.HTML(content)
            if(len(root.xpath("//div/div[@class='col-xs-11']/div[@class='do-not-break forumText wmd']"))>0):
                reviews.append(root.xpath("//div/div[@class='col-xs-11']/div[@class='do-not-break forumText wmd']/text()")[0])
            if(len(root.xpath("//div/div[@class='col-xs-11']/h3"))>0):
                headings.append(root.xpath("//div/div[@class='col-xs-11']/h3/text()")[0])
            else:
                headings.append("")
            if (len(root.xpath("//div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/div[@class='threadMeta']/span[2]/span")) > 0):
                dates.append(root.xpath("//div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/div[@class='threadMeta']/span[2]/span/text()")[0])
            else :
                dates.append("")
            if (len(root.xpath("//div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/span[@class='threadMeta']/a")) > 0):
                authors.append(root.xpath("//div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/span[@class='threadMeta']/a/text()")[0])
            else :
                authors.append("")
            if (len(root.xpath("//div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/span[@class='threadMeta']/div[@class='stars']/span[@class='star on']")) > 0):
                print len(root.xpath("//div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/span[@class='threadMeta']/div[@class='stars']/span[@class='star on']"))
                ratings.append(len(root.xpath("//div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/span[@class='threadMeta']/div[@class='stars']/span[@class='star on']")))
            else :
                ratings.append("")


        # ratings = response.xpath("//ol[@class='commentlist']/li/div[@class='commbox']/div[@class='comment-content-withreview']/div[@class='user_reviews_view simple_color']/div[@class='user_reviews_view_box']/div[@class='user_reviews_view_score']/div[@class='userstar-rating']/span").extract()
        # dates = response.xpath("//div[@class='discussionApp']/div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/div[@class='threadMeta']/span[2]/span/text()").extract()
        # authors = response.xpath("//div[@class='discussionApp']/div/div[@class='col-xs-11']/div[@class='threadMetaWrapper meta']/span[@class='threadMeta']/a/text()").extract()
        img_src = response.xpath(
            "//div[@class='row']/div[@class='col-sm-12']/div[@class='like-box-wrapper']/div[@class='image-wrapper']/img/@data-src").extract()
        if(len(img_src)<1):
            img_src = None
            print("img_src ",img_src)
        else:
            img_src = img_src[0]
            print("img_src ", len(img_src), img_src)
        # headings = response.xpath("//div[@class='discussionApp']/div/div[@class='col-xs-11']/h3/text()").extract()
        website_name = response.xpath("//div[@class='row']/div[@class='col-sm-6 col-lg-4 col-md-5 hidden-xs']/a[@class='brand']/img/@alt").extract()[0]
        print("Reviews ",  len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("ratings ", len(ratings), ratings)
        print("Heading ", len(headings), headings)
        print("Dates ", len(dates), dates)

        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], dates[item], authors[item], "",
                                         self.servicename, reviews[item], img_src, website_name)
            self.save(servicename1)
        self.pushToServer()





