from model.Servicemodel import ServiceRecord
from lxml import etree
class vpnRanks():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        #print("review from vpnranks.com")
        # https://www.highya.com/coinbase-reviews
        for node in response.xpath("//div[@class='comment-body']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='rate']/ul/li/text()").extract()
        dates = response.xpath("//div[@class='comment-meta commentmetadata']/a/text()").extract()
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
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()


