import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

#IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
IP_PORT = os.getenv("IP_PORT", "192.168.250.130:8080")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/umptkinInquiry" % (IP_PORT)

def login_user(a):
  if a == "agen":
    username = "BNIAG50299"
    password = "Ipybni06!"
  elif a == "agan":
    username = "BMSSA"
    password = "Ipybni06!"
  elif a == "bni":
    username = "37370"
    password = "bni1234"

  post_login = """{
    "username": "%s",
    "password": "%s",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595218050176506"
  }
  """ % (username, password)
  req = requests.post("http://%s/auth" % (IP_PORT), json=json.loads(post_login))
  resp = req.json()
  session = resp.get('session')
  assert resp.get('code') == '1'
  logging.debug('login as: ' + a)
  logging.debug('session: ' + session)
  return session

### TC Normal ###
#################
def test_normal():
  session = login_user("agen")
  post_data = """{
    "billerCode": "0026",
	"univCode": "3001",
	"billingNumber": "1234567890",
	"flexiField": "1",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('billerCode') != None
  assert resp.get('univCode') != None
  assert resp.get('billingNumber') != None
  assert resp.get('flexiField') != None
  assert resp.get('univName') != None
  assert resp.get('isRegistration') != None
  assert resp.get('studentId') != None
  assert resp.get('studentName') != None
  assert resp.get('phoneNumber') != None
  assert resp.get('numberOfBills') != None
  assert resp.get('billInfo') != None
  assert resp.get('billAmount') != None
  assert resp.get('billCode') != None
  assert resp.get('totalAmount') != None
  assert resp.get('narration') != None
  assert resp.get('transactionId') != None
  assert resp.get('paymentStatus') != None
  assert resp.get('hostTransactionId') != None
  assert resp.get('fee') != None
  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
    "billerCode": "0026",
	"univCode": "30011",
	"billingNumber": "1234567890",
	"flexiField": "1",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') != None
  assert resp.get('message') != None

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
    "billerCode": "0026",
	"univCode": "3001",
	"billingNumber": "1234567890",
	"flexiField": "1",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('code') == '66'
  assert resp.get('reason') == 'Session tidak ditemukan'
   
### TC Abnormal - Session Invalid ###
#####################################
def test_abnormal_session_invalid():
  session = "12345"
  post_data = """{
    "billerCode": "0026",
	"univCode": "3001",
	"billingNumber": "1234567890",
	"flexiField": "1",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('code') == '66'
  assert resp.get('reason') == 'Session invalid'
  
### TC Bypass Session ###
#########################
def test_bypass_session():
  post_data = """{
    "billerCode": "0026",
	"univCode": "3001",
	"billingNumber": "1234567890",
	"flexiField": "1"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('billerCode') != None
  assert resp.get('univCode') != None
  assert resp.get('billingNumber') != None
  assert resp.get('flexiField') != None
  assert resp.get('univName') != None
  assert resp.get('isRegistration') != None
  assert resp.get('studentId') != None
  assert resp.get('studentName') != None
  assert resp.get('phoneNumber') != None
  assert resp.get('numberOfBills') != None
  assert resp.get('billInfo') != None
  assert resp.get('billAmount') != None
  assert resp.get('billCode') != None
  assert resp.get('totalAmount') != None
  assert resp.get('narration') != None
  assert resp.get('transactionId') != None
  assert resp.get('paymentStatus') != None
  assert resp.get('hostTransactionId') != None
  assert resp.get('fee') != None
  