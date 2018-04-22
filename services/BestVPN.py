from model.Servicemodel import ServiceRecord


class BestVPN():

    def __init__(self):
        pass


    def crawl(self, response, category, servicename):
        reviews = []
        print("Reviews from bestvpn.com")
        # https://www.bestvpn.com/expressvpn-review/
        for node in response.xpath('//div[@class="comment-content"]'):
            reviews.append(node.xpath('string()').extract());
        ratings = "8.2"
        dates = response.xpath("//div[@class='comment-metadata']/time/text()").extract()
        authors = response.xpath("//div[@class='comment-author vcard']/b/text()").extract()

        img_src = response.xpath(
            "//div[@class='review-excerpt row']/div[@class='col-lg-6'][1]/a/img[@class='logo']/@src").extract()
        website_name = response.xpath(
            "//div[@class='container flex justify-content-between']/a[@class='logo']/img/@alt").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings,None, dates[item], authors[item], category,
                          servicename, reviews[item], img_src,website_name);
            servicename1.save()
