from model.Servicemodel import ServiceRecord

class vpnMentor():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)
 #TODO Need to recheck and implement
    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from vpnmentor.com")
        # https://www.highya.com/coinbase-reviews
        for node in response.xpath("//div[@class='review-item style_prevu_kit ']/div[@class='review-content']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='rate']/ul/li/text()").extract()
        dates = response.xpath("//div[@class='row']/div[@class='col-md-4 col-xs-5']/div[@class='user']/div[@class='text-wrap']/h6/text()").extract()
        headings = response.xpath("//div[@class='row']/div[@class='col-md-6 col-md-pull-2 col-xs-12']/div[@class='topic']/span/text()").extract()
        authors = response.xpath("//div[@class='text-wrap']/h5/text()").extract()
        # img_src = response.xpath("//div[@class='img-wrap']/div/").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        print(" Ratings ", len(ratings), ratings)
        print("dates ", len(dates), dates)
        print(" Reviews ", len(reviews), reviews)
        print(" headings ", len(headings), headings)
        print(" authors ", len(authors), authors)
        # print("img_Src ", len(img_src), img_src)
        print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()


