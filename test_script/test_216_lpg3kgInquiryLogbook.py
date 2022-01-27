import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/lpg3kgInquiryLogbook" % (IP_PORT)

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
	"tipe": "monthly",
	"tglawal": "2021-04",
	"tglakhir": "2021-05",
	"username": "BNIAG100185",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1620359190749544",
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
  assert resp.get('count') != None
  assert resp.get('data')!=None
  assert resp.get('data').get('idpangkalan') != None
  assert resp.get('data').get('nama') != None
  assert resp.get('data').get('tglbeli') != None
  assert resp.get('data').get('kategori') != None
  assert resp.get('data').get('alamat') != None
  assert resp.get('data').get('deskripsi') != None
  assert resp.get('data').get('jumlah') != None
  assert resp.get('data').get('harga') != None
  assert resp.get('data').get('total') != None
  assert resp.get('data').get('channelid') != None
  assert resp.get('data').get('idlogbook') != None
  assert resp.get('errorNum')!=None

  

  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
	"tipe": "monthly",
	"tglawal": "2021-04",
	"tglakhir": "2021-05",
	"username": "BNIAG100185",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1620359190749544",
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
	"tipe": "monthly",
	"tglawal": "2021-04",
	"tglakhir": "2021-05",
	"username": "BNIAG100185",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1620359190749544"
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
	"tipe": "monthly",
	"tglawal": "2021-04",
	"tglakhir": "2021-05",
	"username": "BNIAG100185",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1620359190749544",
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
	"tipe": "monthly",
	"tglawal": "2021-04",
	"tglakhir": "2021-05",
	"username": "BNIAG100185"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('count') != None
  assert resp.get('data')!=None
  assert resp.get('data').get('idpangkalan') != None
  assert resp.get('data').get('nama') != None
  assert resp.get('data').get('tglbeli') != None
  assert resp.get('data').get('kategori') != None
  assert resp.get('data').get('alamat') != None
  assert resp.get('data').get('deskripsi') != None
  assert resp.get('data').get('jumlah') != None
  assert resp.get('data').get('harga') != None
  assert resp.get('data').get('total') != None
  assert resp.get('data').get('channelid') != None
  assert resp.get('data').get('idlogbook') != None
  assert resp.get('errorNum')!=None