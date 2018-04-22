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
        for node in response.xpath("//div[@class='review-one-all'][1]/p[2]"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='wpcr3_rating_style1_average']/@style").extract()
        dates = response.xpath("//div[@class='review-mid']/p/text()").extract()
        data = response.xpath("//div[@class='review-cntnr']").extract()
        headings = []
        #TODO code pending giving error
        for content in data:
            #root = etree.fromstring(content)
            print(content)
            break
        img_src = response.xpath("//div[@class='logo-profile']/img/@src").extract()
        authors = response.xpath("//div[@class='review-mid']/h4/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        # print(" Ratings ", len(ratings), ratings)
        #print("dates ", len(dates), dates)
        #print(" Reviews ", len(reviews), reviews)
        #print(" headings ", len(headings), headings)
        #print(" authors ", len(authors), authors)
        #print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], img_src, website_name)
            servicename1.save()


