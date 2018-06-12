from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
# https://www.bestvpnforyou.com/vpn-reviews/expressvpn-review/
class bestVPNForYou():

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        authors = response.xpath("//div[@class='comment-meta commentmetadata']/cite[@class='fn']/text()").extract()
        dates = response.xpath("//div[@class='comment-time']/a/time/text()").extract()
        #print("Authors   ", authors)
        #print("dates   ", dates)
        for node in response.xpath("//div[@class='comment-text']/span"):
            reviews.append(node.xpath('string()').extract());
        print("reviews ", reviews)
        img_src = response.xpath("//div[@class='vcard-wrap']/img[@class='avatar avatar-100 wp-user-avatar wp-user-avatar-100 photo avatar-default']/@src").extract()
        # ratings = response.xpath("//div[@class='star_rating']/@title").extract()
        website_name = response.xpath("///html/head/title/text()").extract()
        #print("img_src   ", img_src)
        #print("websitesName   ", website_name)
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, None, None,  dates[item], authors[item], category,
                          servicename, reviews[item],  img_src, website_name);
            servicename1.save()
        next_page = response.xpath("//div[@class='nav-previous']/a/@href").extract()
        if next_page is not None:
            next_page_url ="".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                yield response.follow(url=next_page_url, callback=self.parsing)
