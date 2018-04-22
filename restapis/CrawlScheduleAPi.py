# For a quick start check out our HTTP Requests collection (Tools|HTTP Client|Open HTTP Requests Collection).
#
# Following HTTP Request Live Templates are available:
# * 'gtrp' and 'gtr' create a GET request with or without query parameters;
# * 'ptr' and 'ptrp' create a POST request with a simple or parameter-like body;
# * 'mptr' and 'fptr' create a POST request to submit a form with a text or file field (multipart/form-data);

from flask import Flask, Response
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from restapis.Login import getUrl
import json
from functools import wraps


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
        auth = request.headers['Authorization']
        if not auth:
            return authenticate()

        elif not check_auth(auth):
            return authenticate()
        return f(*args, **kwargs)

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

@app.route('/schedule', methods=['POST'])
@requires_auth
def do_schedule():
    if request.headers['Content-Type'] == 'application/json':
        requests =  jsonify(request.json)
        time = request['Time']
        crontime = request['Crontime']
        resp = Response(status="ok", message=cronjob(time, crontime) , code = 200, mimetype='application/json')


@app.route('/schedule', methods=['GET'])
@requires_auth
def crawl():
    getUrl()
    resp = Response(status="ok", message="Crawling Scheduled" , code = 200, mimetype='application/json')
    return resp
if __name__ == "__main__":
    app.run()