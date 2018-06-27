# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue

import scrapy
from scrapy import Request
from scrapy.crawler import  CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from services.siteservices.SiteJabberURLCrawler import SiteJabberURLCrawler
from services.SiteJabberCrawler import SiteJabberCrawler

final_dict_urls= {}
dict_url = {}
class SiteServiceListController(scrapy.Spider):
    start_urls = []

    def __init__(self, link):
        if (len(self.start_urls) > 0):
            self.start_urls.pop(0)
        self.start_urls.append(link["url"])
        category = link["Category"];
        dict_url[link["url"]] = {"Category": category}

    def closed(self, reason):
        pass

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers,meta={'dont_merge_cookies': True})

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        if ('sitejabber.com' in response.url):
            if('reviews' in response.url):
                service  = response.url.split("/");
                serviceName = service[len(service)-1];
                print(" Servicesssss   ", serviceName)
                crawler = SiteJabberCrawler( dict_url[response.url]["Category"],serviceName,response.url)
            else:
                crawler = SiteJabberURLCrawler(dict_url[response.url]["Category"])


        else:
            print("Found Nothing")
        if (crawler != None):
            return crawler.crawl(response)

def f(q, ):
    try:
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        deferred = runner.crawl(SiteServiceListController, q[1])
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q[0].put(None)
    except Exception as e:
        q[0].put(e)

def run_spider(urls):
    q = Queue()
    p = Process(target=f, args=([q, urls],))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result
def crawl_services1(urls):
    for i in urls:
        run_spider(i)

