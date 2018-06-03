from model.Servicemodel import ServiceRecord


class ProductreviewCrawler():
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from productreview.com")
        # https://www.productreview.com.au/p/smart-fares.html
        for node in response.xpath("//div[@class='review-overall']"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='rating-md']/p/span/span[@itemprop='ratingValue']/@content").extract()
        headings = response.xpath("//div[@class='review-content']/h3/text()").extract()
        dates =  response.xpath("//div[@class='review-content']/div[@class='rating-md']/p/meta/@content").extract()
        authors = response.xpath("//div[@class='review-author']/h6/a/text()").extract()
        img_src =  response.xpath("//div[@class='item-header-img']/span[@class='item-header-img-container']/img/@src").extract()
        website_name =  response.xpath("/html/head/meta[7]/@content").extract()
        dates = response.xpath("//div[@class='review-content']/div[@class='rating-md']/p/meta/@content").extract()
        print("dates ", len(dates), dates)
        print(" Reviews ", len(reviews), reviews)
        print(" headings ", len(headings), headings)
        print(" authors ", len(authors), authors)
        print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], category,
                          servicename, reviews[item],img_src,website_name);
            servicename1.save()

        next_page = response.xpath("//div[@class='pagination-container']/ul[@class='pagination']/li[7]/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)