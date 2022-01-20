import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/LPG3KGInquiry" % (IP_PORT)

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

reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
### TC Normal ###
#################
def test_normal():
  session = login_user("agen")
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"retailerId": "120351810736027",
	"agentLPGId": "810736",
	"requestQuantity": "13",
	"deliveryDate": "20200122",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1579683624337902",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('reffNum') != None
  assert resp.get('retailerId') != None
  assert resp.get('agentLPGId') != None
  assert resp.get('agentLPGName') != None
  assert resp.get('availableQuantity') != None
  assert resp.get('price') != None
  assert resp.get('deliveryDate') != None
  assert resp.get('requestQuantity') != None
  assert resp.get('amount') != None
  assert resp.get('fee') != None
  assert resp.get('biaya_loket') != None
  assert resp.get('loket_totalBayar') != None
  

  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"retailerId": "1203518107367",
	"agentLPGId": "8136",
	"requestQuantity": "13",
	"deliveryDate": "20200122",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1579683624337902",
    "session": "%s"
  }
  """ % (reffNum,session)
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
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"retailerId": "120351810736027",
	"agentLPGId": "810736",
	"requestQuantity": "13",
	"deliveryDate": "20200122",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1579683624337902"
  }
  """%(reffNum)
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
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"retailerId": "120351810736027",
	"agentLPGId": "810736",
	"requestQuantity": "13",
	"deliveryDate": "20200122",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1579683624337902",
    "session": "%s"
  }
  """ % (reffNum,session)
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
  	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"retailerId": "120351810736027",
	"agentLPGId": "810736",
	"requestQuantity": "13",
	"deliveryDate": "20200122"
  }
  """%(reffNum)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('reffNum') != None
  assert resp.get('retailerId') != None
  assert resp.get('agentLPGId') != None
  assert resp.get('agentLPGName') != None
  assert resp.get('availableQuantity') != None
  assert resp.get('price') != None
  assert resp.get('deliveryDate') != None
  assert resp.get('requestQuantity') != None
  assert resp.get('amount') != None
  assert resp.get('fee') != None
  assert resp.get('biaya_loket') != None
  assert resp.get('loket_totalBayar') != None