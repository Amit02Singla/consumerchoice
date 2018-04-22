import json
import sys
from datetime import datetime

import eventlet

from product.amazon import settings
from product.amazon.Amazon import ParseReviews
from product.amazon.extractors import get_url, get_primary_img
from product.amazon.helpers import make_request, log, format_url, enqueue_url, dequeue_url

crawl_time = datetime.now()

pool = eventlet.GreenPool(settings.max_threads)
pile = eventlet.GreenPile(pool)


def begin_crawl(url):

    page, html = make_request(url)
    count = 0
    # look for subcategory links on this page
    subcategories = page.findAll("div", "bxc-grid__image")  # downward arrow graphics
    subcategories.extend(page.findAll("li", "sub-categories__list__item"))  # carousel hover menu
    sidebar = page.find("div", "browseBox")
    if sidebar:
        subcategories.extend(sidebar.findAll("li"))  # left sidebar

    for subcategory in subcategories:
        link = subcategory.find("a")
        if not link:
            continue
        link = link["href"]
        count += 1
        enqueue_url(link)

    log("Found {} subcategories on {}".format(count, line))


def fetch_listing():

    global crawl_time
    url = dequeue_url()
    if not url:
        log("WARNING: No URLs found in the queue. Retrying...")
        pile.spawn(fetch_listing)
        return

    page, html = make_request(url)
    if not page:
        return
    items = page.findAll("li", "s-result-item")
    log("Found {} items on {}".format(len(items), url))

    for item in items[:settings.max_details_per_listing]:

        product_image = get_primary_img(item)
        if not product_image:
            log("No product image detected, skipping")
            continue

       # product_title = get_title(item)
        product_url = get_url(item)
        data = ParseReviews(product_url)
      #  product_price = get_price(item)
        data
        data.update({'Product URL': format_url(product_url),
                     "Listing URL":format_url(url),
                     "Product Image":product_image,
                     })
        
        f = open('data.json','a')
        json.dump(data,f,indent=4)
        # download_image(product_image, product_id)

    # add next page to queue
    next_link = page.find("a", id="pagnNextLink")
    if next_link:
        log(" Found 'Next' link on {}: {}".format(url, next_link["href"]))
        enqueue_url(next_link["href"])
        pile.spawn(fetch_listing)


def crawlamazon(url):

    begin_crawl(url)  # put a bunch of subcategory URLs into the queue
    log("Beginning crawl at {}".format(crawl_time))
    [pile.spawn(fetch_listing) for _ in range(settings.max_threads)]
    pool.waitall()
