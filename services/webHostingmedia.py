from model.Servicemodel import ServiceRecord

class webHostingmedia():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        #print("review from webHostingmedia.com")
        # https://webhostingmedia.net/bluehost-reviews/
        for node in response.xpath("//div[@class='testimonial']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='rateit']/@data-rateit-value").extract()
        dates = response.xpath("//div[@class='wpcr_fl wpcr_rname']/span[@class='dtreviewed']/text()").extract()
        # headings = response.xpath("//div[@class='width64 floatleft']/h4[3]").extract()
        authors = response.xpath("//div[@class='wpcr_fl wpcr_rname']/span/span/strong/text()").extract()
        # website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         category, servicename, reviews[item], None, None)
            servicename1.save()


