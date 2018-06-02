from model.Servicemodel import ServiceRecord
from lxml import etree

class FreeDatingHelperCrawler():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        # http://www.freedatinghelper.com/reviews/fortyplus-singles/
        #TODO Need to check pick only first review: Refer Sandy
        authors = []
        reviews=[]
        ratings =[]
        data = response.xpath("//div/div/div/section/ol/li").extract()
        print data
        for content in data:
            content = content.replace('<br>', '$')
            root = etree.HTML(content)
            authors.append(root.xpath("//li/article/div/div[2]/span/span/text()"))
            reviews.append(root.xpath("//div/div/div/div/div/span/p/text()"))
            rate = root.xpath("//div/div/table/toby/tr/td/div/span/text()")
            if (rate != None and len(rate) > 0):
                ratings.append(rate[0])
            else:
                ratings.append("")
        website_name= response.xpath("//html/head/meta[8]/@content").extract()[0]
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, None, authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()