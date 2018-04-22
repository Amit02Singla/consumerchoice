from model.Servicemodel import ServiceRecord

class AffgadgetsCrawler():
    def __init__(self):
        pass
    def crawl(self, response,category,servicename):
        reviews = []
        # http://affgadgets.com/binance
        for node in response.xpath('//div[@class="comment-info"]'):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='comment-author-main-meta-info']/div/@class").extract()
        authors =  response.xpath("//div[@class='comname']/cite[@class='fn']/text()").extract()
        dates = response.xpath("//div[@class='comment-author-main-meta-info']/ cite[ @class ='timed'] / text()").extract()
        website_name = response.xpath("//html/head/meta[21]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url,ratings[item],None,dates[item],authors[item],category,servicename,reviews[item],"",website_name);
            servicename1.save()