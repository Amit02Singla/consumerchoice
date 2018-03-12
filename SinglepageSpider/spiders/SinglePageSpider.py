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
        #selector = HtmlXPathSelector(response)
        if( response.xpath("//div[@class = 'we-clamp we-clamp--lines-6 ember-view']").extract_first()):
            print("Found itunes reviews")
            #reviews =  response.xpath("//div[@class = 'we-clamp we-clamp--lines-6 ember-view']/span/text()").extract()
            for node in response.xpath('//div[@class="we-clamp we-clamp--lines-6 ember-view"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = response.xpath("//figure[@class='we-customer-review__rating we-star-rating ember-view']/@aria-label").extract()

            for item in range(0,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                            "url": response.url,
                            "ratings": ratings[item]}
                #print(dict_reviews)
            final_dict_reviews.update(dict_reviews)
            #print ("@@@@@@@@@@ITunes reviews" +str(len(reviews))+ str(len(dict_reviews))+str(len(final_dict_reviews)))
            #print final_dict_reviews
        elif(response.xpath("//div[@class='review-text']").extract()):
            print("Play Store reviews")
            for node in response.xpath('//div[@class="review-text"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = response.xpath("//div[@class='tiny-star star-rating-non-editable-container']/@aria-label").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings[item]}  
            final_dict_reviews.update(dict_reviews)
            #print ("***********ITunes reviews" + str(len(reviews))+str(len(final_dict_reviews)))
            #print final_dict_reviews
        elif(response.xpath("//div[@class='user-review-content']")):
            for node in response.xpath('//div[@class="user-review-content"]'):
                reviews.append(node.xpath('string()').extract());
            ratings= 6.2
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings}  
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath("//div[@class='posting fullpost']")):
             for node in response.xpath('//div[@class="posting fullpost"]'):
                 reviews.append(node.xpath('string()').extract());
             ratings= 0
             for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings}  
             final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="user-review-content"]')):
            for node in response.xpath('//div[@class="user-review-content"]'):
                reviews.append(node.xpath('string()').extract());
            ratings = 8.2
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings}  
            final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="comment-content"]')):
             for node in response.xpath('//div[@class="comment-content"]'):
                 reviews.append(node.xpath('string()').extract());
             ratings = 8.2
             for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings}  
             final_dict_reviews.update(dict_reviews)
        elif( response.xpath('//div[@class="wc-comment-text"]')):
             for node in response.xpath('//div[@class="wc-comment-text"]'):
                 reviews.append(node.xpath('string()').extract());
             ratings= 7.8
             for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings}  
             final_dict_reviews.update(dict_reviews)
        elif(response.xpath('//div[@class="review "]/p')):
            for node in response.xpath('//div[@class="review "]/p'):   
                 reviews.append(node.xpath('string()').extract());
            ratings= response.xpath("//div[@class='star_rating']/@title").extract()
            for item in range(1,len(reviews)):
                dict_reviews[str(response.url+str([item]))] = {"review": reviews[item],
                             "url": response.url,
                             "ratings": ratings}  
            final_dict_reviews.update(dict_reviews)
        else: 
            print ("kuch nhi mila")
        
        #reviews =  response.xpath("//div[@class = 'review-body with-review-wrapper']/text()").extract()
        #divs = selector.xpath('//div[re:test(@class, ".*review.*|.*comment.*|posting fullpost")]')
        #temp_review = []
        '''for node in response.xpath('//div[@class="user-review-content"]'):
            temp_reviews.append(node.xpath('string()').extract());
        reviews = temp_reviews
        print reviews'''
        
        '''elif(response.xpath('//div[@class="review-info__body"]')):
             for node in response.xpath('//div[@class="review-info__body"]'):
                 reviews.append(node.xpath('string()').extract());'''
        
            
    
if __name__ == '__main__':
       process = CrawlerProcess(get_project_settings())
       process.crawl(SinglepagespiderSpider)
       process.start()
       #print final_dict_reviews
       
       with open("reviews.json","w") as f:
                json.dump(final_dict_reviews,f)
       print("Writing json file")