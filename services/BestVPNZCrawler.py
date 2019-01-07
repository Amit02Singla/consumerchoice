from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
# https://www.bestvpnz.com/expressvpn/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class BestVPNZCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BestVPNZCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://www.bestvpnz.com/expressvpn/
        for node in  response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/article/div[@class='comment-content']"):
            reviews.append(node.xpath('string()').extract());
        dates =  response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author-info']/div[@class='entry-meta comment-metadata']/a/time/text()").extract()
        # img_src =  response.xpath("//img[@class='attachment-full size-full wp-post-image']/@src").extract()[0]
        website_name =  response.xpath("//div[@class='inside-article']/div[@class='entry-content']/p[1]/a[@class='myButton']/@href").extract()[0]
        authors = []
        data = response.xpath("//div[@id='comments']/ol[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author-info']").extract()
        # print "imgsrc ", img_src
        print"website ", website_name
        for content in data:
            root = etree.HTML(content)
            if(root.xpath("//cite")):
                if(root.xpath("//cite/a")):
                    authors.append(root.xpath("//cite/a/text()")[0])
                else:
                    authors.append(root.xpath("//cite/text()")[0])


        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], self.category,
                          self.servicename, reviews[item],None,website_name)
            self.save(servicename1)
        self.pushToServer()
