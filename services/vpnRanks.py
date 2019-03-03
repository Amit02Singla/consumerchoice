from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class vpnRanks(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(vpnRanks,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #print("review from vpnranks.com")
        for node in response.xpath("//div[@class='comment-body']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='rate']/ul/li/text()").extract()
        dates = response.xpath("//li/div/div[@class='comment-meta commentmetadata']/text()").extract()
        # headings = response.xpath("//div[@class='row']/div[@class='col-md-6 col-md-pull-2 col-xs-12']/div[@class='topic']/span/text()").extract()
        authors1 = response.xpath("//div[@class='comment-author vcard']").extract()
        authors =[]
        for content in authors1:
            root = etree.fromstring(content)
            if (root.text == None):
                for element in root:
                    authors.append(element.text)
            else:
                for element in root:
                    authors.append(element.text)
        for i in range(len(authors)/2 + 1):
           if i != 0 :
                del authors[i]
        website_name = response.xpath("//div[@class='cta-box']/a[@class='btn btn-vst btn-orange']/@href").extract()[0]
        # img_src = response.xpath("//div[@class='prov-rev-img']/img[@class='img-fluid lazy-loaded']/@src").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()


