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
        return self.crawl(response)

    def crawl(self, response):
        reviews = []
        name = response.xpath("//div[@id='view_category']/div[@class='crumbtrail']/a/text()").extract()
        i = 0
        categoryName = self.category;
        while i < len(name):
            categoryName =  categoryName + " > "+ name[i]
            i = i + 1

        # https://www.sitejabber.com/reviews/zoosk.com
        # for node in response.xpath('//div[@class="review "]/p'):
        #     reviews.append(node.xpath('string()').extract())

        data = response.xpath("//div[@id='left_side']/div[@id='reviews_container']/div[@class='review_row url_home loggedout last']").extract();
        data1 = response.xpath("//div[@id='left_side']/div[@id='reviews_container']/div[@class='review_row url_home loggedout ']").extract();
        authors = []
        headings = []
        ratings = []
        dates = []
        for content1 in data:
            content1 = content1.replace("...", "")
            root = etree.HTML(content1)
            if(len(root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']/a"))):
                authors.append(root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']/a/text()")[0])
            elif (len(root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']"))):
                authors.append(
                    root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']/text()")[0])

            headings.append(root.xpath("//div[@class='review_container ']/div[@class='review ']/div[@class='review_title']/a/text()")[0])
            dates.append(root.xpath("//div[@class='review_container ']/div[@class='review ']/div[@class='stars']/div[@class='time tiny_text faded_text']/text()")[0])
            reviews.append([root.xpath("//div[@class='review_container ']/div[@class='review ']/p/text()")[0]])
            ratings.append(root.xpath("//div[@class='review_container ']/div[@class='review ']/p/@data-rating")[0])
        for content2 in data1:
            content2 = content2.replace("...", "")
            root = etree.HTML(content2)
            if (len(root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']/a"))):
                authors.append(
                    root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']/a/text()")[0])
            elif (len(root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']"))):
                authors.append(
                    root.xpath("//div[@class='author_info tiny_text']/div[@class='author_name']/text()")[0])
            headings.append(root.xpath("//div[@class='review_container ']/div[@class='review ']/div[@class='review_title']/a/text()")[0])
            dates.append(root.xpath("//div[@class='review_container ']/div[@class='review ']/div[@class='stars']/div[@class='time tiny_text faded_text']/text()")[0])
            reviews.append([root.xpath("//div[@class='review_container ']/div[@class='review ']/p/text()")[0]])
            ratings.append(root.xpath("//div[@class='review_container ']/div[@class='review ']/p/@data-rating")[0])

        website = response.xpath("//div[@id='website_info_content']/div[@id='url_address']/a[@class='trackOutboundLink']/@href").extract()[0]
        website_name = website  ;
        authors = list(map(lambda foo: foo.replace(u'\xa0', ' '), authors))
        headings = list(map(lambda foo: foo.replace(u'\u201c', ''), headings))
        headings = list(map(lambda foo: foo.replace(u'\u201d', ''), headings))
        dates = map(lambda  foo: foo.replace("\n\t\t\t\t\t", ""), dates)
        dates = map(lambda foo: foo.replace("\t\t\t\t", ""), dates)
        # print("athors ", len(authors), authors)
        # print("ratings ",len(ratings),ratings)
        # print("headings ", len(headings), headings)
        print("dates ", len(dates))
        print("webiste ", website_name)
        print("reviews ", len(reviews), reviews)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         self.categoryName,
                                         self.servicename, reviews[item], None, website_name)
            self.save(servicename1)

        next_page1 = response.xpath("//div[ @class ='paginator_next']/span/a[@class ='button outline']/@href").extract()
        if next_page1 is not None:
            next_page_url1 ="".join(next_page1)
            if next_page_url1 and next_page_url1.strip():
                yield response.follow(url=next_page_url1, callback=self.parsing)
        self.pushToServer()
