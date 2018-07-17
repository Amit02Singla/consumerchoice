from model.Servicemodel import ServiceRecord
from lxml import etree


#TODO ask sahil
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class BlackPeopleMeet_PissedConsumer(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BlackPeopleMeet_PissedConsumer,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        ratings = []
        dates = []
        authors = []
        print("review from blackpeoplemeet.pissedconsumer.com")
        data = response.xpath("//div[@class='f-component-item review-item  ']").extract()
        for content in data:
            root = etree.HTML(content)
            reviews.append(root.xpath("//div[@class='f-component-info']/div[@class='f-component-text']/div[@class='overflow-text']/text()"))
            if(len(root.xpath("//div[@class='f-component-info-additional']/div[@class='evaluations f-component-info-row']/div[@class='star-rating']/div[@class='star-rating-row']/div[@class='rating-title']/text()"))>0):
                ratings.append(root.xpath("//div[@class='f-component-info-additional']/div[@class='evaluations f-component-info-row']/div[@class='star-rating']/div[@class='star-rating-row']/div[@class='rating-title']/text()")[0])
            else:
                ratings.append("")
            dates.append(root.xpath("//div[@class='f-component-info']/div[@class='f-component-info-header']/meta[@itemprop='datePublished']/@content")[0])
            if len(root.xpath("//div[@class='f-component-info-additional']/div[@class='f-component-info-row with-border']/span[@class='f-component-info-row-title last-title']/span[2]/span[@class='user link']/span[2]/text()")):
                authors.append(root.xpath("//div[@class='f-component-info-additional']/div[@class='f-component-info-row with-border']/span[@class='f-component-info-row-title last-title']/span[2]/span[@class='user link']/span[2]/text()")[0])
            else:
                authors.append("")
        # for node in response.xpath("//div[@class='middleware-review-container'][1]/div/div[@class='f-component-info']/div[@class='f-component-text']/div[@class='overflow-text']"):
        #     reviews.append(node.xpath('string()').extract());
        #
        # ratings = response.xpath("//body/section[@class='row body inside']/section[@class='comments-block']/section[@class='commentblock  ']/div[@class='comment  ']/ul[@class='postby']/li[2]/span[@class='smallStars']/@data-score").extract()
        # dates = response.xpath("//div[@class='middleware-review-container']/div/div[@class='f-component-info']/div[@class='f-component-info-header']/time[@class='post-time secondary-info']/text()").extract()
        website_name = "pissedconsumer.com"
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        next_page = response.xpath("//div[@class='pager pager-block']/ul[@class='pagination infinite-pager']/li[@class='next']/a/@href").extract()

        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(next_page_url, callback=self.parsing)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()





