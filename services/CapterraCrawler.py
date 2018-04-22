from model.Servicemodel import ServiceRecord


class CapterraCrawler():

    def __init__(self):
        pass


    def crawl(self, response, category, servicename):
        reviews = []
        print("Reviews from Capterra.con")
        # https://www.capterra.com/p/170765/ExpressVPN/
        for node in response.xpath('//div[@class="review-comments  color-text"]'):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='overall-rating-container']/span[@class='overall-rating']/span/text()").extract()
        headings = response.xpath("//div[@class='cell seven-eighths  palm-one-whole']/h3/q/text()").extract()
        dates = response.xpath("//div[@class='grid']/div[@class='cell one-eighth  palm-one-whole']/div[@class='quarter-margin-bottom  micro  color-gray  weight-normal  text-right  palm-text-left']/text()").extract()
        img_src = response.xpath("//div[@class='thumbnail  no-hover  listing-thumbnail']/img/@src").extract()
        website_name = response.xpath("//div[@class='site-logo-wrapper']/a/img[@class='site-logo']/@alt").extract()
        for item in range(0, len(reviews)):
            service1 = ServiceRecord(response.url, ratings[item],headings[item], dates[item], None, category,
                          servicename, reviews[item], img_src,website_name);
            service1.save()
