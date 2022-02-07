from tkinter.messagebox import NO
import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/lpgDeleteHarga" % (IP_PORT)

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
	"pin_transaksi": "12345",
	"retailer_name": "Mitsuha",
	"price": "1500",
	"effective_date": "25-10-2018",
	"retailer_phone": "08819092007",
	"retailer_email": "mitsuha@gmail.com",
	"price_id": "107",
	"retailer_id": "000007",
	"channel_id": "AGEN46",
	"agent_id": "810736",
	"staff_id": "BNIAG50299",
	"username": "BNIAG50299",
  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	"ip_address": "10.70.9.176",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1620354236891904",
  "session": "%s"
  }
  """%(session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('error')==False
  assert resp.get('code')=="00"
  assert resp.get('message')=="Harga berhasil dihapus."
  assert resp.get('data') != None
  assert resp.get('data').get('retailer_id') != None
  assert resp.get('data').get('retailer_name') != None
  assert resp.get('data').get('price') != None
  assert resp.get('data').get('price_id') != None
  assert resp.get('data').get('effective_date') != None
  assert resp.get('data').get('retailer_phone') != None
  assert resp.get('data').get('retailer_email') != None
  assert resp.get('data').get('pin_transaksi') != None
  assert resp.get('data').get('channel_id') != None
  assert resp.get('data').get('agent_id') != None
  assert resp.get('data').get('staff_id') != None
  assert resp.get('data').get('username') != None
  assert resp.get('data').get('action') != None
  assert resp.get('data').get('SPECIAL_CONDITION') != None
  assert resp.get('data').get('count') != None
  assert resp.get('data').get('status_detail') != None
  assert resp.get('data').get('status_detail_message') != None

def test_abnormal_wrong_pin():
  session = login_user("agen")
  post_data = """{
  	"retailer_name": "CV SEMOGA KAYA 22222222222",
  	"price": "10250",
  	"effective_date": "27-10-2018",
  	"retailer_phone": "081212345677",
  	"retailer_email": "semoga.kaya@gmail.com",
  	"pin_transaksi": "12345",
  	"price_id": "104",
  	"retailer_id": "120357",
  	"channel_id": "AGEN46",
  	"agent_id": "816",
  	"staff_id": "BNIAG50299",
  	"username": "BNIAG50299",
    "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
  	"ip_address": "10.70.9.176",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1550541552124993",
   "session": "%s"
  }
  """%(session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('error')==True
  assert resp.get('errorNum')!=None
  assert resp.get('message')!=None

  
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
  	"retailer_name": "CV SEMOGA KAYA 22222222222",
  	"price": "10250",
  	"effective_date": "27-10-2018",
  	"retailer_phone": "081212345677",
  	"retailer_email": "semoga.kaya@gmail.com",
  	"pin_transaksi": "12345",
  	"price_id": "104",
  	"retailer_id": "120357",
  	"channel_id": "AGEN46",
  	"agent_id": "816",
  	"staff_id": "BNIAG50299",
  	"username": "BNIAG50299",
    "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
  	"ip_address": "10.70.9.176",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1550541552124993",
   "session": "%s"
  }
  """ %(session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') !=None
  assert resp.get('message') !=None
  

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
  	"retailer_name": "CV SEMOGA KAYA 22222222222",
  	"price": "10250",
  	"effective_date": "27-10-2018",
  	"retailer_phone": "081212345677",
  	"retailer_email": "semoga.kaya@gmail.com",
  	"pin_transaksi": "12345",
  	"price_id": "104",
  	"retailer_id": "120351817",
  	"channel_id": "AGEN46",
  	"agent_id": "810736",
  	"staff_id": "BNIAG50299",
  	"username": "BNIAG50299",
  	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
  	"ip_address": "10.70.9.176",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1550541552124993"
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
  	"retailer_name": "CV SEMOGA KAYA 22222222222",
  	"price": "10250",
  	"effective_date": "27-10-2018",
  	"retailer_phone": "081212345677",
  	"retailer_email": "semoga.kaya@gmail.com",
  	"pin_transaksi": "12345",
  	"price_id": "104",
  	"retailer_id": "120351817",
  	"channel_id": "AGEN46",
  	"agent_id": "810736",
  	"staff_id": "BNIAG50299",
  	"username": "BNIAG50299",
  	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
  	"ip_address": "10.70.9.176",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1550541552124993",
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
	"retailer_name": "CV SEMOGA KAYA 22222222222",
	"price": "10250",
	"effective_date": "27-10-2018",
	"retailer_phone": "081212345677",
	"retailer_email": "semoga.kaya@gmail.com",
	"pin_transaksi": "12345",
	"price_id": "104",
	"retailer_id": "120351810736027",
	"channel_id": "AGEN46",
	"agent_id": "810736",
	"staff_id": "BNIAG50299",
	"username": "BNIAG50299"
  }
  """ 
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') != None
  assert resp.get('message') != None
