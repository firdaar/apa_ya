import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/topUpUangElektronikInquiry" % (IP_PORT)

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
	"providerId": "DANA",
	"billingNumber": "081231988251",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"ip_address": "10.70.9.44",
    "id_api": "web",
	"ip_server": "68",
	"req_id": "1595409493782703",
	"session": "%s"
  }
  """ %(session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('billingLabel') != None
  assert resp.get('billingNumber') != None
  assert resp.get('trxId') != None
  assert resp.get('virtualAccountNumber') != None
  assert resp.get('virtualAccountName') != None
  assert resp.get('vaNameLabel') != None
  assert resp.get('virtualAccountTrxType') != None
  assert resp.get('billedAmount') != None
  assert resp.get('billedAmountLabel') != None
  assert resp.get('billedAmountValue') != None
  assert resp.get('clientId') != None
  assert resp.get('feeAmount') != None
  assert resp.get('feeAmountLabel') != None
  assert resp.get('feeAmountValue') != None
  assert resp.get('currency') != None
  assert resp.get('additionalLabel1') != None
  assert resp.get('additionalLabel2') != None
  assert resp.get('additionalLabel3') != None
  assert resp.get('additionalValue1') != None
  assert resp.get('additionalValue2') != None
  assert resp.get('additionalValue3') != None
  assert resp.get('additional') != None
  assert resp.get('biaya_loket') != None

### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
	"providerId": "DANA",
	"billingNumber": "081231981",
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
	"providerId": "DANA",
	"billingNumber": "081231988251",
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
	"providerId": "DANA",
	"billingNumber": "081231988251",
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
	"providerId": "DANA",
	"billingNumber": "081231988251"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('billingLabel') != None
  assert resp.get('billingNumber') != None
  assert resp.get('trxId') != None
  assert resp.get('virtualAccountNumber') != None
  assert resp.get('virtualAccountName') != None
  assert resp.get('vaNameLabel') != None
  assert resp.get('virtualAccountTrxType') != None
  assert resp.get('billedAmount') != None
  assert resp.get('billedAmountLabel') != None
  assert resp.get('billedAmountValue') != None
  assert resp.get('clientId') != None
  assert resp.get('feeAmount') != None
  assert resp.get('feeAmountLabel') != None
  assert resp.get('feeAmountValue') != None
  assert resp.get('currency') != None
  assert resp.get('additionalLabel1') != None
  assert resp.get('additionalLabel2') != None
  assert resp.get('additionalLabel3') != None
  assert resp.get('additionalValue1') != None
  assert resp.get('additionalValue2') != None
  assert resp.get('additionalValue3') != None
  assert resp.get('additional') != None
  assert resp.get('biaya_loket') != None