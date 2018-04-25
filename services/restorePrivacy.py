from model.Servicemodel import ServiceRecord

class restorePrivacy():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from restoreprivacy.com")
        # https://www.highya.com/coinbase-reviews
        for node in response.xpath("//div[@class='comment-text-inner']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='wpcr3_rating_style1_average']/@style").extract()
        dates = response.xpath("//div[@class='comment-author vcard']/span[@class='ago']/text()").extract()
        # headings = response.xpath("//div[@class='width64 floatleft']/h4[3]").extract()
        authors = response.xpath("//div[@class='comment-author vcard']/span[@class='fn']/span/text()").extract()
        img_src = response.xpath("//div[@class='comment-author vcard']/img[@class='avatar avatar-50 photo']/@src").extract()
        website_name = response.xpath("//div[@class='title-area']/p[@class='site-title']/a/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()


