from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler

class ReviewOpedia(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ReviewOpedia,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []

        for node in response.xpath("//div[@class='item-info review']/div[@class='review-text']"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='item-info-text user']/div[@class='prod-block-line']/div[@class='review-result-rating']/div/meta/@content").extract()
        dates = response.xpath("//div[@class='item-info-text user']/div[@class='prod-block-line']/div[@class='review-date']/text()").extract()
        headings =  response.xpath("//div[@class='item-info review']/div[@class='item-info-text user']/h4[@class='item-title']/text()").extract()
        authors1 =  response.xpath("//div[@class='item-info review']/div[@class='review-result-left']/div[@class='review-result-author']").extract()
        authors = []
        for content in authors1:
            root = etree.HTML(content)
            if(len(root.xpath("//div[@class='reviewed-by']/a/text()"))>0):
                authors.append(root.xpath("//div[@class='reviewed-by']/a/text()"))
            else:
                authors.append(root.xpath("//div[@class='reviewed-by']/text()"))
        website_name =  response.xpath("//div[@class='item-info product']/div[@class='item-info-text']/div[@class='prod-block-line'][2]/a/@href").extract()[0]
        website_name = 'https://www.reviewopedia.com'+website_name
        # img_src = response.xpath("//div[@class='review_result']/div[@class='review_result_left']/img[@class='review_author_img']/@src").extract()
        print("Reviews ", len(reviews), reviews)
        print("Headings ", len(headings), headings)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("Img_src ", website_name)
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, ratings[item],headings[item], dates[item], authors[item], self.category,
                          self.servicename, reviews[item], None,website_name)
            self.save(servicename1)

        # next_page = response.xpath("//div[@class='container']/div[@class='navigator']/a[last()]/@href").extract()
        # if next_page is not None:
        #     next_page_url = "".join(next_page[0])
        #     print(next_page_url)
        #     if next_page_url and next_page_url.strip():
        #         yield Request(url=next_page_url,  callback=self.parsing)
        self.pushToServer()
