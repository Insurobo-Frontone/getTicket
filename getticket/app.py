from dotenv import load_dotenv
import os, requests, json, time, decimal
from flask import Flask, request, make_response
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin

app = Flask(__name__)

#app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()
CORS(app)
cors = CORS(app, resources={
    r"/getTicket/*": {"origin": "*"},
    r"/getBizInfo/*": {"origin": "*"},
    r"/getBizInfoOnce/*": {"origin": "*"},
})

@app.route("/apiticket")
@cross_origin()
def helloWorld2():
    return "Hello, cross-origin-world!2"

@app.route("/")
@cross_origin()
def helloWorld():
    return "Hello, cross-origin-world!"


@app.route("/apiticket/getTicket", methods=['POST'])
def getTicket():
    data = {}
    file_path = "./ticket.json"

    # try:
    with open(file_path, 'r+') as file:
        temp_data = json.load(file)

    now = time.time()
    dt = datetime.fromtimestamp(now)
    oldtime = temp_data['time']

    newtime = dt.timestamp()

    olddatetimeobj = datetime.fromtimestamp(oldtime) + timedelta(hours=1)
    newdatetimeobj = datetime.fromtimestamp(newtime)

    # print('Debug : '+olddatetimeobj.timestamp)
    # print('Debug : '+newdatetimeobj.timestamp)

    if (newdatetimeobj > olddatetimeobj):
        clientId = os.environ.get('clientId')
        clientSecret = os.environ.get('clientSecret')
        url = "https://api.moneypin.biz/bizno/v1/auth/token"

        payload = json.dumps({
            "grantType": "ClientCredentials",
            "clientId": clientId,
            "clientSecret": clientSecret
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        data = {
            "tokenset": response.json(),
            "time": newtime
        }
        print('Debug: key to Store')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)
    else:
        data = temp_data
        print('Debug: Stored key')

    res = {
        "token": data['tokenset']['token']
    }

    return json.dumps(res)

@app.route("/apiticket/getBizInfo", methods=['POST'])
def getBizInfo():
    content_type = request.headers.get('Content-Type')
    accept = request.headers.get('accept')
    authorization = request.headers.get('Authorization')

    url = "https://api.moneypin.biz/bizno/v1/biz/info/base"

    payload = json.dumps(request.json)
    headers = {
        'Content-Type': content_type,
        'Accept': accept,
        'Authorization': authorization
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    response.status="200"
    return response

@app.route("/apiticket/getBizInfoOnce", methods=['POST', "OPTIONS"])
def getBizInfoOnce():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST": # The actual request following the preflight
        data = {}
        file_path = "./ticket.json"

        # try:
        with open(file_path, 'r+') as file:
            temp_data = json.load(file)

        now = time.time()
        dt = datetime.fromtimestamp(now)
        oldtime = temp_data['time']

        newtime = dt.timestamp()

        olddatetimeobj = datetime.fromtimestamp(oldtime) + timedelta(hours=1)
        newdatetimeobj = datetime.fromtimestamp(newtime)

        # print('Debug : '+olddatetimeobj.timestamp)
        # print('Debug : '+newdatetimeobj.timestamp)

        if (newdatetimeobj > olddatetimeobj):
            clientId = os.environ.get('clientId')
            clientSecret = os.environ.get('clientSecret')
            url = "https://api.moneypin.biz/bizno/v1/auth/token"

            payload = json.dumps({
                "grantType": "ClientCredentials",
                "clientId": clientId,
                "clientSecret": clientSecret
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            data = {
                "tokenset": response.json(),
                "time": newtime
            }
            print('Debug: key to Store')
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file)
        else:
            data = temp_data
            print('Debug: Stored key')

        res = {
            "token": data['tokenset']['token']
        }

        token = res['token']

        content_type = request.headers.get('Content-Type')
        accept = request.headers.get('accept')
        authorization = "Bearer " + token

        url = "https://api.moneypin.biz/bizno/v1/biz/info/base"

        payload = json.dumps(request.json)
        headers = {
            'Content-Type': content_type,
            'Accept': accept,
            'Authorization': authorization,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        list = response.json()

        return json.dumps(list)

@app.after_request
def apply_caching(response):
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')
