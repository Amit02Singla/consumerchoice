from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler

class SiteJabberCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(SiteJabberCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        name = response.xpath("//div[@id='view_category']/div[@class='crumbtrail']/a/text()").extract()
        i = 0;
        categoryName = "";
        while i < len(name):
            if (i == len(name) - 1):
                categoryName = categoryName + name[i];
            else:
                categoryName = categoryName + name[i] + " > ";
            i = i + 1;

        # https://www.sitejabber.com/reviews/zoosk.com
        for node in response.xpath('//div[@class="review "]/p'):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='star_rating']/@title").extract()
        dates = response.xpath("//div[@class='time tiny_text faded_text']/text()").extract()
        headings = response.xpath("//div[@class='review_title']/a/text()").extract()
        authors1 = response.xpath("//div[@class='author_name']").extract()
        authors = []
        for content in authors1:
            root = etree.fromstring(content)
            if(root.text == None ):
                for element in root:
                    authors.append(element.text)
            else:
                authors.append(root.text)
        website = response.xpath("//div[@id='header_top']/a[@id='header_logo']/picture/img/@alt").extract()
        website_name = website[0];
        # print(authors)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         categoryName,
                                         servicename, reviews[item], None, website_name);
            self.save(servicename1)

        next_page1 = response.xpath("//div[ @class ='paginator_next']/span/a[@class ='button outline']/@href").extract()
        if next_page1 is not None:
            next_page_url1 ="".join(next_page1)
            if next_page_url1 and next_page_url1.strip():
                yield response.follow(url=next_page_url1, callback=self.parsing)
        self.pushToServer()
