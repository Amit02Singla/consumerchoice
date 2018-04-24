from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree

class SiteJabberCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
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
        website_name = response.xpath("//div[@id='header_top']/a[@id='header_logo']/picture/img/@alt").extract()
        #print(authors)
        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, ratings[item],headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], None,website_name);
            servicename1.save()
        next_page = response.xpath("// div[ @class ='paginator_next']/span/a[@class ='button outline']/@href").extract()
        if next_page is not None:
            next_page_url ="".join(next_page)
            if next_page_url and next_page_url.strip():
                #print(type(next_page_url))
                #print(next_page_url)
                yield response.follow(url=next_page_url, callback=self.parsing)
