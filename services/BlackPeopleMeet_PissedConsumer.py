from model.Servicemodel import ServiceRecord
from lxml import etree

class BlackPeopleMeet_PissedConsumer():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from blackpeoplemeet.pissedconsumer.com")
        for node in response.xpath("//div[@class='middleware-review-container'][1]/div/div[@class='f-component-info']/div[@class='f-component-text']/div[@class='overflow-text']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//body/section[@class='row body inside']/section[@class='comments-block']/section[@class='commentblock  ']/div[@class='comment  ']/ul[@class='postby']/li[2]/span[@class='smallStars']/@data-score").extract()
        dates = response.xpath("div[@class='middleware-review-container']/div/div[@class='f-component-info']/div[@class='f-component-info-header']/time[@class='post-time secondary-info']/text()").extract()
        # headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        # authors = response.xpath("//div[@class='cust_review']/table/tbody/tr[3]/td[@class='customer']").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        # img_src = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/img[@class='avatar avatar-74 photo']/@src").extract()
        #print("Reviews ", len(reviews), reviews)
        # print("Headings ", len(headings), headings)
        # print("Authors ", len(authors), authors)
        #print("Rating ", len(ratings), ratings)
        #print("Dates ", len(dates), dates)
        # print("Img_src ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], None,
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()





