from model.Servicemodel import ServiceRecord

class HostingFactsCrawler():
    def __init__(self):
        pass
    def crawl(self, response,category,servicename):
        reviews = []
        print("review from Hostingfacts.com")
        # https://hostingfacts.com/hosting-reviews/hostgator-wordpress-managed/
        for node in response.xpath('//div[@class="user-review-content"]'):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class= 'user-review']/header/section/span[@class='user-review-rating']/span[@class='value']/text()").extract()
        dates = response.xpath("//div[@class= 'user-review']/header/section/span[@class='user-review-meta']/text()").extract()
        headings = response.xpath("//div[@class= 'user-review']/section/p[@class='user-review-title']/text()").extract()
        authors = response.xpath("//div[@class='user-review']/header/section/p[@class='user-review-name']/a/span/text()").extract()
        img_src = response.xpath("//div[@class='sidebar-padder']/aside/img[@class='img-responsive banner-image center-block']/@src").extract()
        website_name = response.xpath("//div[@class='navbar-header']/a[@class='navbar-brand']/text()").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url,ratings[item],headings[item],dates[item],authors[item],category,servicename,reviews[item],img_src,website_name);
            servicename1.save()