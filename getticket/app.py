from dotenv import load_dotenv
import os, requests, json, time, decimal
from flask import Flask, request
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv()
#CORS(app)
cors = CORS(app, resources={
    r"/getTicket/*": {"origin": "*"},
    r"/getBizInfo/*": {"origin": "*"},
    r"/getBizInfoOnce/*": {"origin": "*"},
})


@app.route("/")
@cross_origin()
def helloWorld():
    return "Hello, cross-origin-world!"


@app.route("/getTicket", methods=['POST'])
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


@app.route("/getBizInfo", methods=['POST'])
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


@app.route("/getBizInfoOnce", methods=['POST'])
def getBizInfoOnce():
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
    authorization = "Bearer "+token

    url = "https://api.moneypin.biz/bizno/v1/biz/info/base"

    payload = json.dumps(request.json)
    headers = {
        'Content-Type': content_type,
        'Accept': accept,
        'Authorization': authorization
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == '__main__':
    import sys
    print(sys.path)
    app.run()
