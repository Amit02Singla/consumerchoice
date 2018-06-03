from model.Servicemodel import ServiceRecord
from lxml import etree
class hostingCharges():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        temp_reviews = []
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from hostingcharges.in")
        # http://www.hostingcharges.in/hosting-reviews/bluehost
        for node in response.xpath("//div[@class='review-cntnr']/div[@class='review-sub-cntnr']/div[@class='review-one-all']/p"):
            temp_reviews.append(node.xpath('string()').extract());
        for item in temp_reviews:
            print (item)
            if(str(item[0].encode("utf-8")).strip()!= ""):
                reviews.append([str(item[0].encode("utf-8")).strip()])
        temp_ratings = response.xpath("//div[@class='review-one-all']/div[@class='lftfeatures']/div/div/input/@value").extract()
        temp_headings = response.xpath("//div[@class='review-right']").extract()
        headings = []
        for content in temp_headings:
            root = etree.HTML(content)
            if(len(root.xpath("//h4/text()")) == 0 ):
                headings.append(root.xpath("//a/text()")[0])
            else:
                headings.append(root.xpath("//h4/text()")[0])

        #TODO code pending giving error url need to extract: done
        ratings = []
        i=0
        sum = 0
        for i in range(len(temp_ratings)):
            if (i+1) % 4 == 0 :
                ratings.append(str(sum/4))
                sum = int(temp_ratings[i])
            else:
                sum = sum + int(temp_ratings[i])

        dates = response.xpath("//div[@class='review-sub-cntnr']/div[@class='review-one-all']/div[@class='review-profile']/div[@class='review-mid']/p/text()").extract()
        img_src = response.xpath("//div/div[1]/div/div/div[1]/a/img/@src").extract()[0]
        authors = response.xpath("//div[@class='review-mid']/h4/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], img_src, website_name)
            servicename1.save()


