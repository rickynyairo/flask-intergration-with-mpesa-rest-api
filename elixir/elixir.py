from flask import Flask, render_template, url_for, request, jsonify#, current_app as app
from wsgiref import headers
from flask_login import login_required, current_user
import os
import psycopg2
import requests
import base64
from flask_sqlalchemy import SQLAlchemy
from requests.auth import HTTPBasicAuth
#import table classes:
from models import *

app = Flask(__name__)#, instance_relative_config=True)
app.config.from_object('config')
#app = Flask(__name__)#, instance_relative_config=True)
db = SQLAlchemy(app)

def get_access_token(object):
    consumer_key = 'ijrrNb44sv7JW8UtPaspuNDOMEmhtEM2'
    consumer_secret = 'sIcDdkuGPXd9HcAy'
    encoded_auth = base64.b64encode(bytes(consumer_key, 'utf-8') + b":" + bytes(consumer_secret, 'utf-8'))
    encoded_auth = str(encoded_auth)[2:-1] #to remove the b and the colons
    authorization_txt = "Basic %s" % encoded_auth
	#"Basic aWpyck5iNDRzdjdKVzhVdFBhc3B1TkRPTUVtaHRFTTI6c0ljRGRrdUdQWGQ5SGNBeQ==",
    auth_api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    headers = {
	    "Authorization": authorization_txt,
	    "content-type":"application/json"
	    }
    auth_req = requests.get(auth_api_url, auth = HTTPBasicAuth(consumer_key, consumer_secret), headers = headers).json()
    access_token = auth_req['access_token']

    return access_token

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
#@login_required
def account():
    return render_template("index.html")

@app.route('/api/mpesa-api/c2bvalidation', methods=['GET', 'POST'])
def validate_transaction():
    request_data = request.json
    this_transaction = transactions(str(request_data['TransID']), int(request_data['MSISDN']), int(request_data['TransAmount'][:-3]), str(request_data['BillRefNumber']))
    #db.session.add(this_transaction)
    #db.session.commit()
    header = {
		"Content-Type":"application/json"
		}
    response = {
        "ResultCode": 0,
        "ResultDesc": "The service was accepted Successfully",
        "ThirdPartyTransID": "1234567890"
    }
    return jsonify(response), 200

@app.route('/api/mpesa-api/c2bconfirmation', methods=['GET','POST'])
def confirm_transaction():
    request_data = request.json
    this_transaction = c2b_transactions(str(request_data['TransID']), int(request_data['MSISDN']), int(request_data['TransAmount'][:-3]), str(request_data['BillRefNumber']))
    db.session.add(this_transaction)
    db.session.commit()
    header = {
		"Content-Type":"application/json"
		}
    response = {
        "ResultCode": 0,
        "ResultDesc": "The service was accepted Successfully",
        "ThirdPartyTransID": "1234567890"
    }
    return jsonify(response), 200

@app.route('/api/mpesa-api/c2b-test-run')
def c2b_test_run():
    #register urls for the process
    reg_url_resp = register_url_func()
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    headers = {
		"Authorization": "Bearer %s" % access_token,
		"Content-Type":"application/json"
		}
    payload = {
        "ShortCode":"600503",
        "CommandID":"CustomerPayBillOnline",
        "Amount": "47520",
        "Msisdn": "254708374149",
        "BillRefNumber": "Raila"
    }
    #simulate transaction
    test_text = requests.post(api_url, json=payload, headers=headers)
    return test_text.text


def register_url_func():
    #uses API to register confirmation and validation url
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    headers = {
		"Authorization": "Bearer %s" % access_token,
		"Content-Type":"application/json"
		}
    payload = {
        "ShortCode": "600503" ,
        "ResponseType": "Completed",
        "ConfirmationURL": "http://flask-trial-2.herokuapp.com/api/mpesa-api/c2bconfirmation",
        "ValidationURL": "http://flask-trial-2.herokuapp.com/api/mpesa-api/c2bvalidation"
    }
    register_url_req = requests.post(api_url, json=payload, headers=headers)
    return register_url_req.text


if __name__ == '__main__':
	app.run(port = 33507)
