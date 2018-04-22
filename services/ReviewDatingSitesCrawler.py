from model.Servicemodel import ServiceRecord


class ReviewDatingSitesCrawler():
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        reviews = []
        print("Review Datingsites")
        # http://reviewsdatingsites.com/site/elitesingles
        for node in response.xpath("//div[@id='reviews']/div[@class='review']/div[@class='row']/div[@class='col-md-9']/div[@class='review-content']/p"):
            reviews.append(node.xpath('string()').extract())
        ratings =  response.xpath("//div[@class='col-md-9']/h4[@class='m-t-0']/span[@class='stars']/span[@itemprop='ratingValue']/@content").extract()
        authors =   response.xpath("//div[@class='media-body text-center']/div/strong/a[@itemprop='author']/text()").extract()
        website_name = response.xpath("//html/body/div[1]/meta[1]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, None, authors[item], category,
                          servicename, reviews[item],"",website_name);
            servicename1.save()