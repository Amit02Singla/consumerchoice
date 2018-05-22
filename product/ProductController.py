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
    crawlAmazon(["https://www.amazon.com/Home-Audio-Electronics/b/ref=nav_shopall_hat?ie=UTF8&node=667846011"])
