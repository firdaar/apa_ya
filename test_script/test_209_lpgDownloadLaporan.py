import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/lpgDownloadLaporan" % (IP_PORT)

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
  "laporan_id": "1",
  "username": "BNIAG50299",
  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
  "ip_address": "10.70.9.176",
  "id_api": "web",
  "ip_server": "68",
  "session": "%s"
  }
  """%(session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('code')=="00"
  assert resp.get('message')=="Data laporan ditemukan."
  assert resp.get('data') != None
  assert resp.get('data').get('rows') != None
  countData= resp.get('data').get('count')
  Data= resp.get('data').get('rows')
  for newData in range(0,countData):
    assert Data[newData].get('id') != None
    assert Data[newData].get('maintenance_harga_pangkalan_id') != None
    assert Data[newData].get('pangkalan_name') != None
    assert Data[newData].get('price') != None
    assert Data[newData].get('effective_date') != None
    assert Data[newData].get('hp') != None
    assert Data[newData].get('email') != None
    assert Data[newData].get('status') != None
    assert Data[newData].get('status_detail') != None
    assert Data[newData].get('created_at') != None
    assert Data[newData].get('updated_at') != None
    assert Data[newData].get('action_by') != None
    assert Data[newData].get('ip_address') == None
    assert Data[newData].get('id_pangkalan') != None
    assert Data[newData].get('index_status') != None
  assert countData
  
  
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
  "laporan_id": "1",
  "username": "BNIAG502",
  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
  "ip_address": "10.70.9.176",
  "id_api": "web",
  "ip_server": "68",
  "session": "%s"
} """ %(session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('code') == '-1'
  assert resp.get('message') =='Agen tidak ditemukan.'
  
### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
  "laporan_id": "1",
  "username": "BNIAG50299",
  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
  "ip_address": "10.70.9.176",
  "id_api": "web",
  "ip_server": "68"
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
  "laporan_id": "1",
  "username": "BNIAG50299",
  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626109 Safari/537.36",
  "ip_address": "10.70.9.176",
  "id_api": "web",
  "ip_server": "68",
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
  "laporan_id": "1",
  "username": "BNIAG50299"
  }
  """ 
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('code')=="00"
  assert resp.get('message')=="Data laporan ditemukan."
  assert resp.get('data') != None
  assert resp.get('data').get('rows') != None
  countData= resp.get('data').get('count')
  Data= resp.get('data').get('rows')
  for newData in range(0,countData):
    assert Data[newData].get('id') != None
    assert Data[newData].get('maintenance_harga_pangkalan_id') != None
    assert Data[newData].get('pangkalan_name') != None
    assert Data[newData].get('price') != None
    assert Data[newData].get('effective_date') != None
    assert Data[newData].get('hp') != None
    assert Data[newData].get('email') != None
    assert Data[newData].get('status') != None
    assert Data[newData].get('status_detail') != None
    assert Data[newData].get('created_at') != None
    assert Data[newData].get('updated_at') != None
    assert Data[newData].get('action_by') != None
    assert Data[newData].get('ip_address') == None
    assert Data[newData].get('id_pangkalan') != None
    assert Data[newData].get('index_status') != None
  assert countData

