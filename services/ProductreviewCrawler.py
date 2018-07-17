from model.Servicemodel import ServiceRecord

from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class ProductreviewCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ProductreviewCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("review from productreview.com")
        # https://www.productreview.com.au/p/smart-fares.html
        for node in response.xpath("//div[@class='review-overall']"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='rating-md']/p/span/span[@itemprop='ratingValue']/@content").extract()
        headings = response.xpath("//div[@class='review-content']/h3/text()").extract()
        dates =  response.xpath("//div[@class='review-content']/div[@class='rating-md']/p/meta/@content").extract()
        authors = response.xpath("//div[@class='review-author']/h6/a/text()").extract()
        img_src =  response.xpath("//div[@class='item-header-img']/span[@class='item-header-img-container']/img/@src").extract()
        website_name =  "productreview.com.au"
        dates = response.xpath("//div[@class='review-content']/div[@class='rating-md']/p/meta/@content").extract()
        print("dates ", len(dates), dates)
        print(" Reviews ", len(reviews), reviews)
        print(" headings ", len(headings), headings)
        print(" authors ", len(authors), authors)
        print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], self.category,
                          self.servicename, reviews[item],img_src[0],website_name);
            self.save(servicename1)

        next_page = response.xpath("//div[@class='pagination-container']/ul[@class='pagination']/li[7]/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()