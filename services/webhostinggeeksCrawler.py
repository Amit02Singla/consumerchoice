from model.Servicemodel import ServiceRecord
from utils.utils import getStarts
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class webhostinggeeksCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(webhostinggeeksCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://webhostinggeeks.com/providers/hostgator?product=shared
        for node in response.xpath('//div[@class="text_description"]'):
            reviews.append(node.xpath('string()').extract());
        dates =  response.xpath("//div[@class='top_line']/span/text()").extract()
        headings = response.xpath("//div[@class='info_description']/p[@class='title_description ']/a/text()").extract()
        authors = response.xpath("//div[@class='user-text']/p/text()").extract()
        ratings1 = response.xpath("//li/div[@class='row-comment']/div[@class='card_user']/ul[@class='rating_block']/li/div[@class='rating-stars-empty small-star']/div/@style").extract()
        website_name =  response.xpath("//div[@class='center_wrapper']/div[@class='col-sm-6 col-md-4 col-lg-4']/a[@class='btn bg-orange-600 visit-host-link']/@href").extract()[0]
        ratings = []
        j = 0
        i = 0
        c = 0
        while i < len(ratings1):
            j = j+1;
            if(j/5==1):
                c= c + (int(getStarts(ratings1[j])))/20.0;
                ratings.append(c/5.0)
                j=0;
            else:
                c = c + (int(getStarts(ratings1[j]))) / 20.0;

            i = i + 1

        print("Reviews ", len(reviews), reviews)
        print("Headings ", len(headings), headings)
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("website ", website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url,None,headings[item],dates[item],authors[item],self.category,self.servicename,reviews[item],"",website_name);
            self.save(servicename1)
        self.pushToServer()