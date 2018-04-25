import requests
import json
import services.ServiceController
param = {
  "email": "data_miner@example.com",
  "password": "ATBdm9",
  "grant_type": "password"
}
url = ""
SUCCESS_STATUS = 200
base_url ="http://52.0.49.246/api/v1/"
def login():
  response = requests.post( base_url+"users/login", param)
  data = response.json()
  return data

def postReview(review):
  data =login()
  header = {'Content-Type':'application/json','Authorization':'bearer '+data['data']['token']['access_token']}
  r = requests.post(base_url+"data_miner/store_data",data=json.dumps(review),headers=header)

def getUrl():
  data = login()
  header = {'Authorization': 'bearer ' + data['data']['token']['access_token']}
  response_website = requests.get(base_url + "scrapping_websites", headers=header)
  website_data = response_website.json()
  website_list = []
  for element in (website_data['data']['scrapping_websites']):
    website_list.append({"ServiceName": "Bluehost",
                 "Category": "Hosting Service",
                 "url": element['url']})
  services.ServiceController.crawl_services(website_list)
