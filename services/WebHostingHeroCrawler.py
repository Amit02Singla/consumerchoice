from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from utils.utils import getStarts
# https://www.webhostinghero.com/reviews/bluehost/
#TODO Done
class WebHostingHeroCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        headings = []
        authors = []
        dates = []
        ratings1 = []
        self.category = category
        self.servicename = servicename

        nodes = response.xpath("//div[@class='row user-review']").extract();

        for content in nodes:
            root = etree.HTML(content)
            # print(root)
            if(len(root.xpath("//div[@class='col-12 review-description']/p/text()"))>0):
                reviews.append(root.xpath("//div[@class='col-12 review-description']/p/text()")[0])
            if(len(root.xpath("//div[@class='col-12 review-rating']/h4/text()"))>0):
                headings.append(root.xpath("//div[@class='col-12 review-rating']/h4/text()")[0])
            else:
                headings.append("")
            if (len(root.xpath("//div[@class='col-12 author']/span/text()")) > 0):
                authors.append(root.xpath("//div[@class='col-12 author']/span/text()")[0])
            else:
                authors.append("")
            if (len(root.xpath("//div[@class='col-12 review-meta'][1]/span[@class='review-date']/text()")) > 0):
                dates.append(root.xpath("//div[@class='col-12 review-meta'][1]/span[@class='review-date']/text()")[0])
            else:
                dates.append("")
            if (len(root.xpath("//div[@class='col-12 review-rating']/div/@class")) > 0):
                ratings1.append(root.xpath("//div[@class='col-12 review-rating']/div/@class")[0])
            else:
                ratings1.append("")


        # for node in response.xpath("//div[@class='row user-review']/div[@class='col-12 review-description']"):
        #     reviews.append(node.xpath('string()').extract());
        # ratings1 =  response.xpath("//div[@class='row user-review']/div[@class='col-12 review-rating']/div/@class").extract()
        # dates = response.xpath("//div[@class='row user-review']/div[@class='col-12 review-meta'][1]/span[@class='review-date']/text()").extract()
        #
        # authors =  response.xpath("//div[@class='row user-review']/div[@class='col-12 author']/span/text()").extract()
        website_name =  response.xpath("/html/head/meta[9]/@content").extract()
        i=0;
        ratings2 = []
        ratings = []
        while i< len(ratings1):
            c= getStarts(ratings1[i])
            ratings2.append(c)
            i = i+1;
            ratings2 = map(lambda foo: foo.replace('-', ''), ratings2)
        i=0
        while i < len(ratings2):
            c= int(ratings2[i])/2.0
            ratings.append(c)
            i = i + 1;

        for item in range(0, len(reviews)):
            servicename1 =ServiceRecord(response.url, ratings[item],headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], "",website_name)
            servicename1.save()
        next_page = response.xpath("//div[@class='col-12']/div[@class='row']/div[@class='col-12 navigator align-center']/a[last()]/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page[0])
            print(next_page_url)
            if next_page_url and next_page_url.strip():
                yield Request(url=next_page_url,  callback=self.parsing)
