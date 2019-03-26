from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class HostAdviceCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(HostAdviceCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://hostadvice.com/hosting-company/godaddy-reviews/
        for node in response.xpath('//div[@class="review-summary"]'):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='review-rating clearfix']/span[@class='review-score']/text()").extract()
        headings = response.xpath("//div[@class='review-content']/h3[@class='review_header']/text()").extract()
        authors1 = response.xpath("//div[@class='review-author']").extract()
        authors = []
        date = response.xpath("//div[@class='review-footer clearfix']/div[@class='when-posted pull-right']/text()").extract()
        i=0
        dates = []
        print("dates ", len(date), date)
        while(i<len(date)):
            dates.append(date[i].split("on")[1])
            i = i+1
        for content in authors1:
            root = etree.fromstring(content)
            for element in root:
                if (element.tag == 'strong'):
                    authors.append(element.text)
                else:
                    authors.append(element.xpath("//a/strong")[0].text)
        img_src = response.xpath("//div/a/img[@class='attachment-post-thumbnail size-post-thumbnail wp-post-image']/@src").extract()[0]
        website_name1 = self.link["url"].split("/")
        website_name1 = (website_name1[len(website_name1) - 2]).split("-")
        website_name = 'https://' + website_name1[0] + ".com"
        name="hostadvice.com"
        print("website  ", website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], self.category,
                          self.servicename, reviews[item],img_src,website_name, name)
            self.save(servicename1)
        next_page = response.xpath("//div[@class='row']/div[@class='col-md-offset-2 col-md-4']/a/@href").extract()

        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(next_page_url, callback=self.parsing)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()

