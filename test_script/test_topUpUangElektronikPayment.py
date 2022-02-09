import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/topUpUangElektronikPayment" % (IP_PORT)

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
	"kode_cabang": "259",
	"kode_loket": "50299",
	"accountNum": "1231",
	"pin_transaksi": "12345",
	"reffNum": "20211203103000050299",
	"providerId": "SHOPEEPAY",
	"billingLabel": "No.VA",
	"billingNumber": "081271139152",
	"trxId": "1360994050",
	"virtualAccountNumber": "8807081247181657",
	"virtualAccountName": "Shopeepay",
	"vaNameLabel": "Nama",
	"virtualAccountTrxType": "i",
	"billedAmount": "1000000",
	"billedAmountLabel": "Batas Maksimum",
	"billedAmountValue": "Rp 1.000.000",
	"clientId": "807",
	"feeAmount": "1000",
	"feeAmountLabel": "Biaya admin",
	"feeAmountValue": "IDR 1.000",
	"currency": "IDR",
	"additionalLabel1": "",
	"additionalLabel2": "",
	"additionalLabel3": "",
	"additionalValue1": "-",
	"additionalValue2": "-",
	"additionalValue3": "-",
	"amount": "3000000",
	"biaya_loket": "3000",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1595409493782703",
	"session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType')=='407'
  assert resp.get('status')=="success"
  assert resp.get('data')!= None
  assert resp.get('data').get('error')== False
  assert resp.get('data').get('ket')!= None
  assert resp.get('data').get('billingLabel')!= None
  assert resp.get('data').get('billingNumber')!= None
  assert resp.get('data').get('trxId')!= None
  assert resp.get('data').get('virtualAccountNumber')!= None
  assert resp.get('data').get('vaNameLabel')!= None
  assert resp.get('data').get('virtualAccountTrxType')!= None
  assert resp.get('data').get('billedAmount')!= None
  assert resp.get('data').get('billedAmountLabel')!= None
  assert resp.get('data').get('billedAmountValue')!= None
  assert resp.get('data').get('clientId')!= None
  assert resp.get('data').get('additionalLabel1')!= None
  assert resp.get('data').get('additionalLabel2')!= None
  assert resp.get('data').get('additionalLabel3')!= None
  assert resp.get('data').get('additionalValue1')!= None
  assert resp.get('data').get('additionalValue2')!= None
  assert resp.get('data').get('additionalValue3')!= None
  assert resp.get('data').get('depositorName')!= None
  assert resp.get('data').get('languageId')!= None
  assert resp.get('data').get('currency')!= None
  assert resp.get('data').get('feeAmount')!= None
  assert resp.get('data').get('customerIdNum')!= None
  assert resp.get('data').get('languageId')!= None
  assert resp.get('data').get('customerIdType')!= None
  assert resp.get('data').get('accountNum')!= None
  assert resp.get('data').get('paymentType')!= None
  assert resp.get('data').get('feeAmountLabel')!= None
  assert resp.get('data').get('feeAmountValue')!= None
  assert resp.get('data').get('journalNum')!= None
  assert resp.get('data').get('additional')!= None
  assert resp.get('data').get('reffNum')!= None
  assert resp.get('data').get('biaya_loket')!= None
  assert resp.get('data').get('errorNum')!= None
  assert resp.get('data').get('transactionTime')!= None
  assert resp.get('data').get('totalAmount')!= None
  assert resp.get('result')!= None
  assert resp.get('result').get('kode_loket')!= None
  assert resp.get('result').get('kd_lkt')!= None
  assert resp.get('result').get('nama')!= None
  assert resp.get('result').get('kode_cabang')!= None
  assert resp.get('result').get('kode_mitra')!= None
  assert resp.get('result').get('alamat')!= None
  assert resp.get('result').get('nama_usaha')!= None
  assert resp.get('CustomerData')!= None
  assert resp.get('CustomerData').get('time')!= None


