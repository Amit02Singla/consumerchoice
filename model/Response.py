import json
class Response():
    def __init__(self,buisnessType):
        self.Service_Name = ""
        self.URL = ""
        self.Category = ""
        self.Sub_Category = ""
        self.Image = []
        self.serviceRecord = []
        self.buisnessType = buisnessType
        self.original_price =  ""
        self.sale_price = ""
        self.availability = ""
        self.specifications = []
        self.description = ""

    @property
    def Service_Name(self):
        return self._Service_Name

    @Service_Name.setter
    def Service_Name(self, value):
        self._Service_Name = value
    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, value):
        self._URL = value
    @property
    def Category(self):
        return self._Category

    @Category.setter
    def Category(self, value):
        self._Category = value

    @property
    def Sub_Category(self):
        return self._Sub_Category

    @Sub_Category.setter
    def Sub_Category(self, value):
        self._Sub_Category = value

    @property
    def Image(self):
        return self._Image

    @Image.setter
    def Image(self, value):
        self._Image = value

    @property
    def buisnessType(self):
        return self._buisnessType

    @buisnessType.setter
    def buisnessType(self, value):
        self._buisnessType = value

    @property
    def original_price(self):
        return self._original_price

    @buisnessType.setter
    def original_price(self, value):
        self._original_price = value

    @property
    def specifications(self):
        return self._specifications

    @buisnessType.setter
    def specifications(self, value):
        self._specifications = value

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, value):
        self._availability = value

    @property
    def sale_price(self):
        return self._sale_price

    @sale_price.setter
    def sale_price(self, value):
        self._sale_price = value

    @property
    def description(self):
        return self._description

    @sale_price.setter
    def description(self, value):
        self._description = value

    def addRecord(self,serviceRecordd):
        self.serviceRecord.append(serviceRecordd)

    def dump(self):
        store_data_dict = {}
        string1 = []
        website_name = ""
        for item in self.serviceRecord:
            string1.append(item.str11())
            website_name = item.website_name
            #str(item)
        return {"business_item_data": {
            "business_type":self.buisnessType,
            "absolute_url": self.URL,
            "category": string1[0]["category"] if len(string1)>0 else self.Category,
            "name": self.Service_Name,
            "sub_category": self.Sub_Category,
            "picture_urls": self.Image,
            "original_price": self.original_price,
            "sale_price": self.sale_price,
            "availability": self.availability,
            "specifications": self.specifications,
            "website_name": self.Service_Name,
            "description": self.description
        },
            "reviews": string1

        }




        #Sreturn json.dumps(store_data_dict).replace("/", "\\/")




