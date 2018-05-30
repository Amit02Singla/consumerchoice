from model.Servicemodel import ServiceRecord

#URL https://www.forexbrokerz.com/brokers/binance-review
class ForexbrokerzCrawler():

    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        reviews = []
        for node in response.xpath('//div[@class="review_top"]/p'):
            reviews.append(node.xpath('string()').extract());
        headings = response.xpath("//div[@class='review']/div[@class='review_top']/span/h3/a/text()").extract()
        dates = response.xpath("//div[@class='review_details']/span/text()").extract()
        ratings = response.xpath("//div[@class='review_details']/div/div/a/text()").extract()
        authors = response.xpath("//div[@class='review_details']/span/strong/text()").extract()
        img_src = response.xpath("//div[@class='broker_img_container']/img/@src").extract()
        website_name = response.xpath("//div[@class='content'][1]/div[@class='top']/a[@class='logo']/@title").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings, dates[item], authors[item], category,
                          servicename, reviews[item], img_src,website_name);
            servicename1.save()
