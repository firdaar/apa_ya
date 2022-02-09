import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/remittancePayment" % (IP_PORT)

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
	"kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"pin_transaksi": "12345",
	"reffCorrespondent": "1600004111",
	"refferenceNum": "S06MERC00134416",
	"counterAdvis": "ITR013441",
	"remmAmount": "4808484.000",
	"remmAmountCurrency": "IDR",
	"trxCharges": "0",
	"refundCharge": "50.000",
	"creditAmount": "4808424.000",
	"creditAmountCurrency": "IDR",
	"baseAmount": "4808424.000",
	"creditAccountNum": 4447,
	"rateType": "03",
	"amdCharges": "0",
	"xtrCharges": "60.000",
	"senderName": "ALI HARYANTO",
	"senderAddress": "12 JALAN SUNGAI HUTAN MELINTANG PER",
	"senderBank": "MERCHANTRADE ASIA SDN.BHD",
	"naration": "",
	"beneficiaryName": "ALI AMI",
	"beneficiaryAddress": "INDONESIA 62808114411",
	"paymentType": "Tunai",
	"paymentCurrency": "IDR/Rupiah",
	"totTrxChargesStr": "60 - IDR",
	"totTrxChargesS": "60.000",
	"remmAmountStr": "4.808.484 - IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68",
	"session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error')==False
  assert resp.get('ket')!= None
  assert resp.get('coreJournal')!= None
  assert resp.get('refferenceNum')!= None
  assert resp.get('reffCorrespondent')!= None
  assert resp.get('senderName')!= None
  assert resp.get('senderAddress')!= None
  assert resp.get('senderBank')!= None
  assert resp.get('naration')!= None
  assert resp.get('beneficiaryName')!= None
  assert resp.get('beneficiaryAddress')!= None
  assert resp.get('paymentType')!= None
  assert resp.get('paymentCurrency')!= None
  assert resp.get('remmAmountStr')!= None
  assert resp.get('totTrxChargesStr')!= None
  assert resp.get('creditAmount')!= None
  assert resp.get('errorNum')!= None


