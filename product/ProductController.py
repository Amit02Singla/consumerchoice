from product.amazon import AmazonController
def crawlAmazon(url):
    AmazonController.crawlamazon(url)

if __name__ == '__main__':
    AmazonController.crawlamazon("https://www.amazon.com/Home-Audio-Electronics/b/ref=nav_shopall_hat?ie=UTF8&node=667846011")