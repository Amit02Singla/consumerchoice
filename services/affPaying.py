from model.Servicemodel import ServiceRecord
from lxml import etree
class affPaying():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        #
        for node in response.xpath("//div[3]/p[1]"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='s_rate_mid']/span/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@class='s_comment_date']/meta[@itemprop='datePublished']/@content").extract()
        authors = response.xpath("//div/dl[@class='s_comment']/h4/span/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()


