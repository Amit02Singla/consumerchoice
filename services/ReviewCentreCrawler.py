from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts

#Todo: WIP giving error
class ReviewCentreCrawler(Spider):

    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        # https://www.reviewcentre.com/Dating-Sites/Elite-Singles-www-elitesingles-co-uk-www-hospiconsultant-com-reviews_3802989#Reviews
        for node in response.xpath("//ol[@class='commentlist clearfix']/li/article/div[@class='comment_postinfo']/div[2]/div[@class='comment_area']/div[@class='comment-content clearfix']/div[1]/span/p"):
            reviews.append(node.xpath('string()').extract());
        authors = response.xpath("//ol[@class='commentlist clearfix']").extract()
        headings = response.xpath("//div[@id='ItemReviewsContent']/div/div[@class='ReviewCommentContent']/div[@class='ReviewCommentContentRight']/h3/a/text()").extract()
        website_name = response.xpath("/html/head/meta[9]/@content").extract()
        img_src = response.xpath("//div[@class='tabBody']/ul[@id='commentsul']/li/div/div/div[@class='userAvatar']/img/@src").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], None, authors[item], category,
                                         servicename, reviews[item], img_src, website_name)
            servicename1.save()

        next_page = response.xpath("//div[@class='pagination']/ul[@id='yw2']/li[@class='next']/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page[0])
            print(next_page_url)
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url, callback=self.parsing)
