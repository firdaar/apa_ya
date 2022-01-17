import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

#IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
IP_PORT = os.getenv("IP_PORT", "192.168.250.130:8080")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/umptkinPayment" % (IP_PORT)

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

transactionId = time.strftime("%Y%m%d%H%M%S") + '050299'
### TC Normal ###
#################
def test_normal():
  session = login_user("agen")
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"billerCode": "0026",
	"univCode": "3001",
	"billingNumber": "1234567890",
	"flexiField": "1",
	"univName": "UM PTKIN",
	"isRegistration": "N",
	"studentId": "1220277890",
	"studentName": "MUHAMMAD YUFIAN PUTRA PRATAMA",
	"phoneNumber": "08111222333",
	"numberOfBills": "1",
	"billInfo": "UM-PTKIN",
	"billAmount": "205000",
	"billCode": "01",
	"totalAmount": "205000",
	"fee": "0",
	"narration": "",
	"transactionId": "%s",
	"paymentStatus": "PAID",
	"pin_transaksi": "12345",
	"accountNumber": "1231",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (transactionId, session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '64'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == False
  assert resp.get('data').get('billerCode') != None
  assert resp.get('data').get('univCode') != None
  assert resp.get('data').get('billingNumber') != None
  assert resp.get('data').get('flexiField') != None
  assert resp.get('data').get('univName') != None
  assert resp.get('data').get('isRegistration') != None
  assert resp.get('data').get('studentId') != None
  assert resp.get('data').get('studentName') != None
  assert resp.get('data').get('phoneNumber') != None
  assert resp.get('data').get('numberOfBills') != None
  assert resp.get('data').get('billInfo') != None
  assert resp.get('data').get('billAmount') != None
  assert resp.get('data').get('billCode') != None
  assert resp.get('data').get('totalAmount') != None
  assert resp.get('data').get('paymentMethod') != None
  assert resp.get('data').get('accountNumber') != None
  assert resp.get('data').get('narration') != None
  assert resp.get('data').get('transactionId') != None
  assert resp.get('data').get('paymentDate') != None
  assert resp.get('data').get('fee') != None
  assert resp.get('data').get('branchNumber') != None
  assert resp.get('data').get('tellerNumber') != None
  assert resp.get('data').get('journalNumber') != None
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
  assert resp.get('CustomerData').get('biaya_adm') != None
  assert resp.get('CustomerData').get('nominal') != None
  assert resp.get('CustomerData').get('time') != None

### TC Abnormal - Transaction Already Done ###
##############################################
def test_abnormal_already_done():
  session = login_user("agen")
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"billerCode": "0026",
	"univCode": "3001",
	"billingNumber": "1234567890",
	"flexiField": "1",
	"univName": "UM PTKIN",
	"isRegistration": "N",
	"studentId": "1220277890",
	"studentName": "MUHAMMAD YUFIAN PUTRA PRATAMA",
	"phoneNumber": "08111222333",
	"numberOfBills": "1",
	"billInfo": "UM-PTKIN",
	"billAmount": "205000",
	"billCode": "01",
	"totalAmount": "205000",
	"fee": "0",
	"narration": "",
	"transactionId": "%s",
	"paymentStatus": "PAID",
	"pin_transaksi": "12345",
	"accountNumber": "1231",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (transactionId, session)
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
  transactionId = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"billerCode": "0026",
	"univCode": "3001",
	"billingNumber": "1234567890",
	"flexiField": "1",
	"univName": "UM PTKIN",
	"isRegistration": "N",
	"studentId": "1220277890",
	"studentName": "MUHAMMAD YUFIAN PUTRA PRATAMA",
	"phoneNumber": "08111222333",
	"numberOfBills": "1",
	"billInfo": "UM-PTKIN",
	"billAmount": "205000",
	"billCode": "01",
	"totalAmount": "204000",
	"fee": "0",
	"narration": "",
	"transactionId": "%s",
	"paymentStatus": "PAID",
	"pin_transaksi": "54321",
	"accountNumber": "1231",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (transactionId, session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '64'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == True
  assert resp.get('data').get('errorNum') == '-2'
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
  assert resp.get('CustomerData').get('biaya_adm') != None
  assert resp.get('CustomerData').get('noRek') != None
  assert resp.get('CustomerData').get('nominal') != None
  assert resp.get('CustomerData').get('time') != None
  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  transactionId = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"billerCode": "0026",
	"univCode": "30011",
	"billingNumber": "1234567890",
	"flexiField": "1",
	"univName": "UM PTKIN",
	"isRegistration": "N",
	"studentId": "1220277890",
	"studentName": "MUHAMMAD YUFIAN PUTRA PRATAMA",
	"phoneNumber": "08111222333",
	"numberOfBills": "1",
	"billInfo": "UM-PTKIN",
	"billAmount": "205000",
	"billCode": "01",
	"totalAmount": "200000",
	"fee": "0",
	"narration": "",
	"transactionId": "%s",
	"paymentStatus": "PAID",
	"pin_transaksi": "12345",
	"accountNumber": "1231",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (transactionId, session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '64'
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
  assert resp.get('CustomerData').get('biaya_adm') != None
  assert resp.get('CustomerData').get('noRek') != None
  assert resp.get('CustomerData').get('nominal') != None
  assert resp.get('CustomerData').get('time') != None

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  transactionId = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"billerCode": "0026",
	"univCode": "30011",
	"billingNumber": "1234567890",
	"flexiField": "1",
	"univName": "UM PTKIN",
	"isRegistration": "N",
	"studentId": "1220277890",
	"studentName": "MUHAMMAD YUFIAN PUTRA PRATAMA",
	"phoneNumber": "08111222333",
	"numberOfBills": "1",
	"billInfo": "UM-PTKIN",
	"billAmount": "205000",
	"billCode": "01",
	"totalAmount": "205000",
	"fee": "0",
	"narration": "",
	"transactionId": "%s",
	"paymentStatus": "PAID",
	"pin_transaksi": "12345",
	"accountNumber": "1231",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703"
  }
  """ % (transactionId)
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
  transactionId = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"billerCode": "0026",
	"univCode": "30011",
	"billingNumber": "1234567890",
	"flexiField": "1",
	"univName": "UM PTKIN",
	"isRegistration": "N",
	"studentId": "1220277890",
	"studentName": "MUHAMMAD YUFIAN PUTRA PRATAMA",
	"phoneNumber": "08111222333",
	"numberOfBills": "1",
	"billInfo": "UM-PTKIN",
	"billAmount": "205000",
	"billCode": "01",
	"totalAmount": "205000",
	"fee": "0",
	"narration": "",
	"transactionId": "%s",
	"paymentStatus": "PAID",
	"pin_transaksi": "12345",
	"accountNumber": "1231",
    "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "ip_address": "10.70.9.44",
    "id_api": "web",
    "ip_server": "68",
    "req_id": "1595409493782703",
    "session": "%s"
  }
  """ % (transactionId, session)
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
  transactionId = time.strftime("%Y%m%d%H%M%S") + '050299'
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"billerCode": "0026",
	"univCode": "30011",
	"billingNumber": "1234567890",
	"flexiField": "1",
	"univName": "UM PTKIN",
	"isRegistration": "N",
	"studentId": "1220277890",
	"studentName": "MUHAMMAD YUFIAN PUTRA PRATAMA",
	"phoneNumber": "08111222333",
	"numberOfBills": "1",
	"billInfo": "UM-PTKIN",
	"billAmount": "205000",
	"billCode": "01",
	"totalAmount": "205000",
	"fee": "0",
	"narration": "",
	"transactionId": "%s",
	"paymentStatus": "PAID",
	"pin_transaksi": "12345",
	"accountNumber": "1231"
  }
  """ % (transactionId)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == True
  assert resp.get('errorNum') == '5006'
  assert resp.get('message') == 'Transaksi sudah dilakukan, mohon cek saldo rekening BNI dan laporan transaksi Anda. Apabila ingin mengulangi transaksi yang sama, silahkan tunggu 5 menit lagi'
