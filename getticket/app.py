from dotenv import load_dotenv
import os, requests, json, time, decimal
from flask import Flask
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
            "time": dt.timestamp()
        }
    else:
        data = temp_data

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)
    return data['tokenset']['token']
    # catch (exception):
    #     return data.json()


@app.post("/getBizInfo")
def getBizInfo(request):
    url = "https://api.moneypin.biz/bizno/v1/biz/info/base"

    payload = json.dumps({
        "bizNoList": [
            "2152195730"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4NjQ2OTkzMTQwMDQ2NTksImNpZCI6IjM3MmExZDBiLTk5YzItNDVmNC05MTRjLWE1YWQ1MDQ1YmJmYiIsInBsbiI6InRlc3QiLCJpYXQiOjE3MDQ0NDEzNDMsImV4cCI6MTcwNDQ0ODU0MywiaXNzIjoibW9uZXlwaW46Yml6bm8ifQ.uilt5hEookHurqQP7h-23A0aIDyaDTGK4qiAGApW3xQ'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


if __name__ == '__main__':
    app.run()
