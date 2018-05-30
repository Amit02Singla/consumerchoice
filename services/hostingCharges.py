from model.Servicemodel import ServiceRecord
from lxml import etree
class hostingCharges():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from hostingcharges.in")
        # https://www.highya.com/coinbase-reviews
        for node in response.xpath("//div[@class='review-cntnr']/div[@class='review-sub-cntnr']/div[@class='review-one-all']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='review-one-all']/div[@class='lftfeatures']/div/div/input/@value").extract()
        headings = response.xpath("//div[@class='review-mid']/p/text()").extract()
        #TODO code pending giving error url need to extract
        ratings1 = []
        for i in range(len(ratings)):
            if i % 4 != 0 and i != 0:
                sum = sum + int(ratings[i])
            else:
                if i != 0:
                    c = sum / 4.0
                    ratings1.append(str(c))
                sum = 0
                sum = sum + int(ratings[i])

        c = sum / 4.0
        ratings1.append(str(c))
        dates = response.xpath("//div[@class='review-sub-cntnr']/div[@class='review-one-all']/div[@class='review-profile']/div[@class='review-mid']/p/text()").extract()
        img_src = response.xpath("//div[@class='logo-profile']/img/@src").extract()
        authors = response.xpath("//div[@class='review-mid']/h4/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        print(" Ratings ", len(ratings1), ratings1)
        reviews = [[s.strip() for s in nested] for nested in reviews]
        i =0
        count = 0
        while i < len(reviews):
            if reviews[i][0] == '':
                del reviews[i]
                count = count+1
            i = i+1
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings1[item], headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], img_src, website_name)
            servicename1.save()


