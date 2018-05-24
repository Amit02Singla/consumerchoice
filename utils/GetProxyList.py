import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue


class GetProxyList(scrapy.Spider):
    start_urls = ["https://www.sslproxies.org/"]

    def __init__(self, link):
        if (len(self.start_urls) > 0):
            self.start_urls.pop(0)
        self.start_urls.append(link)

    def closed(self, reason):
        proxyips = []
        i = 0
        for propyip in self.proxy_ip_list:
            proxyips.append("http://"+propyip+":"+self.proxy_port_list[i])
            i = i+1
        reactor.stop()


    def parse(self,response):
        self.proxy_ip_list = response.xpath("//table[@id='proxylisttable']/tbody/tr/td[1]/text()").extract()
        self.proxy_port_list = response.xpath("//table[@id='proxylisttable']/tbody/tr/td[2]/text()").extract()
        yield


def f(q):
    try:
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        deferred = runner.crawl(GetProxyList,"https://www.sslproxies.org/")
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
    p.join()

