import os
import random
from datetime import datetime
from urlparse import urlparse

from time import sleep
import eventlet

from utils import GetProxyList

requests = eventlet.import_patched('requests.__init__')
time = eventlet.import_patched('time')
#import redis

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from product.amazon import settings

num_requests = 0

#redis = redis.StrictRedis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)


def make_request(url, return_soup=True):
    # global request building and response handling
    GetProxyList.getProxy();

    url = format_url(url,get_host(url))

    if "picassoRedirect" in url:
        return None  # skip the redirect URLs

    global num_requests
    if num_requests >= settings.max_requests:
        raise Exception("Reached the max number of requests: {}".format(settings.max_requests))

    proxies = get_proxy()
    print(proxies)
    try:
        r = requests.get(url, headers=settings.headers, proxies=proxies)
    except RequestException as e:
        sleep(5)
        log("WARNING: Request for {} failed, trying again.".format(url))
        return make_request(url,return_soup)  # try request again, recursively

    num_requests += 1

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        log("WARNING: Got a {} status code for URL: {}".format(r.status_code, url))
        return None

    if return_soup:
        return BeautifulSoup(r.text), r.text
    return r

def get_host(url):
    u = urlparse(url)
    scheme = u.scheme or "https"
    host = scheme+"://"+u.netloc or "www.amazon.com"
    return host

def format_url(url,host):
    # make sure URLs aren't relative, and strip unnecssary query args
    u = urlparse(url)

    path = u.path

    if not u.query:
        query = ""
    else:
        query = "?"
        for piece in u.query.split("&"):
            k, v = piece.split("=")
            if k in settings.allowed_params:
                query += "{k}={v}&".format(**locals())
        query = query[:-1]

    return "{host}{path}{query}".format(**locals())


def log(msg):
    # global logging function
    if settings.log_stdout:
        try:
            print("{}: {}".format(datetime.now(), msg))
        except UnicodeEncodeError:
            pass  # squash logging errors in case of non-ascii text


def get_proxy():
    # choose a proxy server to use for this request, if we need one
    if not settings.proxies or len(settings.proxies) == 0:
        return None

    proxy_ip = random.choice(settings.proxies)

    return {
        "http": proxy_ip,
        "https": proxy_ip,
        "no_proxy": proxy_ip
    }
redis  =[];
def enqueue_url(u,baseUrl):
    host =  get_host(baseUrl)
    url = format_url(u,host)
    return redis.append(url)


def dequeue_url():
    return redis[-1]


if __name__ == '__main__':
    # test proxy server IP masking
    r = make_request('https://api.ipify.org?format=json', return_soup=False)
    print(r.text)