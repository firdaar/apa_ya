import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/pdamPayment" % (IP_PORT)

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
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG,",
	"billingId": "011111113",
	"customerName": "ATIEK SETYOWATIY",
	"response": "<billReffNo>111111111111111</billReffNo><description1>201511</description1><description1Byte></description1Byte><description2></description2><description2Byte></description2Byte><description3></description3><description3Byte></description3Byte>",
	"bl_th": "NOV15",
	"penalti": "00000000",
	"namaPerusahaan": "IPL BSD",
	"kubikasi": "0",
	"amount": "10000",
	"adminFee": "2500",
	"nominalTagihan": "1000000",
	"totalTagihan": "102500",
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '69'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == False
  assert resp.get('data').get('ket') != None
  assert resp.get('data').get('reffNum') != None
  assert resp.get('data').get('journal') != None
  assert resp.get('data').get('billingId') != None
  assert resp.get('data').get('customerName') != None
  assert resp.get('data').get('response') != None
  assert resp.get('data').get('bl_th') != None
  assert resp.get('data').get('penalti') != None
  assert resp.get('data').get('footerNote') != None
  assert resp.get('data').get('kubikasi') != None
  assert resp.get('data').get('amount') != None
  assert resp.get('data').get('financialJournal') != None
  assert resp.get('data').get('nominalTagihan') != None
  assert resp.get('data').get('totalTagihan') != None
  assert resp.get('data').get('accountNum') != None
  assert resp.get('data').get('errorNum') != None
  assert resp.get('result')!= None
  assert resp.get('result').get('kode_loket') != None
  assert resp.get('result').get('kd_lkt') != None
  assert resp.get('result').get('nama') != None
  assert resp.get('result').get('kode_cabang') != None
  assert resp.get('result').get('kode_mitra') != None
  assert resp.get('result').get('alamat') != None
  assert resp.get('result').get('nama_usaha') != None
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('noRek') != None
  assert resp.get('CustomerData').get('customerName') != None
  assert resp.get('CustomerData').get('namaPerusahaan') != None
  assert resp.get('CustomerData').get('adminFee') != None
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
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG,",
	"billingId": "011111113",
	"customerName": "ATIEK SETYOWATIY",
	"response": "<billReffNo>111111111111111</billReffNo><description1>201511</description1><description1Byte></description1Byte><description2></description2><description2Byte></description2Byte><description3></description3><description3Byte></description3Byte>",
	"bl_th": "NOV15",
	"penalti": "00000000",
	"namaPerusahaan": "IPL BSD",
	"kubikasi": "0",
	"amount": "10000",
	"adminFee": "2500",
	"nominalTagihan": "1000000",
	"totalTagihan": "102500",
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68",
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
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG,",
	"billingId": "011111113",
	"customerName": "ATIEK SETYOWATIY",
	"response": "<billReffNo>111111111111111</billReffNo><description1>201511</description1><description1Byte></description1Byte><description2></description2><description2Byte></description2Byte><description3></description3><description3Byte></description3Byte>",
	"bl_th": "NOV15",
	"penalti": "00000000",
	"namaPerusahaan": "IPL BSD",
	"kubikasi": "0",
	"amount": "1009870",
	"adminFee": "2500",
	"nominalTagihan": "1000000",
	"totalTagihan": "102500",
	"pin_transaksi": "123",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68",
  "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('trxType') == '69'
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
  assert resp.get('CustomerData').get('noRek') != None
  assert resp.get('CustomerData').get('customerName') != None
  assert resp.get('CustomerData').get('namaPerusahaan') != None
  assert resp.get('CustomerData').get('adminFee') != None
  assert resp.get('CustomerData').get('time') != None
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
  "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG,",
	"billingId": "0111111130",
	"customerName": "ATIEK SETYOWATIY",
	"response": "<billReffNo>111111111111111</billReffNo><description1>201511</description1><description1Byte></description1Byte><description2></description2><description2Byte></description2Byte><description3></description3><description3Byte></description3Byte>",
	"bl_th": "NOV15",
	"penalti": "00000000",
	"namaPerusahaan": "IPL BSD",
	"kubikasi": "0",
	"amount": "10000",
	"adminFee": "2500",
	"nominalTagihan": "1000000",
	"totalTagihan": "102500",
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '69'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == True
  assert resp.get('data').get('bl_th') != None
  assert resp.get('data').get('message') != None
  assert resp.get('data').get('penalti') != None
  assert resp.get('data').get('kubikasi') != None
  assert resp.get('data').get('nominalTagihan') != None
  assert resp.get('data').get('totalTagihan') != None
  assert resp.get('data').get('kubikasi') != None
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
  assert resp.get('CustomerData').get('noRek') != None
  assert resp.get('CustomerData').get('customerName') != None
  assert resp.get('CustomerData').get('namaPerusahaan') != None
  assert resp.get('CustomerData').get('adminFee') != None
  assert resp.get('CustomerData').get('time') != None
### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
  "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG,",
	"billingId": "011111113",
	"customerName": "ATIEK SETYOWATIY",
	"response": "<billReffNo>111111111111111</billReffNo><description1>201511</description1><description1Byte></description1Byte><description2></description2><description2Byte></description2Byte><description3></description3><description3Byte></description3Byte>",
	"bl_th": "NOV15",
	"penalti": "00000000",
	"namaPerusahaan": "IPL BSD",
	"kubikasi": "0",
	"amount": "10000",
	"adminFee": "2500",
	"nominalTagihan": "1000000",
	"totalTagihan": "102500",
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68"
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
  "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG,",
	"billingId": "011111113",
	"customerName": "ATIEK SETYOWATIY",
	"response": "<billReffNo>111111111111111</billReffNo><description1>201511</description1><description1Byte></description1Byte><description2></description2><description2Byte></description2Byte><description3></description3><description3Byte></description3Byte>",
	"bl_th": "NOV15",
	"penalti": "00000000",
	"namaPerusahaan": "IPL BSD",
	"kubikasi": "0",
	"amount": "10000",
	"adminFee": "2500",
	"nominalTagihan": "1000000",
	"totalTagihan": "102500",
	"pin_transaksi": "12345",
	"accountNum": "1231",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"ip_address": "172.18.0.69",
	"id_api": "web",
	"ip_server": "68",
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
  reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"clientId": "IBOC",
	"reffNum": "%s",
	"providerId": "PDAM_BANDUNG,",
	"billingId": "011111113",
	"customerName": "ATIEK SETYOWATIY",
	"response": "<billReffNo>111111111111111</billReffNo><description1>201511</description1><description1Byte></description1Byte><description2></description2><description2Byte></description2Byte><description3></description3><description3Byte></description3Byte>",
	"bl_th": "NOV15",
	"penalti": "00000000",
	"namaPerusahaan": "IPL BSD",
	"kubikasi": "0",
	"amount": "10000",
	"adminFee": "2500",
	"nominalTagihan": "1000000",
	"totalTagihan": "102500",
	"pin_transaksi": "12345",
	"accountNum": "1231"
  }
  """%(reffNum)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') == '5006'
  assert resp.get('message') == 'Transaksi sudah dilakukan, mohon cek saldo rekening BNI dan laporan transaksi Anda. Apabila ingin mengulangi transaksi yang sama, silahkan tunggu 5 menit lagi'
