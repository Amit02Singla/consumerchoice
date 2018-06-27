import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue

from product.amazon.settings import updateProxies


class GetProxyList(scrapy.Spider):
    start_urls = ["https://www.sslproxies.org/"]
    q = Queue()
    def __init__(self, link,q1):
        if (len(self.start_urls) > 0):
            self.start_urls.pop(0)
        global q
        q = q1
        self.start_urls.append(link)

    def closed(self, reason):
        proxyips = []
        i = 0
        for propyip in self.proxy_ip_list:
            proxyips.append("http://"+propyip+":"+self.proxy_port_list[i])
            i = i+1
        global  q
        q.put(proxyips)
        reactor.stop()


    def parse(self,response):
        self.proxy_ip_list = response.xpath("//table[@id='proxylisttable']/tbody/tr/td[1]/text()").extract()
        self.proxy_port_list = response.xpath("//table[@id='proxylisttable']/tbody/tr/td[2]/text()").extract()
        yield


def f(q):
    try:
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        deferred = runner.crawl(GetProxyList,"https://www.sslproxies.org/",q)
        deferred.addBoth(lambda _: reactor.stop())
        print("method f")
        reactor.run()
        q.put(None)
    except Exception as e:
        print(e)

def getProxy():
    q = Queue()
    p = Process(target=f, args=([q]))
    print("crawl_services()")
    p.start()
    result = q.get()
    updateProxies(result)
    p.join()

