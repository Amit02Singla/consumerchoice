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
    crawlAmazon(["https://www.amazon.ca/pc-laptop-computer-microsoft-surface/b/ref=nav_shopall_mj_ce_all_comp?ie=UTF8&node=2404990011"])