### TC Abnormal - Transaction Already Done ###
##############################################
def test_abnormal_already_done():
  session = login_user("agen")
  post_data = """{
	"kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"pin_transaksi": "12345",
	"reffCorrespondent": "1600004111",
	"refferenceNum": "S06MERC00134416",
	"counterAdvis": "ITR013441",
	"remmAmount": "4808484.000",
	"remmAmountCurrency": "IDR",
	"trxCharges": "0",
	"refundCharge": "50.000",
	"creditAmount": "4808424.000",
	"creditAmountCurrency": "IDR",
	"baseAmount": "4808424.000",
	"creditAccountNum": 4447,
	"rateType": "03",
	"amdCharges": "0",
	"xtrCharges": "60.000",
	"senderName": "ALI HARYANTO",
	"senderAddress": "12 JALAN SUNGAI HUTAN MELINTANG PER",
	"senderBank": "MERCHANTRADE ASIA SDN.BHD",
	"naration": "",
	"beneficiaryName": "ALI AMI",
	"beneficiaryAddress": "INDONESIA 62808114411",
	"paymentType": "Tunai",
	"paymentCurrency": "IDR/Rupiah",
	"totTrxChargesStr": "60 - IDR",
	"totTrxChargesS": "60.000",
	"remmAmountStr": "4.808.484 - IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68",
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
	"kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"pin_transaksi": "12",
	"reffCorrespondent": "1600004111",
	"refferenceNum": "S06MERC00134416",
	"counterAdvis": "ITR013441",
	"remmAmount": "4808484.000",
	"remmAmountCurrency": "IDR",
	"trxCharges": "0",
	"refundCharge": "50.00",
	"creditAmount": "4808424.00",
	"creditAmountCurrency": "IDR",
	"baseAmount": "4808424.000",
	"creditAccountNum": 4447,
	"rateType": "03",
	"amdCharges": "0",
	"xtrCharges": "60.000",
	"senderName": "ALI HARYANTO",
	"senderAddress": "12 JALAN SUNGAI HUTAN MELINTANG PER",
	"senderBank": "MERCHANTRADE ASIA SDN.BHD",
	"naration": "",
	"beneficiaryName": "ALI AMI",
	"beneficiaryAddress": "INDONESIA 62808114411",
	"paymentType": "Tunai",
	"paymentCurrency": "IDR/Rupiah",
	"totTrxChargesStr": "60 - IDR",
	"totTrxChargesS": "60.000",
	"remmAmountStr": "4.808.484 - IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '401'
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
  assert resp.get('CustomerData') != None
  assert resp.get('CustomerData').get('time') != None
  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
	"kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"pin_transaksi": "12345",
	"reffCorrespondent": "1600004",
	"refferenceNum": "S06MERC00116",
	"counterAdvis": "ITR013441",
	"remmAmount": "4808484.000",
	"remmAmountCurrency": "IDR",
	"trxCharges": "0",
	"refundCharge": "50.000",
	"creditAmount": "4808424.000",
	"creditAmountCurrency": "IDR",
	"baseAmount": "4808424.000",
	"creditAccountNum": 4447,
	"rateType": "03",
	"amdCharges": "0",
	"xtrCharges": "60.000",
	"senderName": "ALI HARYANTO",
	"senderAddress": "12 JALAN SUNGAI HUTAN MELINTANG PER",
	"senderBank": "MERCHANTRADE ASIA SDN.BHD",
	"naration": "",
	"beneficiaryName": "ALI AMI",
	"beneficiaryAddress": "INDONESIA 62808114411",
	"paymentType": "Tunai",
	"paymentCurrency": "IDR/Rupiah",
	"totTrxChargesStr": "60 - IDR",
	"totTrxChargesS": "60.000",
	"remmAmountStr": "4.808.484 - IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '401'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == True
  assert resp.get('data').get('errorNum') != None
  assert resp.get('data').get('message') != None
  assert resp.get('data').get('ori_errorNum')!=None
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
  post_data = """{
	"kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"pin_transaksi": "12345",
	"reffCorrespondent": "1600004111",
	"refferenceNum": "S06MERC00134416",
	"counterAdvis": "ITR013441",
	"remmAmount": "4808484.000",
	"remmAmountCurrency": "IDR",
	"trxCharges": "0",
	"refundCharge": "50.000",
	"creditAmount": "4808424.000",
	"creditAmountCurrency": "IDR",
	"baseAmount": "4808424.000",
	"creditAccountNum": 4447,
	"rateType": "03",
	"amdCharges": "0",
	"xtrCharges": "60.000",
	"senderName": "ALI HARYANTO",
	"senderAddress": "12 JALAN SUNGAI HUTAN MELINTANG PER",
	"senderBank": "MERCHANTRADE ASIA SDN.BHD",
	"naration": "",
	"beneficiaryName": "ALI AMI",
	"beneficiaryAddress": "INDONESIA 62808114411",
	"paymentType": "Tunai",
	"paymentCurrency": "IDR/Rupiah",
	"totTrxChargesStr": "60 - IDR",
	"totTrxChargesS": "60.000",
	"remmAmountStr": "4.808.484 - IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68"
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
	"kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"pin_transaksi": "12345",
	"reffCorrespondent": "1600004111",
	"refferenceNum": "S06MERC00134416",
	"counterAdvis": "ITR013441",
	"remmAmount": "4808484.000",
	"remmAmountCurrency": "IDR",
	"trxCharges": "0",
	"refundCharge": "50.000",
	"creditAmount": "4808424.000",
	"creditAmountCurrency": "IDR",
	"baseAmount": "4808424.000",
	"creditAccountNum": 4447,
	"rateType": "03",
	"amdCharges": "0",
	"xtrCharges": "60.000",
	"senderName": "ALI HARYANTO",
	"senderAddress": "12 JALAN SUNGAI HUTAN MELINTANG PER",
	"senderBank": "MERCHANTRADE ASIA SDN.BHD",
	"naration": "",
	"beneficiaryName": "ALI AMI",
	"beneficiaryAddress": "INDONESIA 62808114411",
	"paymentType": "Tunai",
	"paymentCurrency": "IDR/Rupiah",
	"totTrxChargesStr": "60 - IDR",
	"totTrxChargesS": "60.000",
	"remmAmountStr": "4.808.484 - IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68",
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
	"kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"pin_transaksi": "12345",
	"reffCorrespondent": "1600004111",
	"refferenceNum": "S06MERC00134416",
	"counterAdvis": "ITR013441",
	"remmAmount": "4808484.000",
	"remmAmountCurrency": "IDR",
	"trxCharges": "0",
	"refundCharge": "50.000",
	"creditAmount": "4808424.000",
	"creditAmountCurrency": "IDR",
	"baseAmount": "4808424.000",
	"creditAccountNum": 4447,
	"rateType": "03",
	"amdCharges": "0",
	"xtrCharges": "60.000",
	"senderName": "ALI HARYANTO",
	"senderAddress": "12 JALAN SUNGAI HUTAN MELINTANG PER",
	"senderBank": "MERCHANTRADE ASIA SDN.BHD",
	"naration": "",
	"beneficiaryName": "ALI AMI",
	"beneficiaryAddress": "INDONESIA 62808114411",
	"paymentType": "Tunai",
	"paymentCurrency": "IDR/Rupiah",
	"totTrxChargesStr": "60 - IDR",
	"totTrxChargesS": "60.000",
	"remmAmountStr": "4.808.484 - IDR"
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
