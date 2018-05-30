from model.Servicemodel import ServiceRecord
from lxml import etree
#TODO: 2-Raiting pending,incompletem header, raiting etc.
#url "https://www.10bestonline.com/top_10_best_online_dating_reviews/eHarmony_customer_reviews/"
class BestOnline():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from 10bestonline.com")
        for node in response.xpath("//div[@class='cust_review']/table/tr[5]/td[@class='comment']"):
            reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='box col-12 review-title']/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@class='customer_reviews']/div/div[@class='cust_review']/table/tr[2]/td[@class='customer']/text()").extract()
        # headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        authors = response.xpath("//div[@class='cust_review']/table/tr[3]/td[@class='customer']/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        # img_src = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/img[@class='avatar avatar-74 photo']/@src").extract()
        #print("Reviews ", len(reviews), reviews)
        # print("Headings ", len(headings), headings)
        #print("Authors ", len(authors), authors)
        # print("Rating ", len(ratings), ratings)
        #print("Dates ", len(dates), dates)
        # print("Img_src ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()

        next_page = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)




