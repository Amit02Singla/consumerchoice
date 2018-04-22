from model.Servicemodel import ServiceRecord


class hostAdvisor():
    def __init__(self):
        pass

    def parsing(self, response):
        return self.crawl(response, self.category, self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        # https://www.hostadvisor.com/reviews/shared-web-hosting/bluehost
        for node in response.xpath("//div[@class='textHolder']/div[2]/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='textHolder']/div/span/meta[@itemprop='ratingValue']/@content").extract()
        # dates = response.xpath("//div[@class='review-mid']/p/text()").extract()
        headings = response.xpath("//div[@class='textHolder']/h5/text()").extract()
        img_src = response.xpath("//div[@class='user-img ']/img/@src").extract()
        authors = response.xpath("//div[@class='hidden-xs']/p[1]/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        authors = map(lambda s: s.strip(), authors)
        authors = list(filter(None, authors))
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], None, authors[item],
                                         category, servicename, reviews[item], img_src, website_name)
            servicename1.save()

        next_page = response.xpath("//div[@class='reviewBlock']/nav[@class='text-center']/ul[@class='pagination']/li[21]/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url, "    url")
                yield response.follow(url=next_page_url, callback=self.parsing)


