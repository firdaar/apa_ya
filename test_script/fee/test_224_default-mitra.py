import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/fee/default-mitra" % (IP_PORT)

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
     "search": "",
    "offset": "0",
    "limit": "10",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625123127838157",
    "session": "%s"
  }""" % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('count')!=None
  for row in range(resp.get('count')):
    assert resp.get('rows')[row].get('id') !=None
    assert resp.get('rows')[row].get('trx_type_source') !=None
    assert resp.get('rows')[row].get('jenis_trx') !=None
    assert resp.get('rows')[row].get('industri') !=None
    assert resp.get('rows')[row].get('trx_type_target') !=None
    assert resp.get('rows')[row].get('biller_target') !=None
    assert resp.get('rows')[row].get('trx_type_source_desc') !=None
    assert resp.get('rows')[row].get('channel_source') !=None
    assert resp.get('rows')[row].get('nom_min') !=None
    assert resp.get('rows')[row].get('nom_max') !=None
    assert resp.get('rows')[row].get('fee_perorangan') !=None
    assert resp.get('rows')[row].get('fee_super_agen') !=None
    assert resp.get('rows')[row].get('biaya_loket') !=None



### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user('agen')
  post_data = """{
     "search": "",
    "offset": "0",
    "limit": "0",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625123127838157",
    "session": "%s"
  }""" % (session)
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
     "search": "",
    "offset": "0",
    "limit": "10",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625123127838157"
  }"""
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
     "search": "",
    "offset": "0",
    "limit": "10",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625123127838157",
    "session": "%s"
  }""" % (session)
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
    "search": "",
    "offset": "0",
    "limit": "10",
    "order": ""
  } """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('rows')!=None
  for row in range(resp.get('count')):
    assert resp.get('rows')[row].get('id') !=None
    assert resp.get('rows')[row].get('trx_type_source') !=None
    assert resp.get('rows')[row].get('jenis_trx') !=None
    assert resp.get('rows')[row].get('industri') !=None
    assert resp.get('rows')[row].get('trx_type_target') !=None
    assert resp.get('rows')[row].get('biller_target') !=None
    assert resp.get('rows')[row].get('trx_type_source_desc') !=None
    assert resp.get('rows')[row].get('channel_source') !=None
    assert resp.get('rows')[row].get('nom_min') !=None
    assert resp.get('rows')[row].get('nom_max') !=None
    assert resp.get('rows')[row].get('fee_perorangan') !=None
    assert resp.get('rows')[row].get('fee_super_agen') !=None
    assert resp.get('rows')[row].get('biaya_loket') !=None
  assert resp.get('count')!=None
