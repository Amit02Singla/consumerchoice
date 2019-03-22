import json

from scrapy import Spider
import restapis.Login
from model.Response import Response


class BaseSiteURLCrawler(Spider):

    def __init__(self):
        self.dict_url = {}
        self.final_json = {}
        self.category = ""
        self.service_name = ""
        pass
    def createCategory(self,link):
        self.category = link["Category"];
        self.service_name = link["ServiceName"]
        self.dict_url[link["url"]] = {"Category": self.category,
                                 "Service Name": self.service_name}
        response = Response("Service");
        response.Service_Name = self.service_name
        response.Category = self.category
        response.URL = link["url"]
        self.final_json[self.service_name] = {"response": response}
    def save(self,serviceRecord):
        response = self.final_json[self.service_name]["response"]
        response.addRecord(serviceRecord);
    def pushToServer(self):
        str1 = ""
        dictionary = {}
        buisness_units = []
        for k, v in self.final_json.items():
            responselist = []
            responselist.append(v["response"].dump())
            dictionary[k] = {"scrapping_website_name": v["response"].serviceRecord[0].name, "scrapping_website_url": v["response"].URL,
                             "response": responselist}
            buisness_units.append(dictionary[k])
            path =v["response"].URL.replace("http:","").replace('https:','').replace("/","").replace(".","_").replace("?","").replace("=","")+".json"
            restapis.Login.postReview({"business_units": buisness_units})
        with open(path,'w') as f:
            json.dump({"business_units":buisness_units},f)


