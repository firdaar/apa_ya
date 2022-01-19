import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/IBSInquiry" % (IP_PORT)

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
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "202001061326540100189",
	"billingId": "2019080113540183",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1578292014292005",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('reffNum') != None
  assert resp.get('h_billingId') != None
  assert resp.get('h_billingName') != None
  assert resp.get('h_channelId') != None
  assert resp.get('h_billAmount') != None
  assert resp.get('h_billInfo6') != None
  assert resp.get('h_billInfo71') != None
  assert resp.get('h_billInfo72') != None
  assert resp.get('h_billInfo73') != None
  assert resp.get('h_billInfo74') != None
  assert resp.get('h_billInfo75') != None
  assert resp.get('h_billInfo76') != None
  assert resp.get('h_billInfo77') != None
  assert resp.get('h_billInfo78') != None
  assert resp.get('h_billInfo79') != None
  assert resp.get('h_billInfo710') != None
  assert resp.get('c_fee') != None
  assert resp.get('loket_totalBayar') != None
  

  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "20200106100189",
	"billingId": "20190801140183",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1578292014292005",
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
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "202001061326540100189",
	"billingId": "2019080113540183",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1578292014292005"
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
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "202001061326540100189",
	"billingId": "2019080113540183",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1578292014292005",
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
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "202001061326540100189",
	"billingId": "2019080113540183"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('reffNum') != None
  assert resp.get('h_billingId') != None
  assert resp.get('h_billingName') != None
  assert resp.get('h_channelId') != None
  assert resp.get('h_billAmount') != None
  assert resp.get('h_billInfo6') != None
  assert resp.get('h_billInfo71') != None
  assert resp.get('h_billInfo72') != None
  assert resp.get('h_billInfo73') != None
  assert resp.get('h_billInfo74') != None
  assert resp.get('h_billInfo75') != None
  assert resp.get('h_billInfo76') != None
  assert resp.get('h_billInfo77') != None
  assert resp.get('h_billInfo78') != None
  assert resp.get('h_billInfo79') != None
  assert resp.get('h_billInfo710') != None
  assert resp.get('c_fee') != None
  assert resp.get('loket_totalBayar') != None
  