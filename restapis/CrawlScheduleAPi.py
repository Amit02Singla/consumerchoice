# For a quick start check out our HTTP Requests collection (Tools|HTTP Client|Open HTTP Requests Collection).
#
# Following HTTP Request Live Templates are available:
# * 'gtrp' and 'gtr' create a GET request with or without query parameters;
# * 'ptr' and 'ptrp' create a POST request with a simple or parameter-like body;
# * 'mptr' and 'fptr' create a POST request to submit a form with a text or file field (multipart/form-data);
import json
import threading
from functools import wraps

from flask import Flask, request, jsonify
from flask import Response

from restapis.Login import MyThread
from utils.GoogleSearch import dataforSEO
from utils.GoogleSearch import search

app = Flask(__name__)

def check_auth(auth):
    return auth == 'bearer crawl token'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers.keys():
            auth = request.headers['Authorization']
            if not auth:
                return authenticate()

            elif not check_auth(auth):
                return authenticate()
            return f(*args, **kwargs)
        else:
            return authenticate()

    return decorated

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.headers['Content-Type'] == 'application/json':
        data = {
            'hello': 'world',
            'number': 3
        }
        js = json.dumps(data)

        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://luisrei.com'

        return resp
        return jsonify(request.json['message'])


@app.route('/business_items/scrape', methods=['GET'])
@requires_auth
def crawlSite():
    id = request.args.get("id")
    categoryName = request.args.get("category_name")
    url = request.args.get("scrapping_website_url")
    callback_url = request.args.get("callback_url")
    thread = MyThread(id,categoryName,url,callback_url)
    thread.start()
    resp = "Schedule Success"
    return resp



@app.route('/categories/search_websites', methods=['POST'])
@requires_auth
def googleSearch():
    jsn = jsonify(request.data)
    print("request from ror for 2nd step " , jsn )
    print("   callbackurl  ", jsn.callback_url)
    print("   urls  ",jsn.website_urls )
    websiteUrls = jsn.website_urls
    callback_url = jsn.callback_url
    t1 = threading.Thread(target=search, args=(websiteUrls, callback_url))
    t1.start()
    response = "Searching Scheduled"
    return response


@app.route('/categories/search_services', methods=['GET'])
@requires_auth
def getDataSEO():
    id = request.args.get('id')
    categoryName =request.args.get('name')
    categoryKeywords = request.args.getlist('keywords')
    callback_url = request.args.get('callback_url')
    print(categoryKeywords , categoryName, callback_url , id)
    t1 = threading.Thread(target=dataforSEO,args=(id,categoryName,categoryKeywords,callback_url))
    t1.start()
    response ="Searching Scheduled"
    return response


@app.route('/categories/search_websites', methods=['POST'])
def searchGoogle1():
    print(request.data)
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0',port="5001")
