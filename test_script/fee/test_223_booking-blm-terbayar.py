import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/fee/booking-blm-terbayar" % (IP_PORT)

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
     "username": "BNIAG50299",
    "start_date": "2021-12-25",
    "end_date": "2021-01-25",
    "offset": "",
    "limit": "",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625112989690107",
    "session": "%s"
  }""" % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('rows')!=None
  assert resp.get('rows').get('transaksi_id')!=None
  assert resp.get('rows').get('kode_mitra')!=None
  assert resp.get('rows').get('kode_cabang')!=None
  assert resp.get('rows').get('kode_loket')!=None
  assert resp.get('rows').get('datetime')!=None
  assert resp.get('rows').get('industri')!=None
  assert resp.get('rows').get('trx_name')!=None
  assert resp.get('rows').get('flag_fee_loket')!=None
  assert resp.get('rows').get('jumlah_transaksi')!=None
  assert resp.get('rows').get('pendapatan_per_transaksi')!=None
  assert resp.get('rows').get('total_pendapatan')!=None
  assert resp.get('rows').get('status')!=None
  assert resp.get('rows').get('via')!=None
  assert resp.get('footer') !=None
  assert resp.get('footer').get('jumlah_transaksi_cr')!=None
  assert resp.get('footer').get('jumlah_transaksi_db')!=None
  assert resp.get('footer').get('total_pendapatan_cr')!=None
  assert resp.get('footer').get('total_pendapatan_db')!=None

  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user('agen')
  post_data = """{
     "username": "BNIAG5029",
    "start_date": "2021-12-25",
    "end_date": "2021-01-25",
    "offset": "",
    "limit": "",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625112989690107",
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
     "username": "BNIAG50299",
    "start_date": "2021-12-25",
    "end_date": "2021-01-25",
    "offset": "",
    "limit": "",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625112989690107"
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
     "username": "BNIAG50299",
    "start_date": "2021-12-25",
    "end_date": "2021-01-25",
    "offset": "",
    "limit": "",
    "order": "",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472124 Safari/537.36",
    "ip_address": "10.45.63.51",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1625112989690107",
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
     "username": "BNIAG50299",
    "start_date": "2021-12-25",
    "end_date": "2021-01-25",
    "offset": "",
    "limit": "",
    "order": ""
  } """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('rows')!=None
  assert resp.get('rows').get('transaksi_id')!=None
  assert resp.get('rows').get('kode_mitra')!=None
  assert resp.get('rows').get('kode_cabang')!=None
  assert resp.get('rows').get('kode_loket')!=None
  assert resp.get('rows').get('datetime')!=None
  assert resp.get('rows').get('industri')!=None
  assert resp.get('rows').get('trx_name')!=None
  assert resp.get('rows').get('flag_fee_loket')!=None
  assert resp.get('rows').get('jumlah_transaksi')!=None
  assert resp.get('rows').get('pendapatan_per_transaksi')!=None
  assert resp.get('rows').get('total_pendapatan')!=None
  assert resp.get('rows').get('status')!=None
  assert resp.get('rows').get('via')!=None
  assert resp.get('footer') !=None
  assert resp.get('footer').get('jumlah_transaksi_cr')!=None
  assert resp.get('footer').get('jumlah_transaksi_db')!=None
  assert resp.get('footer').get('total_pendapatan_cr')!=None
  assert resp.get('footer').get('total_pendapatan_db')!=None
