from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
class HostAdviceCrawler(Spider):
    def __init__(self):
        pass

    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        self.category = category
        self.servicename = servicename
        reviews = []
        # https://hostadvice.com/hosting-company/godaddy-reviews/
        for node in response.xpath('//div[@class="review-summary"]'):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='review-rating clearfix']/span[@class='review-score']/text()").extract()
        headings = response.xpath("//div[@class='review-content']/h3[@class='review_header']/text()").extract()
        authors1 = response.xpath("//div[@class='review-author']").extract()
        authors = []
        for content in authors1:
            root = etree.fromstring(content)
            for element in root:
                if (element.tag == 'strong'):
                    authors.append(element.text)
                else:
                    authors.append(element.xpath("//a/strong")[0].text)
        img_src = response.xpath("//div[@class='col-md-offset-1 col-md-5 col-xs-6']/img[ @class='attachment-post-thumbnail size-post-thumbnail wp-post-image']/@src").extract()
        website_name = response.xpath("//div[@class='location_info']/span[2]/span[1]/a[@class='home']/span/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], None, authors[item], category,
                          servicename, reviews[item],img_src,website_name)
            servicename1.save()
        next_page = response.xpath("//div[@class='col-md-offset-2 col-md-4']/a[ @class ='orange_button']/@href").extract()
        if next_page is not None:
            next_page_url = " ".join(next_page)
            if next_page_url and next_page_url.strip():
                yield Request(url=next_page_url,  callback=self.parsing)

        # yield response.follow(next_page_url, callback=self.parse)
