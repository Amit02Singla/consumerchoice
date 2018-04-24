from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
class DatingSitesReviewsCrawler(Spider):
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        self.category = category
        self.servicename = servicename
        reviews = []
        # https://www.datingsitesreviews.com/staticpages/index.php?page=BlackPeopleMeet-Reviews&query=blackpeoplemeet
        for node in :
            reviews.append(node.xpath('string()').extract());
        temp_data = response.xpath("//div[@id='comments']/div[@class='block-comment-content level-0']/ul[@class='comment_status']/li[@class='comment_author']/text()").extract()
        dates =
        headings =  response.xpath("//div[@id='comments']/div[@class='block-comment-content level-0']/ul[@class='comment_status']/li[@class='comment_title']/text()").extract()
        authors =
        img_src =
        website_name =
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                          servicename, reviews[item],img_src,website_name)
            servicename1.save()
