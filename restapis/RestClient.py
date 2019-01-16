from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
import time
from threading import Thread


class RestClient():
    domain = "api.dataforseo.com"

    def __init__(self):
        self.username = "jp@hipnode.com"
        self.password = "fVgDzN3CIVEyg3p9"

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        print("in request")
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        print("in get");
        return self.request(path, 'GET')

    def post(self, path, data):
        print("in post");
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)


if __name__ == '__main__':
    my = RestClient();
    # you can set as "index of post_data" your ID, string, etc. we will return it with all results.
    post_data = dict()
    post_data[23] = dict(
        priority=1,
        se_name="google.com",
        se_language="English",
        loc_name_canonical="India",
        key="HomeLight"
    )
    post_data[24] = dict(
        priority=1,
        se_name="google.com",
        se_language="English",
        loc_name_canonical="India",
        key="norton"
    )

    response = my.post("/v2/srp_tasks_post", dict(data=post_data))
    if response["status"] == "error":
        print("error. Code: %d Message: %s" % (response["error"]["code"], response["error"]["message"]))
    else:
        print(response["results"])
    print("before sleep")
    time.sleep(90);
    print(" after sleep")
    data = []
    completed_tasks_response = my.get("/v2/srp_tasks_get")

    if completed_tasks_response["status"] == "error":
        print("error. Code: %d Message: %s" % (
        completed_tasks_response["error"]["code"], completed_tasks_response["error"]["message"]))
    else:
        results = completed_tasks_response["results"]
        print(results)
        for result in results:
            srp_response = my.get("/v2/srp_tasks_get/%d" % (result["task_id"]))
            if srp_response["status"] == "error":
                print("error. Code: %d Message: %s" % (srp_response["error"]["code"], srp_response["error"]["message"]))
            else:
                dict = srp_response["results"]
                for urlList in dict["organic"]:
                    data.append(urlList["result_url"]);
                print(dict)
                print("data ", len(data), data)

