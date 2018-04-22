from model.Servicemodel import ServiceRecord


class ProductreviewCrawler():
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        reviews = []
        print("Product Review")
        # https://www.productreview.com.au/p/smart-fares.html
        #TODO date missing--done
        for node in response.xpath("//div[@class='review-overall']"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='rating-md']/p/span/span[@itemprop='ratingValue']/@content").extract()
        headings = response.xpath("//div[@class='review-content']/h3/text()").extract()
        dates =  response.xpath("//div[@class='review-content']/div[@class='rating-md']/p/meta/@content").extract()
        authors = response.xpath("//div[@class='review-author']/h6/a/text()").extract()
        img_src =  response.xpath("//div[@class='item-header-img']/span[@class='item-header-img-container']/img/@src").extract()
        website_name =  response.xpath("/html/head/meta[7]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], category,
                          servicename, reviews[item],img_src,website_name);
            servicename1.save()