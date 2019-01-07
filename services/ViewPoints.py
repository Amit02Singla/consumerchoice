from time import sleep

from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
from lxml import etree

# http://www.viewpoints.com/Kayak-com-reviews
class ViewPoints(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ViewPoints,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print(" in viewPoints   " ,self.link["url"])
        data = response.xpath("//div[@class='pr-contents-wrapper']").extract()
        for content in data:
            root = etree.HTML(content)
            print "length ", len(root.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-main-wrapper']/div[@class='pr-review-text']/p[@class='pr-comments']"))
            if(len(root.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-main-wrapper']/div[@class='pr-review-text']/p[@class='pr-comments']"))>0):
                reviews.append(root.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-main-wrapper']/div[@class='pr-review-text']/p[@class='pr-comments']/text()"))

        ratings =  response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/span[@class='pr-rating pr-rounded']/text()").extract()
        dates = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-author-date pr-rounded']/text()").extract()
        authors = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-author']/div[@class='pr-review-author-info-wrapper']/p[@class='pr-review-author-name']/span/text()").extract()
        headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@class='grid-container']/div[@class='grid-featured']/div[@class='globalNav']/a[@class='logo header']/img/@alt").extract()
        img_src = response.xpath(
            "//div[@class='productDetails']/div[@class='productControls']/div[@class='productPhotoViewer ']/img[@class='photo']/@src").extract()[0]

        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("ratings ", len(ratings), ratings)
        print("Heading ", len(headings), headings)
        print("Dates ", len(dates), dates)
        print("img src ", img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], None, authors[item], "",
                                         self.servicename, reviews[item], img_src, website_name)
            self.save(servicename1)
        next_page = response.xpath(
            "//div[@class='pr-page-nav-wrapper']/p[@class='pr-page-nav']/span[@class='pr-page-next']/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                sleep(5)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()


