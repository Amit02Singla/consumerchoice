from model.Servicemodel import ServiceRecord
from lxml import etree

#URL https://www.comparitech.com/vpn/reviews/expressvpn/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class CompariTech(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}

        super(CompariTech,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):

        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        root = etree.HTML(response)
        print("review from comparitech.com")
        for node in root.xpath(".//ul[@class='comment-list']/li/article/div[@class='comment-content']"):
            reviews.append([node.xpath('string()')]);
        # ratings = response.xpath("//div[@class='box col-12 review-title']/meta[@itemprop='ratingValue']/@content").extract()
        dates = root.xpath(".//ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-metadata']/a/time/text()")
        # headings = root.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        authors1 = root.xpath(".//ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/b[@class='fn']")
        website_name = "comparitech.com"
        # img_src = root.xpath(".//div[@class='main wrapper clearfix']/div[@class='section'][2]/div[@class='review--summary full-width large-cta']/div[@class='review-summary-section top']/a[@class='review-summary-column image centered-no-stretch']/@style")
        # img_src = str(img_src[0]).split("'")[1]
        authors = []
        for root1 in authors1:
            if(len(root1.xpath("//b/text()"))>0):
                authors.append(root1.xpath("//b/text()")[2])
            else:
                authors.append("")

        print("reviews ", len(reviews), reviews)
        print("dates ", len(dates))
        print("authors ", len(authors), authors)
        # print("img_src ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(self.link["url"], None, None, dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()






