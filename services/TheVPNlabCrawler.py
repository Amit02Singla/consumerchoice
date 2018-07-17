from model.Servicemodel import ServiceRecord

from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class TheVPNlabCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(TheVPNlabCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        dates= []
        authors= []
        # https://www.thevpnlab.com/reviews/nordvpn-review
        for node in response.xpath("//div[@class='ur-inner']/div[@class='user-review']"):
            reviews.append(node.xpath('string()').extract());
        date_authors = response.xpath("//div[@class='ur-inner']/div[@class='user-name']/text()").extract()
        for element in date_authors:
            authors.append(element.split("on")[0].split("By")[1])
            dates.append(element.split("on")[-1])
        ratings1 =  response.xpath("//div[@class='user-stars']/div/@id").extract()
        img_src =  response.xpath("//div[@id='introimg']/img/@src").extract()
        website_name =  "thevpnlab.com"
        ratings = []
        i=0
        while i < len(ratings1):
            c= ratings1[i].replace('stars-','')
            ratings.append(c)
            i = i+1

        print "img_src ", img_src
        print "ratings ", ratings
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None,dates[item], authors[item], self.category,
                          self.servicename, reviews[item],img_src[0],website_name);
            self.save(servicename1)
        self.pushToServer()