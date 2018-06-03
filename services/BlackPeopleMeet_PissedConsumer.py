from model.Servicemodel import ServiceRecord
from lxml import etree


#TODO ask sahil

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
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], None,
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()





