from dotenv import load_dotenv
import os, requests, json, time, decimal
from flask import Flask, request
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv()
cors = CORS(app, resources={
    r"/getTicket/*": {"origin": "*"},
    r"/getBizInfo/*": {"origin": "*"},
})


@app.route("/")
@cross_origin()
def helloWorld():
    return "Hello, cross-origin-world!"


@app.post("/getTicket")
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


@app.post("/getBizInfo")
def getBizInfo():
    content_Type = request.headers.get('Content-Type')
    accept = request.headers.get('accept')
    authorization = request.headers.get('Authorization')

    url = "https://api.moneypin.biz/bizno/v1/biz/info/base"

    payload = json.dumps(request.json)
    headers = {
        'Content-Type': content_Type,
        'Accept': accept,
        'Authorization': authorization
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


if __name__ == '__main__':
    app.run()
