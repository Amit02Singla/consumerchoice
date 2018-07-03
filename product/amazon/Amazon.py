# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 21:49:30 2018

@author: madhvi.gupta
"""

import json
import re
from time import sleep

import requests
from dateutil import parser as dateparser
from lxml import html
from requests import RequestException

from product.amazon import settings
from product.amazon.helpers import get_proxy, log, get_host
from utils import utils
from product.amazon.helpers import make_request


def ParseReviews(url, productImage):
    # for i in range(5):
    #     try:
    # This script has only been tested with Amazon.com
    #Todo: check for subcategory and append it in json
    amazon_url =  url
    print(url)
    # Add some recent user agent to prevent amazon from blocking the request
    # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome

    product_image = []
    product_image.append(productImage)
    page = make_request(url, False)
    page_response = page.text
    parser = html.fromstring(page_response)
    XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
    XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
    XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
    XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
    XPATH_PRODUCT_NAME = "//div/h1/span[@id='productTitle']/text()"
    XPATH_PRODUCT_PRICE = "//span[@class='a-text-strike']/text()"
    XPATH_PRODUCT_AVAILABILITY = '//div[@id="availability"]/span/text()'
    XPATH_PRODUCT_CATEGORY = '//div[@id="wayfinding-breadcrumbs_feature_div"]/ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span[@class="a-list-item"]/a[@class="a-link-normal a-color-tertiary"]/text()'
    XPATH_PRODUCT_LIST_PRICE = "//span[@id='priceblock_ourprice']/text()"
    XPATH_PRODUCT_BRAND = '//div[@class="a-section a-spacing-none"]/a[@id="bylineInfo"]/text()'
    XPATH_PRODUCT_DESCRIPTION = "//div[@id='productDescription']/p/text()"
    XPATH_REVIEW_COUNT = "//div/span[@data-hook='total-review-count']/text()"
    XPATH_SUB_CATEGORY = '//div[@id="wayfinding-breadcrumbs_feature_div"]/ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span[@class="a-list-item"]/a[@class="a-link-normal a-color-tertiary"]/text()'
    XPATH_PRODUCT_BRAND = '//div[@class="a-section a-spacing-none"]/a[@id="bylineInfo"]/text()'
    raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
    if(len(raw_product_price) > 0):
        product_price = raw_product_price[0]
    else:
        product_price = None
    product_brand = parser.xpath(XPATH_PRODUCT_BRAND)
    raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
    product_name = ''.join(raw_product_name).strip()
    if product_name == '':
        return None
    log("Crawling PRODUCT  >>>>>>>>"+product_name)
    raw_product_description = parser.xpath(XPATH_PRODUCT_DESCRIPTION)
    product_description = ""
    for prod in raw_product_description:
        product_description += " " + (prod.strip())
    total_ratings = parser.xpath(XPATH_AGGREGATE_RATING)
    checkAvailability = ['Currently unavailable.', 'Currently unavailable', 'Out of stock', 'Out of stock.']

    availability = parser.xpath(XPATH_PRODUCT_AVAILABILITY)
    if (availability):
        availability = (availability)[0].strip().rstrip('.')
    if availability in checkAvailability:
        avail = 'false'
    else:
        avail = 'true'
    category = parser.xpath(XPATH_PRODUCT_CATEGORY)
    categories = ""
    flag = 0
    for cate in category:
        if(flag == 1):
            categories = categories + " > "+(cate).strip()
        else:
            categories = categories+ (cate).strip()
            flag =1
    if (category):
        category = (category)[0].strip()
    price = parser.xpath(XPATH_PRODUCT_LIST_PRICE)
    if(len(price)):
        list_price = price[0]
    else:
        list_price = None

    reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
    if not reviews:
        reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
    ratings_dict = {}
    details = []

    # grabing the rating  section in product page
    for ratings in total_ratings:
        extracted_rating = ratings.xpath('./td//a//text()')
        if extracted_rating:
            rating_key = extracted_rating[0]
            raw_raing_value = extracted_rating[1]
            rating_value = raw_raing_value
            if rating_key:
                ratings_dict.update({rating_key: rating_value})

    #getting url for all reviews
    next_page = parser.xpath(
        ".//div[@id='reviewsMedley']/div[@class='a-column a-span8']/div[@id='cr-medley-top-reviews-wrapper']/div[@id='reviews-medley-footer']/div[@class='a-row a-spacing-large']/a[@class='a-link-emphasis a-text-bold']/@href")
    count = parser.xpath(XPATH_REVIEW_COUNT)
    if len(count) > 0:
        count = count[0]
    else:
        count = 0
    if(len(next_page)>0):
        print("on first page", product_name, categories)
        details =  checkAndGetReviewAvailability(count,get_host(url)+next_page[0], settings.getheaders(), categories, product_name, product_image)


        # Parsing individual reviews

    data = {"business_units":[{"response": [{"business_item_data": {
            "business_type": "Product",
            "absolute_url": amazon_url,
            "category": categories,
            "name": product_name,
            "sub_category": "",
            "picture_urls": product_image,
            "original_price": product_price,
            "sale_price": list_price,
            "availability": bool(avail),
            "specifications": [],
            "website_name": get_host(url),
            "description": product_description
        },
            "reviews": details}],

        "scrapping_website_url": url,
        "scrapping_website_name":get_host(url) }]}

    return data
    #     except ValueError:
    #         print("Retrying to get the correct response")

    # return {"error":"failed to process the page","asin":asin}


def ReadAsin():
    # Add your own ASINs here
    AsinList = ['B01K6FEU1I']
    extracted_data = []
    for asin in AsinList:
        extracted_data.append(ParseReviews(asin))
        sleep(5)
    f = open('data.json', 'w')
    json.dump(extracted_data, f, indent=4)
def checkAndGetReviewAvailability(count,page_url, headers, categories, product_name, product_image):
    data = gettingIndividualReviews(page_url,headers,categories,product_name,product_image)
    if len(data) != int(count):
        log("review found length "+str(len(data)) + "  total count " + count)
        log("count not equal trying again")
        sleep(60)
        return checkAndGetReviewAvailability(count, page_url, headers, categories, product_name, product_image)
    return data

def gettingIndividualReviews(page_url, headers, categories, product_name, product_image):
    log("getting review for "+page_url)
    page = make_request(page_url, False)
    log("Request complete")
    page_response = page.text
    parser = html.fromstring(page_response)
    reviews_list = []
    next_page = parser.xpath(
        ".//div[@id='cm_cr-pagination_bar']/ul[@class='a-pagination']/li[@class='a-last']/a/@href")
    sleep(10)
    if len(next_page) > 0:
        reviews_list = gettingIndividualReviews(get_host(page_url) + next_page[0], headers, categories, product_name, product_image)

    XPATH_REVIEW_SECTION_1 = './/div[contains(@id,"reviews-summary")]'
    XPATH_REVIEW_SECTION_2 = './/div[@data-hook="review"]'
    reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
    if not reviews:
        reviews = parser.xpath(XPATH_REVIEW_SECTION_2)

    for review in reviews:
        XPATH_RATING = './/i[@data-hook="review-star-rating"]//text()'
        XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
        XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
        XPATH_REVIEW_TEXT_1 = './/span[@data-hook="review-body"]//text()'
        XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
        XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
        XPATH_AUTHOR = './/span[@data-hook="review-author"]/a//text()'
        XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'


        raw_review_author = review.xpath(XPATH_AUTHOR)
        raw_review_rating = review.xpath(XPATH_RATING)
        raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
        raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
        raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
        raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
        raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

        # cleaning data
        author = ' '.join(' '.join(raw_review_author).split())
        review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
        review_header = ' '.join(' '.join(raw_review_header).split())

        try:
            review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
        except:
            review_posted_date = None
        review_text = ' '.join(' '.join(raw_review_text1).split())

        # grabbing hidden comments if present
        if raw_review_text2:
            json_loaded_review_data = json.loads(raw_review_text2[0])
            json_loaded_review_data_text = json_loaded_review_data['rest']
            cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
            full_review_text = review_text + cleaned_json_loaded_review_data_text
        else:
            full_review_text = review_text
        if not raw_review_text1:
            full_review_text = ' '.join(' '.join(raw_review_text3).split())

        raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
        review_comments = ''.join(raw_review_comments)
        review_comments = re.sub('[A-Za-z]', '', review_comments).strip()
        review_dict = {
            # review_comment_count':review_comments,
            "absolute_url": page_url,
            "rating": utils.getStarts(review_rating),
            "review_title": review_header,
            "reviewed_at": utils.convertDate(review_posted_date),
            "reviewer_name": author,
            "category": categories,

            "review_text": full_review_text,
            "picture_urls": product_image,
            "website_name": get_host(page_url)

        }
        reviews_list.append(review_dict)
    return reviews_list


if __name__ == '__main__':
    ReadAsin()