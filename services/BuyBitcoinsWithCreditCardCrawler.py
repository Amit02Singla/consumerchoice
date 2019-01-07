from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler

class BuyBitcoinsWithCreditCardCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BuyBitcoinsWithCreditCardCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []

        # http://www.buybitcoinswithcreditcard.net/en/coinbase-com/
        '''temp_dates =  response.xpath("//div[@class='box']/ol[@class='comment-list']/li/div/div[@class='comment-author vcard rc']/text()").extract()
        dates = []
        for j in range(1, len(dates)):
            if (j % 2 != 0):
                dates.append(dates[j]'''
        authors = []
        reviews=[]
        ratings =[]
        reviews = []
        dates = []
        ratings1 = []
        data = response.xpath("//div[@id='reviews']/div[@class='box']/ol[@class='comment-list']/li").extract()
        for content in data:
            content = content.replace('<br>', '$')

            root = etree.fromstring(content)
            dates.append(root.xpath("//div/div[@class='comment-author vcard rc']/text()")[1])
            authors.append(root.xpath("//div/div/cite/text()")[0])
            reviews.append(root.xpath("//div/p/text()"))
            rate = root.xpath("//div/div[@class='comment-author vcard rc']/div/span/text()")
            if(len(rate)>0):
                ratings1.append(int(rate[0]))
            else:
                ratings1.append("")
        i=0
        while i < len(ratings1):
            if(ratings1[i]==""):
                ratings.append("")
            else:
                c= float(ratings1[i]/20.0)
                ratings.append(round(c,1))
            i = i+1
        website_name = response.xpath("//div[@class='inner']/div[@class='box right']/a[@class='zumanbieter']/@href").extract()[0]
        print("website name   ", website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
                                         "", self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()

