from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
class DatingSitesReviewsCrawler(Spider):
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        self.category = category
        self.servicename = servicename
        reviews = []
        # https://www.datingsitesreviews.com/staticpages/index.php?page=BlackPeopleMeet-Reviews&query=blackpeoplemeet
        # TODO Extract data: done
        for node in response.xpath("//div[@id='comments']/div[@class='block-comment-content level-0']/div[@class='comment_content']"):
            reviews.append(node.xpath('string()').extract());
        temp_data = response.xpath("//div[@id='comments']/div[@class='block-comment-content level-0']/ul[@class='comment_status']/li[@class='comment_author']").extract()
        dates = []
        authors = []
        for content in temp_data:
            root = etree.HTML(content)
            if(root.xpath("//a")):
                data = root.xpath("//a/text()")
                authors.append(data)
                dates.append(str(root.xpath("//text()")[2].split(",")[1].split("@")[0]))
            else:
                data = root.xpath("//text()")
                dates.append(data[0].split(":")[1].split(",")[1].split("@")[0])
                data1=data[0].encode("utf-8")
                data1 = data1.replace('\xc2\xa0', ' ')
                authors.append(data1.split(":")[1].split(" on ")[0])

        headings =  response.xpath("//div[@id='comments']/div[@class='block-comment-content level-0']/ul[@class='comment_status']/li[@class='comment_title']/text()").extract()
        website_name =  response.xpath("/html/head/title").extract()[0].split(" - ")[1]

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], dates[item], authors[item], category,
                          servicename, reviews[item],None,website_name)
            servicename1.save()
