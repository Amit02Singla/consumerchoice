from model.Servicemodel import ServiceRecord

class consumerAffairsCrawler():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from Consumeraffairs.com")
        # https://www.consumeraffairs.com/internet/godaddy.html
        for node in response.xpath("//div[@class='campaign-reviews__regular-container js-campaign-reviews__regular-container']/div/div[@class='rvw-bd ca-txt-bd-2']/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='stars-rtg stars-rtg--sm']/@data-rating").extract()
        ratings.pop(0)
        ratings.pop(0)
        ratings.pop(0)
        ratings.pop(0)
        ratings.pop(0)
        temp_dates = response.xpath("//div[@class='rvw-bd ca-txt-bd-2']/span[@class='ca-txt-cpt ca-txt--clr-gray']/text()").extract()
        dates = []
        for date in temp_dates:
            dates.append(date.split(":")[1])
        authors =  response.xpath("//div[@class='rvw-aut']/div[@class='rvw-aut__inf']/strong[@class='rvw-aut__inf-nm']/text()").extract()
        website_name = response.xpath("//html/head/meta[3]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category, servicename,
                                         reviews[item], None, website_name)
            servicename1.save()
        next_page = response.xpath("//div[@class='prf-lst']/nav[@class='prf-pgr js-profile-pager']/a[@class='ca-a-md "
                                   "ca-a-uprcs ca-a-blk prf-pgr__nxt js-profile-pager__next']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url, "    url")
                yield response.follow(url=next_page_url, callback=self.parsing)
