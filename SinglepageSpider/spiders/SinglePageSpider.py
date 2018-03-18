# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#from scrapy.selector import HtmlXPathSelector 
import json


final_dict_reviews= {}

class SinglepagespiderSpider(scrapy.Spider):
    
    name = 'SinglePageSpider'
    def __init__(self):
        with open("temp.txt", 'r') as f:
            self.start_urls = f.read().split("\n")
        #print(start_urls);
    
    def parse(self, response):
        self.log('I just visited: ' + response.url)
        dict_reviews = {}
        reviews= []
        if(response.xpath('//div[@class="review-info__body"]')):
            print("Reviews from Trustpilot.com")
            #https://www.trustpilot.com/review/expressvpn.com
            for node in response.xpath('//div[@class="review-info__body"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = response.xpath("//div[@class='review-info__header__verified']/div/meta[@itemprop='ratingValue']/@content").extract()
            dates=  response.xpath("//div[@class='header__verified__date']/time/text()").extract()
            headings =  response.xpath("//div[@class='review-info__body']/h2/a/text()").extract()
            authors = response.xpath("//div[@class='consumer-info__details']/h3/text()").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "heading": headings[item],
                             "date": dates[item],
                             "author" : authors[item]} 
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="user-review-content"]')):
            print("review from Hostingfacts.com")
            #https://hostadvice.com/hosting-company/godaddy-reviews/
            for node in response.xpath('//div[@class="user-review-content"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = response.xpath("//div[@class= 'user-review']/header/section/span[@class='user-review-rating']/span[@class='value']/text()").extract()
            dates =  response.xpath("//div[@class= 'user-review']/header/section/span[@class='user-review-meta']/text()").extract()
            headings = response.xpath("//div[@class= 'user-review']/section/p[@class='user-review-title']/text()").extract()
            authors = response.xpath("//div[@class='user-review']/header/section/p[@class='user-review-name']/a/span/text()").extract()            
            img_src =  response.xpath("//div[@class='sidebar-padder']/aside/img[@class='img-responsive banner-image center-block']/@src").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "heading": headings[item],
                             "date": dates[item],
                             "author" : authors[item],
                             "Image Source": img_src} 
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="review-summary"]')):
            print("Hostadvice.com")
            for node in response.xpath('//div[@class="review-summary"]'):
                reviews.append(node.xpath('string()').extract());
            ratings=  response.xpath("//div[@class='review-rating clearfix']/span[@class='review-score']/text()").extract()
            headings =  response.xpath("//div[@class='review-content']/h3[@class='review_header']/text()").extract()
            authors = response.xpath("//div[@class='review-author']/strong/text()").extract()
            img_src =  response.xpath("//div[@class='col-md-offset-1 col-md-5 col-xs-6']/img[ @class='attachment-post-thumbnail size-post-thumbnail wp-post-image']/@src").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "heading": headings[item],
                             "author" : authors[item],
                             "Image Source": img_src} 
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="comment pure-u-1 wcc"]')):
            print("whoishostingthis.com")
            #https://www.whoishostingthis.com/hosting-reviews/bluehost/
            for node in response.xpath('//div[@class="comment pure-u-1 wcc"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = response.xpath("//div[@class='user-info pure-u-1']/img[@class='stars overall']/@alt").extract()
            dates =  response.xpath("//div[@class='user-info pure-u-1']/time/@content").extract() 
            authors =  response.xpath("//div[@class='author']/span[@class='name']/text()").extract()
            img_src =  response.xpath("//div[@class='host-info wcc']/a[1]/img[@class=' logo']/@src").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "author" : authors[item],
                             "Image Source": img_src} 
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="review "]/p')):
            print("Reviews from sitejabber.com")
            #https://www.sitejabber.com/reviews/zoosk.com
            for node in response.xpath('//div[@class="review "]/p'):   
                 reviews.append(node.xpath('string()').extract());
            ratings= response.xpath("//div[@class='star_rating']/@title").extract()
            dates =  response.xpath("//div[@class='time tiny_text faded_text']/text()").extract()
            headings =  response.xpath("//div[@class='review_title']/a/text()").extract()
            authors=  response.xpath("//div[@class='author_name']/a/text()").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings,
                             "heading": headings[item],
                             "date": dates[item],
                             "author" : authors[item]}  
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="comment-content"]')):
            print("Reviews from bestvpn.com")
            #https://www.bestvpn.com/expressvpn-review/
            for node in response.xpath('//div[@class="comment-content"]'):
                 reviews.append(node.xpath('string()').extract());
            ratings = 8.2
            dates =response.xpath("//div[@class='comment-metadata']/time/text()").extract()
            authors = response.xpath("//div[@class='comment-author vcard']/b/text()").extract()
            img_src =  response.xpath("//div[@class='review-excerpt row']/div[@class='col-lg-6'][1]/a/img[@class='logo']/@src").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings,
                             "date": dates[item],
                             "author" : authors[item],
                             "Image Source": img_src}  
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//p[@class="review-body"]')):
            print("Reviews from Resellerrating.com")
            #https://www.resellerratings.com/store/Nordvpn_com
            for node in response.xpath('//p[@class="review-body"]'):
                    reviews.append(node.xpath('string()').extract());
            dates = response.xpath("//div[@class='comment']/div[2]/div[@class='date fr']/span/text()").extract()
            ratings = response.xpath("//div[@class='rating fl']/meta[@itemprop='ratingValue']/@content").extract()
            authors =  response.xpath("//div[@class='review'][1]/div[@class='row']/div[@class='three mobile-one columns']/div[@class='avatar']/div[@class='user']/meta/@content").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings,
                             "date": dates[item],
                             "author" : authors[item],
                             "Image Source": img_src}  
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="review-comments  color-text"]')):
            print("Reviews from Capterra.con")
            #https://www.capterra.com/p/170765/ExpressVPN/
            for node in response.xpath('//div[@class="review-comments  color-text"]'): 
                reviews.append(node.xpath('string()').extract());
            ratings =  response.xpath("//div[@class='overall-rating-container']/span[@class='overall-rating']/span/text()").extract()
            headings =  response.xpath("//div[@class='cell seven-eighths  palm-one-whole']/h3/q/text()").extract()
            dates =  response.xpath("//div[@class='grid']/div[@class='cell one-eighth  palm-one-whole']/div[@class='quarter-margin-bottom  micro  color-gray  weight-normal  text-right  palm-text-left']/text()").extract()
            img_src = response.xpath("//div[@class='thumbnail  no-hover  listing-thumbnail']/img/@src").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "date": dates[item],
                             "Image Source": img_src}  
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="review_top"]/p')):
            print("Reviews from Forexbrokerz.com")
            #https://www.forexbrokerz.com/brokers/binance-review
            for node in response.xpath('//div[@class="review_top"]/p'):
                  reviews.append(node.xpath('string()').extract());
            headings =  response.xpath("//div[@class='review']/div[@class='review_top']/span/h3/a/text()").extract()
            dates = response.xpath("//div[@class='review_details']/span/text()").extract()
            ratings =  response.xpath("//div[@class='review_details']/div/div/a/text()").extract()
            authors = response.xpath("//div[@class='review_details']/span/strong/text()").extract()
            img_src =  response.xpath("//div[@class='broker_img_container']/img/@src").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "date": dates[item],
                             "authors": authors[item],
                             "Image Source": img_src}  
            final_dict_reviews.update(dict_reviews)
        else: 
            print ("kuch nhi mila")
        #selector = HtmlXPathSelector(response)
        '''if( response.xpath("//div[@class = 'we-clamp we-clamp--lines-6 ember-view']").extract_first()):
            print("Found itunes reviews")
            #reviews =  response.xpath("//div[@class = 'we-clamp we-clamp--lines-6 ember-view']/span/text()").extract()
            for node in response.xpath('//div[@class="we-clamp we-clamp--lines-6 ember-view"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = response.xpath("//figure[@class='we-customer-review__rating we-star-rating ember-view']/@aria-label").extract()
            headings =response.xpath("//div[@class='we-customer-review__header']/h3/text()").extract()
            dates =  response.xpath("//div[@class='we-customer-review__header']/h4/time/@aria-label").extract()
            authors = response.xpath("//div[@class='we-customer-review__user we-truncate we-truncate--single-line ember-view']/text()").extract()
            for item in range(0,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                            "url": response.url,
                            "ratings": ratings[item],
                            "heading": headings[item],
                            "date": dates[item],
                            "author" : authors[item]}
                #print(dict_reviews)
            final_dict_reviews.update(dict_reviews)
            #print ("@@@@@@@@@@ITunes reviews" +str(len(reviews))+ str(len(dict_reviews))+str(len(final_dict_reviews)))
            #print final_dict_reviews
        elif(response.xpath("//div[@class='review-text']").extract()):
            print("Play Store reviews")
            for node in response.xpath('//div[@class="review-text"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = response.xpath("//div[@class='tiny-star star-rating-non-editable-container']/@aria-label").extract()
            dates = response.xpath("//div[@class = 'review-info']/span[@class='review-date']/text()").extract()
            authors = response.xpath("//div[@class = 'review-info']/span[@class='author-name']/text()").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "date":dates[item],
                             "author": authors[item]}  
            final_dict_reviews.update(dict_reviews)
            #print ("***********ITunes reviews" + str(len(reviews))+str(len(final_dict_reviews)))
            #print final_dict_reviews
        elif(response.xpath("//div[@class='posting fullpost']")):
             for node in response.xpath('//div[@class="posting fullpost"]'):
                 reviews.append(node.xpath('string()').extract());
             ratings= 0
             dates = response.xpath("//div[@class='author-date']/text()").extract()
             headings = response.xpath("//div[@class='subject']/text()").extract()
             authors =response.xpath("//div[@class='author-name']/a/text()").extract()
             for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings,
                             "heading": headings[item],
                             "date": dates[item],
                             "author" : authors[item]}  
             final_dict_reviews.update(dict_reviews)
        
        elif( response.xpath('//div[@class="wc-comment-text"]')):
             for node in response.xpath('//div[@class="wc-comment-text"]'):
                 reviews.append(node.xpath('string()').extract());
             ratings= 7.8
             authors=  response.xpath("//div[@class='wc-comment-author wcai-uname-info wcai-not-clicked']/text()").extract()
             for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings,
                             "author": authors[item]}  
             final_dict_reviews.update(dict_reviews)
       
        elif(response.xpath("//div[@class='user-review-content']")):
            for node in response.xpath('//div[@class="user-review-content"]'):
                reviews.append(node.xpath('string()').extract());
            ratings=  response.xpath("//div[@class='user-review-content-column']/p/span[@class='user-review-rating']/span[@class='value']/text()").extract()            
            dates = response.xpath("//div[@class='user-review-content-column']/p/span[@class='user-review-meta']/text()").extract()
            headings=  response.xpath("//div[@class='user-review-content-column']/p[@class='user-review-title']/text()").extract()
            temp_authors = authors = response.xpath("//div[@class='user-review-content-column']/p[@class='user-review-name']/text()").extract()
            authors= []
            for i in range(1,len(temp_authors)):
                 if(temp_authors[i]):
                     authors.append(temp_authors[i])
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item],
                             "heading": headings[item],
                             "date": dates[item],
                             "author" : authors[item]} 
            final_dict_reviews.update(dict_reviews)'''
        
        
        #reviews =  response.xpath("//div[@class = 'review-body with-review-wrapper']/text()").extract()
        #divs = selector.xpath('//div[re:test(@class, ".*review.*|.*comment.*|posting fullpost")]')
        #temp_review = []
        
            
    
if __name__ == '__main__':
       process = CrawlerProcess(get_project_settings())
       process.crawl(SinglepagespiderSpider)
       process.start()
       #print final_dict_reviews
       
       with open("reviews.json","w") as f:
                json.dump(final_dict_reviews,f)
       print("Writing json file")