from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
# https://www.bestvpn.com/expressvpn-review/
class BestVPN(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BestVPN,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://www.bestvpn.com/expressvpn-review/
        print("https://www.bestvpn.com/     ", self.link["url"])
        for node in response.xpath("//ol[@class='comment-list']/li/article/div[@class='comment-content']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = "8.2"
        dates = response.xpath("//ol[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-metadata']/a/time/text()").extract()
        authors = response.xpath("//ol[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/b[@class='fn']/text()").extract()
        # img_src = response.xpath("//div[@class='review-excerpt row']/div[@class='col-lg-6'][1]/a/img[@class='logo']/@src").extract()[0]
        website_name = "bestvpn.com"
        print("Reviews ", len(reviews))
        print("Authors ", len(authors), authors)
        # print("img_src ", len(img_src), img_src)

        print("Dates ", len(dates), dates)

        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None,None, dates[item], authors[item], "",
                          self.servicename, reviews[item], "",website_name);
            self.save(servicename1)
        self.pushToServer()
