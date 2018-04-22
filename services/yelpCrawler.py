from model.Servicemodel import ServiceRecord

class yelpCrawler():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        # https://www.yelp.com/biz/fatcow-burlington
        for node in response.xpath('//div[@class="review-content"]'):
            reviews.append(node.xpath('string()').extract())

        ratings =  response.xpath("//div[@class='biz-rating biz-rating-large clearfix']/div/div/@title").extract()
        dates =  response.xpath("//div[@class='biz-rating biz-rating-large clearfix']/span[@class='rating-qualifier']/text()").extract()
        authors =  response.xpath("//div[@class='media-story']/ul[@class='user-passport-info']/li[@class='user-name']/a[@id='dropdown_user-name']/text()").extract()
        website_name =  response.xpath("//html/head/meta[6]/@content").extract()
        print(" Ratings ", len(ratings), ratings)
        print("dates ", len(dates), dates)
        print(" Reviews ", len(reviews), reviews)
        # print(" headings ", len(headings), headings)
        print(" authors ", len(authors), authors)
        print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url,ratings[item],None,dates[item],authors[item],category,servicename,reviews[item],"",website_name);
            servicename1.save()

        next_page = response.xpath("//div[@class='arrange_unit']/a[@class='u-decoration-none next pagination-links_anchor']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url, "    url")
                yield response.follow(url=next_page_url, callback=self.parsing)
