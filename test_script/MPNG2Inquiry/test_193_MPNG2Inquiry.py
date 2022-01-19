import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/MPNG2Inquiry" % (IP_PORT)

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
    "reffNum": "201909111038260100164",
	"billingId": "115030016764845",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1568173106864228",
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
  assert resp.get('h_npwp') != None
  assert resp.get('h_nama') != None
  assert resp.get('h_alamat') != None
  assert resp.get('h_akun') != None
  assert resp.get('h_kdJnsSetoran') != None
  assert resp.get('h_masaPajak') != None
  assert resp.get('h_nomorSK') != None
  assert resp.get('h_nop') != None
  assert resp.get('h_jnsDokumen') != None
  assert resp.get('h_nmrDokumen') != None
  assert resp.get('h_tglDokumen') != None
  assert resp.get('h_kdKpbc') != None
  assert resp.get('h_kodeKL') != None
  assert resp.get('h_unitEselon') != None
  assert resp.get('h_kdSatker') != None
  assert resp.get('h_currency') != None
  assert resp.get('c_adminBank') != None
  assert resp.get('h_tagihan') != None
  assert resp.get('c_totalBayar') != None
  

  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
 	"reffNum": "201909111038260100",
	"billingId": "115030016764",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1568173106864228",
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
	"reffNum": "201909111038260100164",
	"billingId": "115030016764845",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1568173106864228"
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
  "reffNum": "201909111038260100164",
	"billingId": "115030016764845",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1568173106864228",
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
   	"reffNum": "201909111038260100164",
	"billingId": "115030016764845"
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
  assert resp.get('h_npwp') != None
  assert resp.get('h_nama') != None
  assert resp.get('h_alamat') != None
  assert resp.get('h_akun') != None
  assert resp.get('h_kdJnsSetoran') != None
  assert resp.get('h_masaPajak') != None
  assert resp.get('h_nomorSK') != None
  assert resp.get('h_nop') != None
  assert resp.get('h_jnsDokumen') != None
  assert resp.get('h_nmrDokumen') != None
  assert resp.get('h_tglDokumen') != None
  assert resp.get('h_kdKpbc') != None
  assert resp.get('h_kodeKL') != None
  assert resp.get('h_unitEselon') != None
  assert resp.get('h_kdSatker') != None
  assert resp.get('h_currency') != None
  assert resp.get('c_adminBank') != None
  assert resp.get('h_tagihan') != None
  assert resp.get('c_totalBayar') != None
  