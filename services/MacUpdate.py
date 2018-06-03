from model.Servicemodel import ServiceRecord
from utils.utils import getStarts

#TODO redo website
#URL https://www.macupdate.com/app/mac/52417/purevpn
class MacUpdate():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from macupdate.com")
        for node in response.xpath("//div/div[@class='yui3-u rcpb-content']/p[@class='rcpb-revcom-content']"):
            reviews.append(node.xpath('string()').extract())
        ratings = response.xpath("//div/div[@class='yui3-u rcpb-content']/div/input/@value/@text()").extract()
        dates = response.xpath("//div/div[@class='yui3-u rcpb-content']/span[@class='rcpb-postdate']/text()").extract()
        headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        authors = response.xpath("//div[@class='box col-12 review-info']/strong/span/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        img_src = response.xpath("//div[@class='avatar']/img/@src").extract()
        print(" raaaaaa")

        for i in range(len(ratings)):
            if i != 0:
                del [ratings]
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], img_src, website_name)
            servicename1.save()

        next_page = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)




