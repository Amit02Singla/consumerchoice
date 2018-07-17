from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class vpnMentor(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(vpnMentor,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #print("review from vpnmentor.com")
        # https://www.vpnmentor.com/reviews/expressvpn/
        authors = []
        dates = []
        ratings = []
        reviews = []
        headings = []
        data = response.xpath("//div[@id='user-review']/span/div[@class='block-content']/div/div[@class='review-item style_prevu_kit ']").extract()
        for content in data:
            content = content.replace('<br>', '$')
            root = etree.HTML(content)
            if len(root.xpath("//div/div/div/div/div/h5/text()")) == 0:
                authors.append("")
            else:
                authors.append(root.xpath("//div/div/div/div/div/h5/text()")[0])
            if(len(root.xpath("//div[@class='review-head']/div[@class='row']/div[@class='col-md-4 col-xs-5']/div[@class='user']/div[@class='text-wrap']/h6/text()")) == 0):
                dates.append("")
            else:
                dates.append(str(root.xpath("//div[@class='review-head']/div[@class='row']/div[@class='col-md-4 col-xs-5']/div[@class='user']/div[@class='text-wrap']/h6/text()")[0]))
            headings.append(root.xpath("//div[@class='review-head']/div[@class='row']/div[@class='col-md-6 col-md-pull-2 col-xs-12']/div[@class='topic']/span/text()")[0])
            ratings.append(str(root.xpath("//div[@class='review-head']/div[@class='row']/div[@class='col-md-2 col-md-push-6 col-xs-7']/div[@class='rate']/ul/li[@class='fa']/text()")))
            reviews.append(root.xpath("///div[@class='review-content']/p/text()"))
        website_name = "vpnmentor.com"
        print("reviews ", len(reviews))
        print("authors   ", len(authors), authors)
        print ("dates ", len(dates))
        print("headings ", len(headings))
        print("ratings ", len(ratings))
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         "", self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()


