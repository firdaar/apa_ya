import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/lpg3kgInsertLogbook" % (IP_PORT)

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

reffNum=time.strftime("%Y%m%d%H%M%S") + '0100185'
### TC Normal ###
#################
def test_normal():
  session = login_user("agen")
  post_data = """{
  "nama": "nurus test",
	"tglbeli": "2021-05-07",
	"kategori": "Rumah Tangga",
	"alamat": "palmerah",
	"deskripsi": "toko nurus",
	"jumlah": "18",
	"harga": "19500",
	"total": "351000",
	"username": "BNIAG100185",
	"reffNum": "%s",
	"pin_transaksi": "bni098765",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1620352037409454",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('data') != None
  assert resp.get('data').get('error') == False
  assert resp.get('data').get('idpangkalan') != None
  assert resp.get('data').get('nama') != None
  assert resp.get('data').get('tglbeli') != None
  assert resp.get('data').get('kategori') != None
  assert resp.get('data').get('alamat') != None
  assert resp.get('data').get('deskripsi') != None
  assert resp.get('data').get('harga') != None
  assert resp.get('data').get('jumlah') != None
  assert resp.get('data').get('total') != None
  assert resp.get('data').get('code') != None
  assert resp.get('errorNum')!=None

def test_abnormal_wrong_pin():
  session = login_user("agen")
  post_data = """{
  	"nama": "nurus test",
  	"tglbeli": "2021-05-07",
  	"kategori": "Rumah Tangga",
  	"alamat": "palmerah",
  	"deskripsi": "toko nurus",
  	"jumlah": "18",
  	"harga": "19500",
  	"total": "351000",
  	"username": "BNIAG100185",
  	"reffNum": "%s",
  	"pin_transaksi": "145",
  	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
  	"ip_address": "10.70.9.164",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1620352037409454",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') == '-2'
  assert resp.get('message') == 'Pin transaksi salah.'

  
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
	"nama": "nurus test",
	"tglbeli": "2021-05-07",
	"kategori": "Rumah Tangga",
	"alamat": "palmerah",
	"deskripsi": "toko nurus",
	"jumlah": "18",
	"harga": "19500",
	"total": "351000",
	"username": "BNIAG100185",
	"reffNum": "202105070847170100185",
	"pin_transaksi": "bni098765",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	"ip_address": "10.70.9.164",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1620352037409454",
	"session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') == "-1"
  assert resp.get('message') == "Duplicate reffNum"

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
  	"nama": "nurus test",
  	"tglbeli": "2021-05-07",
  	"kategori": "Rumah Tangga",
  	"alamat": "palmerah",
  	"deskripsi": "toko nurus",
  	"jumlah": "18",
  	"harga": "19500",
  	"total": "351000",
  	"username": "BNIAG100185",
  	"reffNum": "%s",
  	"pin_transaksi": "bni098765",
  	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
  	"ip_address": "10.70.9.164",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1620352037409454"
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
  session = "bni098765"
  post_data = """{
  	"nama": "nurus test",
  	"tglbeli": "2021-05-07",
  	"kategori": "Rumah Tangga",
  	"alamat": "palmerah",
  	"deskripsi": "toko nurus",
  	"jumlah": "18",
  	"harga": "19500",
  	"total": "351000",
  	"username": "BNIAG100185",
  	"reffNum": "%s",
  	"pin_transaksi": "bni098765",
  	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
  	"ip_address": "10.70.9.164",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1620352037409454",
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
  post_data = """{
  	"nama": "nurus test",
  	"tglbeli": "2021-05-07",
  	"kategori": "Rumah Tangga",
  	"alamat": "palmerah",
  	"deskripsi": "toko nurus",
  	"jumlah": "18",
  	"harga": "19500",
  	"total": "351000",
  	"username": "BNIAG100185",
  	"reffNum": "%s",
  	"pin_transaksi": "bni098765"
  }
  """ %(reffNum)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') == '5006'
  assert resp.get('message') == 'Transaksi sudah dilakukan, mohon cek saldo rekening BNI dan laporan transaksi Anda. Apabila ingin mengulangi transaksi yang sama, silahkan tunggu 5 menit lagi'
