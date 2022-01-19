import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/IBSPayment" % (IP_PORT)

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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "%s",
	"h_billingId": "2019080113540183",
	"h_billingName": "TEST IBS, PT",
	"h_channelId": "ATM",
	"h_billAmount": "2440000",
	"h_billInfo6": "IBS PELINDO",
	"h_billInfo71": "111776000287",
	"h_billInfo72": "111776000286",
	"h_billInfo73": "111776000285",
	"h_billInfo74": "111776000284",
	"h_billInfo75": "111776000283",
	"h_billInfo76": "111776000282",
	"h_billInfo77": "111776000281",
	"h_billInfo78": "111776000280",
	"h_billInfo79": "111776000279",
	"h_billInfo710": "111776000278",
	"c_fee": "1500",
	"loket_totalBayar": 2441500,
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1578292029814561",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '124'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == False
  assert resp.get('data').get('reffNum') != None
  assert resp.get('data').get('ket') != None
  assert resp.get('data').get('h_billingId') != None
  assert resp.get('data').get('h_billingName') != None
  assert resp.get('data').get('h_channelId') != None
  assert resp.get('data').get('h_billAmount') != None
  assert resp.get('data').get('h_billInfo6') != None
  assert resp.get('data').get('c_fee') != None
  assert resp.get('data').get('loket_totalBayar') != None
  assert resp.get('data').get('financialJournal') != None
  assert resp.get('data').get('h_status') != None
  assert resp.get('data').get('errorNum') != None
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "%s",
	"h_billingId": "2019080113540183",
	"h_billingName": "TEST IBS, PT",
	"h_channelId": "ATM",
	"h_billAmount": "2440000",
	"h_billInfo6": "IBS PELINDO",
	"h_billInfo71": "111776000287",
	"h_billInfo72": "111776000286",
	"h_billInfo73": "111776000285",
	"h_billInfo74": "111776000284",
	"h_billInfo75": "111776000283",
	"h_billInfo76": "111776000282",
	"h_billInfo77": "111776000281",
	"h_billInfo78": "111776000280",
	"h_billInfo79": "111776000279",
	"h_billInfo710": "111776000278",
	"c_fee": "1500",
	"loket_totalBayar": 2441500,
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1578292029814561",
    "session": "%s"
  }
  """ % (reffNum,session)
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "%s",
	"h_billingId": "2019080113540183",
	"h_billingName": "TEST IBS, PT",
	"h_channelId": "ATM",
	"h_billAmount": "244000000",
	"h_billInfo6": "IBS PELINDO",
	"h_billInfo71": "111776000287",
	"h_billInfo72": "111776000286",
	"h_billInfo73": "111776000285",
	"h_billInfo74": "111776000284",
	"h_billInfo75": "111776000283",
	"h_billInfo76": "111776000282",
	"h_billInfo77": "111776000281",
	"h_billInfo78": "111776000280",
	"h_billInfo79": "111776000279",
	"h_billInfo710": "111776000278",
	"c_fee": "1500",
	"loket_totalBayar": 2441500,
	"pin_transaksi": "1231",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1578292029814561",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '124'
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
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('time') != None
  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  reffNum=time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "%s",
	"h_billingId": "2019080183",
	"h_billingName": "TEST IBS, PT",
	"h_channelId": "ATM",
	"h_billAmount": "2440000",
	"h_billInfo6": "IBS PELINDO",
	"h_billInfo71": "111776000287",
	"h_billInfo72": "111776000286",
	"h_billInfo73": "111776000285",
	"h_billInfo74": "111776000284",
	"h_billInfo75": "111776000283",
	"h_billInfo76": "111776000282",
	"h_billInfo77": "111776000281",
	"h_billInfo78": "111776000280",
	"h_billInfo79": "111776000279",
	"h_billInfo710": "111776000278",
	"c_fee": "1500",
	"loket_totalBayar": 2441500,
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1578292029814561",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '124'
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
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('time') != None

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  reffNum=time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "%s",
	"h_billingId": "2019080113540183",
	"h_billingName": "TEST IBS, PT",
	"h_channelId": "ATM",
	"h_billAmount": "2440000",
	"h_billInfo6": "IBS PELINDO",
	"h_billInfo71": "111776000287",
	"h_billInfo72": "111776000286",
	"h_billInfo73": "111776000285",
	"h_billInfo74": "111776000284",
	"h_billInfo75": "111776000283",
	"h_billInfo76": "111776000282",
	"h_billInfo77": "111776000281",
	"h_billInfo78": "111776000280",
	"h_billInfo79": "111776000279",
	"h_billInfo710": "111776000278",
	"c_fee": "1500",
	"loket_totalBayar": 2441500,
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1578292029814561"
  }
  """ %(reffNum)
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
  reffNum=time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "%s",
	"h_billingId": "2019080113540183",
	"h_billingName": "TEST IBS, PT",
	"h_channelId": "ATM",
	"h_billAmount": "2440000",
	"h_billInfo6": "IBS PELINDO",
	"h_billInfo71": "111776000287",
	"h_billInfo72": "111776000286",
	"h_billInfo73": "111776000285",
	"h_billInfo74": "111776000284",
	"h_billInfo75": "111776000283",
	"h_billInfo76": "111776000282",
	"h_billInfo77": "111776000281",
	"h_billInfo78": "111776000280",
	"h_billInfo79": "111776000279",
	"h_billInfo710": "111776000278",
	"c_fee": "1500",
	"loket_totalBayar": 2441500,
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"ip_address": "10.70.9.44",
	"id_api": "web",
	"ip_server": "68",
	"req_id": "1578292029814561",
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
  reffNum=time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
	"kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"reffNum": "%s",
	"h_billingId": "2019080113540183",
	"h_billingName": "TEST IBS, PT",
	"h_channelId": "ATM",
	"h_billAmount": "2440000",
	"h_billInfo6": "IBS PELINDO",
	"h_billInfo71": "111776000287",
	"h_billInfo72": "111776000286",
	"h_billInfo73": "111776000285",
	"h_billInfo74": "111776000284",
	"h_billInfo75": "111776000283",
	"h_billInfo76": "111776000282",
	"h_billInfo77": "111776000281",
	"h_billInfo78": "111776000280",
	"h_billInfo79": "111776000279",
	"h_billInfo710": "111776000278",
	"c_fee": "1500",
	"loket_totalBayar": 2441500,
	"pin_transaksi": "12345",
	"accountNum": "1231"
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
