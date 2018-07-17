from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
#TODO Done
# http://www.yscam.com/blackpeoplemeet-com-08
class Yscam(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(Yscam,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #print("review from yscam.com")
        for node in response.xpath("//body/section[@class='row body inside']/section[@class='comments-block']/section[@class='commentblock  ']/div[@class='comment  ']/div"):
            reviews.append(node.xpath('string()').extract());
        reviews = [[s.strip() for s in nested] for nested in reviews]
        i = 0
        count = 0
        while i < len(reviews):
            if reviews[i][0] == 'Mark as Useful' or reviews[i][0] == 'Post Reply' :
                del reviews[i]
                count = count + 1
                while (i < len(reviews) and (reviews[i][0] == 'Mark as useful' or reviews[i][0] == 'Post Reply')):
                    del reviews[i]
                    count = count + 1
            i = i + 1
        ratings = response.xpath("//body/section[@class='row body inside']/section[@class='comments-block']/section[@class='commentblock  ']/div[@class='comment  ']/ul[@class='postby']/li[2]/span[@class='smallStars']/@data-score").extract()
        dates = response.xpath("//body/section[@class='row body inside']/section[@class='comments-block']/section[@class='commentblock  ']/div[@class='comment  ']/ul[@class='postby']/li[1]/text()").extract()
        # headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        # authors = response.xpath("//div[@class='cust_review']/table/tbody/tr[3]/td[@class='customer']").extract()
        website_name = "yscam.com"
        # img_src = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/img[@class='avatar avatar-74 photo']/@src").extract()
        print("dates ", len(dates))
        print(" Reviews ", len(reviews))
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], None,
                                         "", self.servicename, reviews[item], None, website_name)
            self.save(servicename1)

        next_page = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                #print(type(next_page_url))
                #print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()




