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
        authors = []
        reviews=[]
        ratings =[]
        data = response.xpath("//div[@itemtype='http://schema.org/Review']").extract()
        for content in data:
            content = content.replace('<br>', '$')
            root = etree.fromstring(content)
            temp = (root)
            for element in root.iter():
                temp_tag= element.tag
                temp_data = element.text
                if(element.tag == 'span'):
                    authors.append(element.text)
                if(element.tag == 'p'):
                    reviews.append(element.text)

        #website_name=
       #for item in range(0, len(reviews)):
            #servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
             #                            category, servicename, reviews[item], None, website_name)
            #servicename1.save()