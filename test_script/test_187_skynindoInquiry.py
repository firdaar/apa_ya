import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/skynindoInquiry" % (IP_PORT)

#cek user login
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
 #akan post/kirim data login 
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
    "reffNum": "202003030950250100190",
	  "customerId": "1011011234567811",
	  "packageCode": "101",
	  "providerId": "SKYNINDO",
	  "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
	  "ip_address": "10.70.9.89",
	  "id_api": "web",
	  "ip_server": "68",
	  "req_id": "1561617885314116",
    "session": "%s"
  }""" % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('reffNum') != None
  assert resp.get('providerId') != None
  assert resp.get('customerId') != None
  assert resp.get('packageCode') != None
  assert resp.get('customerName') != None
  assert resp.get('penalty') != None
  assert resp.get('biaya_loket') != None
  assert resp.get('biaya_adm') != None
  assert resp.get('billReffNo') != None
  assert resp.get('billReffNo2') != None
  assert resp.get('amount') != None
  assert resp.get('loket_totalAmount') != None
 
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
    "reffNum": "20190627134445000005",
	  "customerId": "4567811113330",
	  "packageCode": "101",
	  "providerId": "SKYNINDO",
	  "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
	  "ip_address": "10.70.9.89",
	  "id_api": "web",
	  "ip_server": "68",
	  "req_id": "1561617885314116",
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
   "reffNum": "202003030950250100190",
  	"customerId": "1011011234567811",
  	"packageCode": "101",
  	"providerId": "SKYNINDO",
  	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
  	"ip_address": "10.70.9.89",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1561617885314116"
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
    "reffNum": "202003030950250100190",
  	"customerId": "1011011234567811",
  	"packageCode": "101",
  	"providerId": "SKYNINDO",
  	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
  	"ip_address": "10.70.9.89",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1561617885314116",
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
    "reffNum": "202003030950250100190",
  	"customerId": "1011011234567811",
  	"packageCode": "101",
  	"providerId": "SKYNINDO"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket')!=None
  assert resp.get('reffNum') != None
  assert resp.get('providerId') != None
  assert resp.get('customerId') != None
  assert resp.get('packageCode') != None
  assert resp.get('customerName') != None
  assert resp.get('penalty') != None
  assert resp.get('biaya_loket') != None
  assert resp.get('biaya_adm') != None
  assert resp.get('billReffNo') != None
  assert resp.get('billReffNo2') != None
  assert resp.get('amount') != None
  assert resp.get('loket_totalAmount') != None
