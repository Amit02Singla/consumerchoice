from model.Servicemodel import ServiceRecord
from lxml import etree
#TODO: 2-Raiting pending,incompletem header, raiting etc.: done
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
        stars = response.xpath("//div[@class='cust_review']/table/tr/td[@class= 'stars']/div/@class").extract()
        rate = []
        ratings= []
        for i in range(0,len(stars)):
            if(stars[i]== 'onestar_small'):
                rate.append("1")
            elif(stars[i]== 'twostars_small'):
                rate.append("2")
            elif (stars[i] == 'threestars_small'):
                rate.append("3")
            elif (stars[i] == 'fourstars_small'):
                rate.append("4")
            elif (stars[i] == 'fivestars_small'):
                rate.append("5")
        i=0
        while(i<len(rate)):
            ratings.append(str((int(rate[i])+int(rate[i+1])+int(rate[i+2])+int(rate[i+3])+int(rate[i+4])+int(rate[i+5]))/6))
            i= i+6


        # ratings = response.xpath("//div[@class='box col-12 review-title']/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@class='customer_reviews']/div/div[@class='cust_review']/table/tr[2]/td[@class='customer']/text()").extract()
        headings = response.xpath("//div[@class='cust_review']/table/tr/th[@class= 'title']/text()").extract()
        authors = response.xpath("//div[@class='cust_review']/table/tr[3]/td[@class='customer']/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        # img_src = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/img[@class='avatar avatar-74 photo']/@src").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
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




