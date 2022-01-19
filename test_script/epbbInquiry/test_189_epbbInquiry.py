import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/epbbInquiry" % (IP_PORT)

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
  
session = login_user("agen")
### TC Normal ###
#################
def test_normal():
  #session = login_user("agen")
  post_data = """{
    "reffNum": "202101181331490100185",
	  "nop": "510301000100300020",
	  "tahunPajak": "2016",
	  "providerId": "PBB",
	  "daerah": "",
	  "billerCode": "",
	  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	  "ip_address": "10.45.63.50",
	  "id_api": "web",
	  "ip_server": "68",
	  "req_id": "1610951509458005",
    "session": "%s"
  }""" % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') ==False
  assert resp.get('reffNum') != None
  assert resp.get('providerId') != None
  assert resp.get('billerCode') != None
  assert resp.get('daerah') != None
  assert resp.get('amount') != None
  assert resp.get('nop') != None
  assert resp.get('namaWp') != None
  assert resp.get('tahunPajak') != None
  assert resp.get('jumlahTagihan') != None
  assert resp.get('kecamatan') != None
  assert resp.get('alamatWp') != None
  assert resp.get('fee') != None
  assert resp.get('namaPBB') != None
  assert resp.get('total_amount') != None
  assert resp.get('jenisPajakAtauKodya') != None
  assert resp.get('kodeRekeningPokok') != None
  assert resp.get('kodeRekeningBunga') != None
  assert resp.get('kodeRekeningDenda') != None
  assert resp.get('kodeRekeningSanksi') != None
  assert resp.get('jumlahPokok') != None
  assert resp.get('jumlahDenda') != None
  assert resp.get('jumlahSanksi') != None
  assert resp.get('ket') != None
  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  #session = login_user('agen')
  post_data = """{
    "reffNum": "2021011813314901001851",
	  "nop": "5103010001003000201",
	  "tahunPajak": "2016",
	  "providerId": "PBD",
	  "daerah": "",
	  "billerCode": "",
	  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	  "ip_address": "10.45.63.50",
	  "id_api": "web",
	  "ip_server": "68",
	  "req_id": "1610951509458005",
    "session": "%s"
  }""" % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  print(json.loads(post_data))
  print(http_endpoint)
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
    "reffNum": "202101181331490100185",
	  "nop": "510301000100300020",
	  "tahunPajak": "2016",
	  "providerId": "PBB",
	  "daerah": "",
	  "billerCode": "",
	  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	  "ip_address": "10.45.63.50",
	  "id_api": "web",
	  "ip_server": "68",
	  "req_id": "1610951509458005"
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
    "reffNum": "202101181331490100185",
	  "nop": "510301000100300020",
	  "tahunPajak": "2016",
	  "providerId": "PBB",
	  "daerah": "",
	  "billerCode": "",
	  "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	  "ip_address": "10.45.63.50",
	  "id_api": "web",
	  "ip_server": "68",
	  "req_id": "1610951509458005",
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
    "reffNum": "202101181331490100185",
	  "nop": "510301000100300020",
	  "tahunPajak": "2016",
	  "providerId": "PBB",
	  "daerah": "",
	  "billerCode": ""
  } """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') ==False
  assert resp.get('reffNum') != None
  assert resp.get('providerId') != None
  assert resp.get('billerCode') != None
  assert resp.get('daerah') != None
  assert resp.get('amount') != None
  assert resp.get('nop') != None
  assert resp.get('namaWp') != None
  assert resp.get('tahunPajak') != None
  assert resp.get('jumlahTagihan') != None
  assert resp.get('kecamatan') != None
  assert resp.get('alamatWp') != None
  assert resp.get('fee') != None
  assert resp.get('namaPBB') != None
  assert resp.get('total_amount') != None
  assert resp.get('jenisPajakAtauKodya') != None
  assert resp.get('kodeRekeningPokok') != None
  assert resp.get('kodeRekeningBunga') != None
  assert resp.get('kodeRekeningDenda') != None
  assert resp.get('kodeRekeningSanksi') != None
  assert resp.get('jumlahPokok') != None
  assert resp.get('jumlahDenda') != None
  assert resp.get('jumlahSanksi') != None
  assert resp.get('ket') != None