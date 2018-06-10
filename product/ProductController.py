from product.amazon import AmazonController
from utils import GetProxyList
urllist = []
def crawlAmazon(urls):
    global  urllist
    urllist = urls
    GetProxyList.getProxy();
    onProxyUpdated()
def onProxyUpdated():
    for url in urllist:
        AmazonController.crawlamazon(url)

if __name__ == '__main__':
    crawlAmazon(["https://www.amazon.co.uk/Computer-Components/b/ref=nav_shopall_cc?ie=UTF8&node=428655031"])
