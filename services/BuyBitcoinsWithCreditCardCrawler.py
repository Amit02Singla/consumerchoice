from model.Servicemodel import ServiceRecord
from lxml import etree

class BuyBitcoinsWithCreditCardCrawler():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
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
        data = response.xpath("//div[@id='reviews']/div[@class='box']/ol[@class='comment-list']/li").extract()
        for content in data:
            content = content.replace('<br>', '$')
            root = etree.fromstring(content)
            for element in root.iter():
                temp_tag= element.tag
                temp_data = element.text
                if (element.tag == 'cite'):
                    authors.append(element.text)
                if(element.tag == 'p'):
                    reviews.append(element.text)
                if(element.tag == 'span'):
                    ratings.append(int(element.text)/100)
                if(element.tag == 'div'):
                    if(element.xpath == "//div/div[@class='comment-author vcard rc']"):
                            dates.append(element.text)

        website_name = response.xpath("//html/head/title/text()").extract()[0].split("-")[1]
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()

