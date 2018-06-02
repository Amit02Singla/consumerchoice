from model.Servicemodel import ServiceRecord
from lxml import etree

#TODO etree complete auther extraction: Refer sandy
#URL https://www.comparitech.com/vpn/reviews/expressvpn/

class CompariTech():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from comparitech.com")
        for node in response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/div[@class='comment-content']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='box col-12 review-title']/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-metadata']/a/time/text()").extract()
        # headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        authors1 = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        img_src = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/img[@class='avatar avatar-74 photo']/@src").extract()
        authors = []
        for content in authors1:
            root = etree.HTML(content)

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         category, servicename, reviews[item], img_src, website_name)
            servicename1.save()






