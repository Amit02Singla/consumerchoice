from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class FreeDatingHelper(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(FreeDatingHelper,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #https: // www.webhostinghero.com / reviews / bluehost /
        for node in response.xpath("//div[@class='comment_postinfo']/div/div[@class='comment_area']/div[@class='comment-content clearfix']/div/span"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='comment_postinfo']/div[2]/table[@class='ratings']/tbody/tr/td[@class='rating_value']/div/span/text()").extract()
        # dates = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div[@class='userComments']/div[@class='userDetails']/div[@class='userLocation']/p[1]/span[@class='pIcn']/text()").extract()
        authors =  response.xpath("//div[@class='comment_postinfo']/div[2]/span[@class='fn']/span/text()").extract()
        # headings = response.xpath("//div[@id='left-area']/section[@id='comment-wrap']/ol[@class='commentlist clearfix']/li/article/div[@class='comment_postinfo']/div[2]/div[@class='comment_area']/div[@class='comment-content clearfix']/div[@class='notrecommended']/text()").extract()
        website_name =  response.xpath("/html/head/meta[9]/@content").extract()
        img_src = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()
        print("Reviews ", len(reviews[0]), reviews[0])

        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("website ", len(website_name), website_name)
        print("Img_src ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, None,None, None, authors[item], self.category,
                          self.servicename, reviews[item], img_src,website_name)
            self.save(servicename1)

        next_page = response.xpath("//div[@class='pagination']/ul[@id='yw2']/li[@class='next']/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page[0])
            print(next_page_url)
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url,  callback=self.parsing)
        self.pushToServer()
