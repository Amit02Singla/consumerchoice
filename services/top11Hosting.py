from model.Servicemodel import ServiceRecord
from utils.utils import getStarts
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class top11Hosting(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(top11Hosting,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://top11hosting.com/hostgator-review/
        for node in response.xpath("//div[@class='wpcr3_item wpcr3_business']/div/blockquote[@class='wpcr3_content']"):
            reviews.append(node.xpath('string()').extract());
        rate = response.xpath("//div[@class='wpcr3_rating_style1_average']/@style").extract()
        rate.pop(0)
        rate.pop(0)
        ratings = []
        for i in range(0,len(rate)):
            rate[i]=rate[i].split(":")[1].split("%")[0]
            ratings.append(str((int(rate[i]))*5/100))
        dates = response.xpath("//div[@class='wpcr3_review_datePublished']/text()").extract()
        # headings = response.xpath("//div[@class='width64 floatleft']/h4[3]").extract()
        authors = response.xpath("//div[@class='wpcr3_review_author']/span[@class='wpcr3_caps']/text()").extract()
        website_name = response.xpath("//div[@class='width64 floatleft']/div[@class='width45 floatright']/p[@class='aligncenter']/a[@class='button2_fixed']/@href").extract()[0]
        ratings1 = []
        i =0
        print "website ", website_name
        # while i < len(ratings):
        #     c= int(getStarts(ratings[i]))/20
        #     ratings1.append(str(c))
        #     i = i + 1
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
                                         "", self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()


