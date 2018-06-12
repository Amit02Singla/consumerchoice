from model.Servicemodel import ServiceRecord
from lxml import etree


# http://www.hostingcharges.in/hosting-reviews/fatcow
# TODO DONE
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
        # for item in temp_reviews:
        #     # print (item)
        #     if(str(item[0].encode("utf-8")).strip()!= ""):
        #         reviews.append([str(item[0].encode("utf-8")).strip()])
        for node in response.xpath("//div[@class='review-sub-cntnr']/div[@class='review-one-all']/p[@class='cust-review']"):
            reviews.append(node.xpath('string()').extract());

        temp_ratings = response.xpath("//div[@class='review-one-all']/div[@class='lftfeatures']/div/div/input/@value").extract()
        temp_headings = response.xpath("//div[@class='review-right']").extract()
        headings = []
        for content in temp_headings:
            root = etree.HTML(content)
            if(len(root.xpath("//h4/text()")) == 0 ):
                headings.append(root.xpath("//a/text()")[0])
            else:
                headings.append(root.xpath("//h4/text()")[0])
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
        img_src = response.xpath("//div[@class='review-cntnr']/div[@class='review-sub-cntnr']/div[@class='logo-img']/a/img/@src").extract()[0]
        authors = response.xpath("//div[@class='review-mid']/h4/text()").extract()
        website_name = response.xpath("//div[@id='bs-example-navbar-collapse-1']/ul[@class='nav navbar-nav navbar-right']/li[@class='dropdown'][1]/a/@href").extract()

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], img_src, website_name)
            servicename1.save()


