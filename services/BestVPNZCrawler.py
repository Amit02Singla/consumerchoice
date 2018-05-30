from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree

#TODO Author value need to check
class BestVPNZCrawler(Spider):
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        self.category = category
        self.servicename = servicename
        reviews = []
        # https://www.bestvpnz.com/expressvpn/
        for node in  response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/article/div[@class='comment-content']"):
            reviews.append(node.xpath('string()').extract());
        dates =  response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author-info']/div[@class='entry-meta comment-metadata']/a/time/text()").extract()
        authors =   response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author-info']/div[@class='comment-author vcard']/cite[@class='fn']/text()").extract()
        img_src =  response.xpath("//div[@class='page-header-image-single grid-containergrid-parent']/img[@class='attachment-full size-full wp-post-image']/@src").extract()
        website_name =  response.xpath("/html/head/link[8]/@title").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                          servicename, reviews[item],img_src,website_name)
            servicename1.save()
