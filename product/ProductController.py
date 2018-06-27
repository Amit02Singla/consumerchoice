from product.amazon import AmazonController, Amazon
from utils import GetProxyList
urllist = []
def crawlAmazon(urls):
    global  urllist
    urllist = urls
    #GetProxyList.getProxy();
    onProxyUpdated()
def onProxyUpdated():
    for url in urllist:
        AmazonController.crawlamazon(url)

if __name__ == '__main__':
    crawlAmazon(["https://www.amazon.com/Vehicles/b/ref=topnav_storetab_vehicles?ie=UTF8&node=10677469011"])
