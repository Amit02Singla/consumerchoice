from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class restorePrivacy(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(restorePrivacy,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("review from restoreprivacy.com")
        # https://restoreprivacy.com/expressvpn-review/
        for node in response.xpath("//div[@class='comment-text-inner']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='wpcr3_rating_style1_average']/@style").extract()
        dates = response.xpath("//div[@class='comment-author vcard']/span[@class='ago']/text()").extract()
        # headings = response.xpath("//div[@class='width64 floatleft']/h4[3]").extract()
        authors = response.xpath("//div[@class='comment-author vcard']/span[@class='fn']/span/text()").extract()
        img_src = response.xpath("//div[@class='comment-author vcard']/img[@class='avatar avatar-50 photo']/@src").extract()
        website_name = response.xpath("//div[@class='title-area']/p[@class='site-title']/a/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         "", self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()


