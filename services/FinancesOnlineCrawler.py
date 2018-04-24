from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
class FinancesOnlineCrawler(Spider):
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        self.category = category
        self.servicename = servicename
        reviews = []
        # https://reviews.financesonline.com/p/vyprvpn/
        for node in :
            reviews.append(node.xpath('string()').extract());
        dates =
        headings =
        authors =
        img_src =
        website_name =  
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                          servicename, reviews[item],img_src,website_name)
            servicename1.save()
