from model.Servicemodel import ServiceRecord


class TheVPNlanCrawler():
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        reviews = []
        dates= []
        authors= []
        # https://www.thevpnlab.com/reviews/nordvpn-review
        for node in response.xpath("//div[@class='ur-inner']/div[@class='user-review']"):
            reviews.append(node.xpath('string()').extract());
        date_authors = response.xpath("//div[@class='ur-inner']/div[@class='user-name']/text()").extract()
        for element in date_authors:
            authors.append(element.split("on")[0].split("By")[1])
            dates.append(element.split("on")[-1])
        ratings =  response.xpath("//div[@class='user-stars']/div/@id").extract()
        img_src =  response.xpath("//div[@class='introvoerview']/div[@id='introimg']/img/@src").extract()
        temp_data = response.xpath("//html/head/script[4]/text()").extract()
        website_name =  temp_data[0].split(",")[3].split(":")[1]
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None,dates[item], authors[item], category,
                          servicename, reviews[item],img_src,website_name);
            servicename1.save()