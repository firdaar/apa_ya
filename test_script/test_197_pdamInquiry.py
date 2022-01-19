import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/pdamInquiry" % (IP_PORT)

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

#browser,id_add,id_api,ip_server,req_id sama semua untuk post login 
#untuk seterusnya mengikuti format request
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
    "clientId": "IBOC",
    "reffNum": "%s",
    "providerId": "PDAM_BANDUNG",
    "adminFeeFlag": "0",
    "pdam_type": "IPL/PAM_BSD",
    "billingId": "011111113",
    "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "ip_address": "172.18.0.69",
    "id_api": "web",
    "ip_server": "68",
    "session": "%s"
  }
  """ %(reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('billingId') != None
  assert resp.get('customerName') != None
  assert resp.get('flag') != None
  assert resp.get('billRepeatCount') != None
  assert resp.get('kandatelNum') != None
  assert resp.get('langCode') != None
  assert resp.get('billerCode') != None
  assert resp.get('adminFee') != None
  assert resp.get('billDate') != None
  assert resp.get('billAmount') != None
  assert resp.get('amount') != None
  assert resp.get('bl_th') != None
  assert resp.get('nominalTagihan') != None
  assert resp.get('penalti') != None
  assert resp.get('totalTagihan') != None
  

  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
 	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG",
	"adminFeeFlag": "0",
	"pdam_type": "IPL/PAM_BSD",
	"billingId": "01111111310",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68",
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG",
	"adminFeeFlag": "0",
	"pdam_type": "IPL/PAM_BSD",
	"billingId": "011111113",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68"
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
  "clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG",
	"adminFeeFlag": "0",
	"pdam_type": "IPL/PAM_BSD",
	"billingId": "011111113",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68",
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
  "clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG",
	"adminFeeFlag": "0",
	"pdam_type": "IPL/PAM_BSD",
	"billingId": "011111113"
  }
  """%(reffNum)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('billingId') != None
  assert resp.get('customerName') != None
  assert resp.get('flag') != None
  assert resp.get('billRepeatCount') != None
  assert resp.get('kandatelNum') != None
  assert resp.get('langCode') != None
  assert resp.get('billerCode') != None
  assert resp.get('adminFee') != None
  assert resp.get('billDate') != None
  assert resp.get('billAmount') != None
  assert resp.get('amount') != None
  assert resp.get('bl_th') != None
  assert resp.get('nominalTagihan') != None
  assert resp.get('penalti') != None
  assert resp.get('totalTagihan') != None
  