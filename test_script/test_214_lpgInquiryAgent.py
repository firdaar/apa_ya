import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/lpgInquiryAgent" % (IP_PORT)

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
	"channel_id": "AGENT46",
	"username": "BNIAG50299",
	"agent_id": "810736",
  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
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
  print(resp)
  assert resp.get('error') == False
  assert resp.get('code') == "00"
  assert resp.get('message')=="Agent ditemukan."
  assert resp.get('data')!=None
  assert resp.get('data').get('agent_name') != None
  assert resp.get('data').get('agent_id') != None
  assert resp.get('data').get('provinsi') != None
  assert resp.get('data').get('account_num') != None
  assert resp.get('data').get('phone_num') != None
  assert resp.get('data').get('kabupaten') != None
  assert resp.get('data').get('notif_sms') != None
  assert resp.get('data').get('agent_email') != None

### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
	"channel_id": "AGENT46",
	"username": "BNIAG50299",
	"agent_id": "8106",
  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
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
  print(resp)
  assert resp.get('error') == True
  assert resp.get('code') != None
  assert resp.get('message') != None

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
	"channel_id": "AGENT46",
	"username": "BNIAG50299",
	"agent_id": "810736",
    "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
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
  print(resp)
  assert resp.get('code') == '66'
  assert resp.get('reason') == 'Session tidak ditemukan'
   
### TC Abnormal - Session Invalid ###
#####################################
def test_abnormal_session_invalid():
  session = "12345"
  post_data = """{
	"channel_id": "AGENT46",
	"username": "BNIAG50299",
	"agent_id": "810736",
    "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
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
  print(resp)
  assert resp.get('code') == '66'
  assert resp.get('reason') == 'Session invalid'
  
### TC Bypass Session ###
#########################
def test_bypass_session():
  post_data = """{
	"channel_id": "AGENT46",
	"username": "BNIAG50299",
	"agent_id": "810736"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('error') == False
  assert resp.get('code') != None
  assert resp.get('message')!=None
  assert resp.get('data')!=None
  assert resp.get('data').get('agent_name') != None
  assert resp.get('data').get('agent_id') != None
  assert resp.get('data').get('provinsi') != None
  assert resp.get('data').get('account_num') != None
  assert resp.get('data').get('phone_num') != None
  assert resp.get('data').get('kabupaten') != None
  assert resp.get('data').get('notif_sms') != None
  assert resp.get('data').get('agent_email') != None
