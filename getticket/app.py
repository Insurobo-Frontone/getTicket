from dotenv import load_dotenv
import os 
import requests
import json
from flask import Flask

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.post("/getTicket")
def getTicket():
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
    return response.text

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
    return response.text