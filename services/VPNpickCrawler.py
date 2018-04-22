from model.Servicemodel import ServiceRecord


class VPNpickCrawler():
    def __init__(self):
        pass

 #TODO author and review count mismatch-- done
    def crawl(self, response, category, servicename):
        reviews = []
        # https://vpnpick.com/reviews/expressvpn/
        for node in response.xpath("//div[@id='comments']/ol[@class='commentlist']/li/div/div[@class='commentmetadata']/div[@class='commenttext']"):
            reviews.append(node.xpath('string()').extract());
        dates = response.xpath("//div[@class='comment-author vcard']/span[@class='ago']/text()").extract()
        authors =  response.xpath("//div[@id='comments']/ol[@class='commentlist']/li/div/div[@class='comment-author vcard']/span[@class='fn']/span")
        img_src =  response.xpath("//div[@class='thecontent']/p[1]/img[@class='alignright wp-image-3155']/@src").extract()
        website_name =  response.xpath("/html/head/meta[6]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                          servicename, reviews[item],img_src,website_name);
            servicename1.save()