### TC Abnormal - Transaction Already Done ###
##############################################
def test_abnormal_already_done():
  session = login_user("agen")
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"accountNum": "1231",
	"pin_transaksi": "12345",
	"reffNum": "20211203103000050299",
	"providerId": "SHOPEEPAY",
	"billingLabel": "No.VA",
	"billingNumber": "081271139152",
	"trxId": "1360994050",
	"virtualAccountNumber": "8807081247181657",
	"virtualAccountName": "Shopeepay",
	"vaNameLabel": "Nama",
	"virtualAccountTrxType": "i",
	"billedAmount": "1000000",
	"billedAmountLabel": "Batas Maksimum",
	"billedAmountValue": "Rp 1.000.000",
	"clientId": "807",
	"feeAmount": "1000",
	"feeAmountLabel": "Biaya admin",
	"feeAmountValue": "IDR 1.000",
	"currency": "IDR",
	"additionalLabel1": "",
	"additionalLabel2": "",
	"additionalLabel3": "",
	"additionalValue1": "-",
	"additionalValue2": "-",
	"additionalValue3": "-",
	"amount": "3000000",
	"biaya_loket": "3000",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1595409493782703",
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
	"kode_cabang": "259",
	"kode_loket": "50299",
	"accountNum": "1231",
	"pin_transaksi": "1235",
	"reffNum": "20211203103000050299",
	"providerId": "SHOPEEPAY",
	"billingLabel": "No.VA",
	"billingNumber": "081271139152",
	"trxId": "1360994050",
	"virtualAccountNumber": "8807081247181657",
	"virtualAccountName": "Shopeepay",
	"vaNameLabel": "Nama",
	"virtualAccountTrxType": "i",
	"billedAmount": "1000000",
	"billedAmountLabel": "Batas Maksimum",
	"billedAmountValue": "Rp 1.000.000",
	"clientId": "807",
	"feeAmount": "1000",
	"feeAmountLabel": "Biaya admin",
	"feeAmountValue": "IDR 1.000",
	"currency": "IDR",
	"additionalLabel1": "",
	"additionalLabel2": "",
	"additionalLabel3": "",
	"additionalValue1": "-",
	"additionalValue2": "-",
	"additionalValue3": "-",
	"amount": "3000000",
	"biaya_loket": "3000",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '407'
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
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"accountNum": "1231",
	"pin_transaksi": "1235",
	"reffNum": "20211203103000050299",
	"providerId": "SHOPEEPAY",
	"billingLabel": "No.VA",
	"billingNumber": "081271139152",
	"trxId": "1360994050",
	"virtualAccountNumber": "880708124711657",
	"virtualAccountName": "Shopeepay",
	"vaNameLabel": "Nama",
	"virtualAccountTrxType": "i",
	"billedAmount": "1000000",
	"billedAmountLabel": "Batas Maksimum",
	"billedAmountValue": "Rp 1.000.000",
	"clientId": "807",
	"feeAmount": "1000",
	"feeAmountLabel": "Biaya admin",
	"feeAmountValue": "IDR 1.000",
	"currency": "IDR",
	"additionalLabel1": "",
	"additionalLabel2": "",
	"additionalLabel3": "",
	"additionalValue1": "-",
	"additionalValue2": "-",
	"additionalValue3": "-",
	"amount": "3000000",
	"biaya_loket": "3000",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '407'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == True
  assert resp.get('data').get('errorNum') != None
  assert resp.get('data').get('message') != None
  assert resp.get('data').get('ori_errorNum')!=None
  assert resp.get('data').get('ori_message')!=None
  assert resp.get('result') != None
  assert resp.get('result').get('kode_loket') != None
  assert resp.get('result').get('kd_lkt') != None
  assert resp.get('result').get('nama') != None
  assert resp.get('result').get('kode_cabang') != None
  assert resp.get('result').get('kode_mitra') != None
  assert resp.get('result').get('alamat') != None
  assert resp.get('result').get('nama_usaha')!= None
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('time') != None


### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"accountNum": "1231",
	"pin_transaksi": "1235",
	"reffNum": "20211203103000050299",
	"providerId": "SHOPEEPAY",
	"billingLabel": "No.VA",
	"billingNumber": "081271139152",
	"trxId": "1360994050",
	"virtualAccountNumber": "880708124711657",
	"virtualAccountName": "Shopeepay",
	"vaNameLabel": "Nama",
	"virtualAccountTrxType": "i",
	"billedAmount": "1000000",
	"billedAmountLabel": "Batas Maksimum",
	"billedAmountValue": "Rp 1.000.000",
	"clientId": "807",
	"feeAmount": "1000",
	"feeAmountLabel": "Biaya admin",
	"feeAmountValue": "IDR 1.000",
	"currency": "IDR",
	"additionalLabel1": "",
	"additionalLabel2": "",
	"additionalLabel3": "",
	"additionalValue1": "-",
	"additionalValue2": "-",
	"additionalValue3": "-",
	"amount": "3000000",
	"biaya_loket": "3000",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1595409493782703"
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
	"kode_cabang": "259",
	"kode_loket": "50299",
	"accountNum": "1231",
	"pin_transaksi": "1235",
	"reffNum": "20211203103000050299",
	"providerId": "SHOPEEPAY",
	"billingLabel": "No.VA",
	"billingNumber": "081271139152",
	"trxId": "1360994050",
	"virtualAccountNumber": "880708124711657",
	"virtualAccountName": "Shopeepay",
	"vaNameLabel": "Nama",
	"virtualAccountTrxType": "i",
	"billedAmount": "1000000",
	"billedAmountLabel": "Batas Maksimum",
	"billedAmountValue": "Rp 1.000.000",
	"clientId": "807",
	"feeAmount": "1000",
	"feeAmountLabel": "Biaya admin",
	"feeAmountValue": "IDR 1.000",
	"currency": "IDR",
	"additionalLabel1": "",
	"additionalLabel2": "",
	"additionalLabel3": "",
	"additionalValue1": "-",
	"additionalValue2": "-",
	"additionalValue3": "-",
	"amount": "3000000",
	"biaya_loket": "3000",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"ip_address": "10.70.9.44",
	"ip_server": "68",
    "id_api": "web",
	"req_id": "1595409493782703",
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
	"kode_cabang": "259",
	"kode_loket": "50299",
	"accountNum": "1231",
	"pin_transaksi": "1235",
	"reffNum": "20211203103000050299",
	"providerId": "SHOPEEPAY",
	"billingLabel": "No.VA",
	"billingNumber": "081271139152",
	"trxId": "1360994050",
	"virtualAccountNumber": "880708124711657",
	"virtualAccountName": "Shopeepay",
	"vaNameLabel": "Nama",
	"virtualAccountTrxType": "i",
	"billedAmount": "1000000",
	"billedAmountLabel": "Batas Maksimum",
	"billedAmountValue": "Rp 1.000.000",
	"clientId": "807",
	"feeAmount": "1000",
	"feeAmountLabel": "Biaya admin",
	"feeAmountValue": "IDR 1.000",
	"currency": "IDR",
	"additionalLabel1": "",
	"additionalLabel2": "",
	"additionalLabel3": "",
	"additionalValue1": "-",
	"additionalValue2": "-",
	"additionalValue3": "-",
	"amount": "3000000",
	"biaya_loket": "3000"
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
