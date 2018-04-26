import threading

import os
import requests
import json
from services.ServiceController import crawl_services
param = {
  "email": "data_miner@example.com",
  "password": "ATBdm9",
  "grant_type": "password"
}
url = ""
SUCCESS_STATUS = 200
base_url ="http://52.0.49.246/api/v1/"
custom_base_url = ""

def login():
  response = requests.post( base_url+"users/login", param)
  print(response)
  data = response.json()
  return data

def postReview(review):

  if(custom_base_url == ""):
    data =login()
    header = {'Content-Type': 'application/json', 'Authorization': 'bearer ' + data['data']['token']['access_token']}
    requests.post(base_url + "data_miner/store_data", data=json.dumps(review), headers=header)
  else:
    requests.post(custom_base_url + "data_miner/store_data", data=json.dumps(review))

def crawling():
  data = login()
  header = {'Authorization': 'bearer ' + data['data']['token']['access_token']}
  response_website = requests.get(base_url + "scrapping_websites", headers=header)
  website_data = response_website.json()
  website_list = []
  for element in (website_data['data']['scrapping_websites']):
    website_list.append({"ServiceName": "Bluehost",
                         "Category": "Hosting Service",
                         "url": element['url']})

    print("crawl_services called")
  crawl_services(website_list)
def crawlURL(url,responseURL):
  website_list = []
  website_list.append({"ServiceName": "Bluehost",
                       "Category": "Hosting Service",
                       "url": url})
  global custom_base_url
  custom_base_url = responseURL
  crawl_services(website_list)
class MyThread(threading.Thread):
  def __init__(self, url,responseURL):
    super(MyThread, self).__init__()
    self.responseURL = responseURL
    self.URL = url
  def run(self):
    print("Mythread start")
    if(self.URL == ""):
      crawling()
    else:
      crawlURL(self.URL,self.responseURL)

