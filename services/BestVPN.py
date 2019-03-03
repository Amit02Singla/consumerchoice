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
        for node in response.xpath("//div[@id='comments-container']/ol[@class='post-comments']/li[@class='comment']/p"):
            reviews.append(node.xpath('string()').extract());
        # ratings = "8.2"
        dates = response.xpath("//div[@id='comments-container']/ol[@class='post-comments']/li[@class='comment']/header/div[@class='mr-auto']/div[@class='comment-author']/div/span/em/text()").extract()
        authors = response.xpath("//div[@id='comments-container']/ol[@class='post-comments']/li[@class='comment']/header/div[@class='mr-auto']/div[@class='comment-author']/div/h5/text()").extract()
        img_src = response.xpath("//a[@class='logo-link']/img[@class='provider-logo']/@src").extract()[0]
        website_name = response.xpath("//a[@class='logo-link']/@href").extract()[0]
        website_name = "https://www.bestvpn.com"+website_name
        print("Reviews ", len(reviews))
        print("Authors ", len(authors), authors)
        print("img_src ", len(img_src), img_src)

        print("Dates ", len(dates), dates)

        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None,None, dates[item], authors[item], self.category,
                          self.servicename, reviews[item], img_src,website_name);
            self.save(servicename1)
        self.pushToServer()
