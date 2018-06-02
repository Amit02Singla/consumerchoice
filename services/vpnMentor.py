from model.Servicemodel import ServiceRecord
from lxml import etree

class vpnMentor():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)
 #TODO Need to recheck and implement: done some error
    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
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
            authors.append(root.xpath("//div/div/div/div/div/h5/text()"))
            dates.append(str(root.xpath("//div[@class='review-head']/div[@class='row']/div[@class='col-md-4 col-xs-5']/div[@class='user']/div[@class='text-wrap']/h6/text()")))
            headings.append(root.xpath("//div[@class='review-head']/div[@class='row']/div[@class='col-md-6 col-md-pull-2 col-xs-12']/div[@class='topic']/span/text()"))
            ratings.append(str(root.xpath("//div[@class='review-head']/div[@class='row']/div[@class='col-md-2 col-md-push-6 col-xs-7']/div[@class='rate']/ul/li[@class='fa']/text()")))
            reviews.append(root.xpath("///div[@class='review-content']/p/text()"))
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()


