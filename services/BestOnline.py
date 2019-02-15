from model.Servicemodel import ServiceRecord
from lxml import etree
#url "https://www.10bestonline.com/top_10_best_online_dating_reviews/eHarmony_customer_reviews/"
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class BestOnline(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BestOnline,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
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
            ratings.append(str(round((float(rate[i])+float(rate[i+1])+float(rate[i+2])+float(rate[i+3])+float(rate[i+4])+float(rate[i+5]))/6.0, 1)))
            i= i+6


        # ratings = response.xpath("//div[@class='box col-12 review-title']/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@class='customer_reviews']/div/div[@class='cust_review']/table/tr[2]/td[@class='customer']/text()").extract()
        headings = response.xpath("//div[@class='cust_review']/table/tr/th[@class= 'title']/text()").extract()
        authors = response.xpath("//div[@class='cust_review']/table/tr[3]/td[@class='customer']/text()").extract()
        website_name = response.xpath("//div[@class='customer_reviews']/div[@class='button_link button_visit']/a[@class='review_reminder_fancybox']/@href").extract()[0]
        website_name = 'https://www.10bestonline.com/'+website_name
        print("website name"+ website_name)
        if(len(authors) == 1):
            if authors[0]== "Your Name":
                reviews = []
                dates= []
                authors = []
                headings = []
                ratings = []
        print "reviews ", len(reviews)
        print "ratings  ", len(ratings)
        print "dates    ", len(dates)
        print "headings ", len(headings)
        print "authors ", len(authors)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)

        next_page = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()




