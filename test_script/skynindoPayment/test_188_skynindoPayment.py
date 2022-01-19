import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/skynindoPayment" % (IP_PORT)

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
    "kode_mitra": "BNI",
  	"kode_loket": "50299",
  	"kode_cabang": "259",
  	"reffNum": "202003030951080100190",
  	"providerId": "SKYNINDO",
  	"customerId": "1014567811113333",
  	"packageCode": "101",
  	"customerName": "FAMILY 1 BLN",
  	"penalty": "0",
  	"biaya_loket": "0",
  	"biaya_adm": "0",
  	"billReffNo": "E9O855909598992",
  	"billReffNo2": "78547",
  	"amount": "800000",
  	"loket_totalAmount": 8000000,
  	"pin_transaksi": "12345",
  	"accountNum": "1231",
  	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
  	"ip_address": "10.70.9.89",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1561617885314116",
   "session": "%s"
  }
  """ %  (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '120'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == False
  assert resp.get('data').get('reffNum') != None
  assert resp.get('data').get('ket') != None
  assert resp.get('data').get('customerId') != None
  assert resp.get('data').get('packageCode') != None
  assert resp.get('data').get('customerName') != None
  assert resp.get('data').get('penalty') != None
  assert resp.get('data').get('biaya_loket') != None
  assert resp.get('data').get('biaya_adm') != None
  assert resp.get('data').get('billReffNo') != None
  assert resp.get('data').get('billReffNo2') != None
  assert resp.get('data').get('amount') != None
  assert resp.get('data').get('loket_totalAmount') != None
  assert resp.get('result') != None
  assert resp.get('result').get('kode_loket') != None
  assert resp.get('result').get('kd_lkt') != None
  assert resp.get('result').get('nama') != None
  assert resp.get('result').get('kode_cabang') != None
  assert resp.get('result').get('kode_mitra') != None
  assert resp.get('result').get('alamat') != None
  assert resp.get('result').get('nama_usaha') != None
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('time') != None

### TC Abnormal - Transaction Already Done ###
##############################################

def test_abnormal_already_done():
  session = login_user("agen")
  post_data = """{
    "kode_mitra": "BNI",
    "kode_loket": "50299",
    "kode_cabang": "259",
    "reffNum": "201906271345150000112",
    "providerId": "SKYNINDO",
    "customerId": "101456781111333112",
    "packageCode": "",
    "customerName": "FAMILY 1 BLN",
    "penalty": "0",
    "biaya_loket": "0",
    "biaya_adm": "0",
    "billReffNo": "",
    "billReffNo2": "",
    "amount": "800000",
    "loket_totalAmount": 8000000,
    "pin_transaksi": "12345",
    "accountNum": "1231",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "ip_address": "10.70.9.89",
    "ip_server": "68",
    "req_id": "1561617885314116",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') == '5006'
  assert resp.get('message') == 'Transaksi sudah dilakukan, mohon cek saldo rekening BNI dan laporan transaksi Anda. Apabila ingin mengulangi transaksi yang sama, silahkan tunggu 5 menit lagi'
  
### TC Abnormal - Wrong Pin ###
###############################
def test_abnormal_wrong_pin():
  session = login_user("agen")
  post_data = """{
    "kode_mitra": "BNI",
  	"kode_loket": "50299",
  	"kode_cabang": "259",
  	"reffNum": "202003030951080100190",
  	"providerId": "SKYNINDO",
  	"customerId": "1014567811113333",
  	"packageCode": "101",
  	"customerName": "FAMILY 1 BLN",
  	"penalty": "0",
  	"biaya_loket": "0",
  	"biaya_adm": "0",
  	"billReffNo": "E9O855909598992",
  	"billReffNo2": "78547",
  	"amount": "8000000",
  	"loket_totalAmount": 8000000,
  	"pin_transaksi": "54321",
  	"accountNum": "1231",
  	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
  	"ip_address": "10.70.9.89",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1561617885314116",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '120'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == True
  assert resp.get('data').get('errorNum') == '5013'
  assert resp.get('data').get('message') == 'TRANSAKSI GAGAL : Pin transaksi salah'
  assert resp.get('result') != None
  assert resp.get('result').get('kode_loket') != None
  assert resp.get('result').get('kd_lkt') != None
  assert resp.get('result').get('nama') != None
  assert resp.get('result').get('kode_cabang') != None
  assert resp.get('result').get('kode_mitra') != None
  assert resp.get('result').get('alamat') != None
  assert resp.get('result').get('nama_usaha') != None
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('time') != None
  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
   "kode_mitra": "BNI",
  	"kode_loket": "502993",
  	"kode_cabang": "259",
  	"reffNum": "201906271345150000112",
  	"providerId": "SKYNINDO",
  	"customerId": "101456781111333112",
  	"packageCode": "101",
  	"customerName": "FAMILY 1 BLN",
  	"penalty": "0",
  	"biaya_loket": "0",
  	"biaya_adm": "0",
  	"billReffNo": "",
  	"billReffNo2": "",
  	"amount": "8000000",
  	"loket_totalAmount": 8000000,
  	"pin_transaksi": "12345",
  	"accountNum": "1231",
  	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
  	"ip_address": "10.70.9.89",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1561617885314116",
     "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '120'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == True
  assert resp.get('data').get('errorNum') != None
  assert resp.get('data').get('message') != None
  assert resp.get('data').get('ori_errorNum') != None
  assert resp.get('data').get('ori_message') != None
  assert resp.get('result') != None
  assert resp.get('result').get('kode_loket') != None
  assert resp.get('result').get('kd_lkt') != None
  assert resp.get('result').get('nama') != None
  assert resp.get('result').get('kode_cabang') != None
  assert resp.get('result').get('kode_mitra') != None
  assert resp.get('result').get('alamat') != None
  assert resp.get('result').get('nama_usaha') != None
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('time') != None

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
   "kode_mitra": "BNI",
  	"kode_loket": "50299",
  	"kode_cabang": "259",
  	"reffNum": "2019062713451500000",
  	"providerId": "SKYNINDO",
  	"customerId": "1014567811113333",
  	"packageCode": "101",
  	"customerName": "FAMILY 1 BLN",
  	"penalty": "0",
  	"biaya_loket": "0",
  	"biaya_adm": "0",
  	"billReffNo": "",
  	"billReffNo2": "",
  	"amount": "8000000",
  	"loket_totalAmount": 8000000,
  	"pin_transaksi": "12345",
  	"accountNum": "1231",
  	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
  	"ip_address": "10.70.9.89",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1561617885314116"
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
   "kode_mitra": "BNI",
  	"kode_loket": "50299",
  	"kode_cabang": "259",
  	"reffNum": "2019062713451500000",
  	"providerId": "SKYNINDO",
  	"customerId": "1014567811113333",
  	"packageCode": "101",
  	"customerName": "FAMILY 1 BLN",
  	"penalty": "0",
  	"biaya_loket": "0",
  	"biaya_adm": "0",
  	"billReffNo": "",
  	"billReffNo2": "",
  	"amount": "8000000",
  	"loket_totalAmount": 8000000,
  	"pin_transaksi": "12345",
  	"accountNum": "1231",
  	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
  	"ip_address": "10.70.9.89",
  	"id_api": "web",
  	"ip_server": "68",
  	"req_id": "1561617885314116",
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
    "kode_mitra": "BNI",
  	"kode_loket": "50299",
  	"kode_cabang": "259",
  	"reffNum": "2019062713451500000",
  	"providerId": "SKYNINDO",
  	"customerId": "1014567811113333",
  	"packageCode": "101",
  	"customerName": "FAMILY 1 BLN",
  	"penalty": "0",
  	"biaya_loket": "0",
  	"biaya_adm": "0",
  	"billReffNo": "",
  	"billReffNo2": "",
  	"amount": "8000000",
  	"loket_totalAmount": 8000000,
  	"pin_transaksi": "12345",
  	"accountNum": "1231"
  }
  """ 
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') == '5006'
  assert resp.get('message') == 'Transaksi sudah dilakukan, mohon cek saldo rekening BNI dan laporan transaksi Anda. Apabila ingin mengulangi transaksi yang sama, silahkan tunggu 5 menit lagi'
