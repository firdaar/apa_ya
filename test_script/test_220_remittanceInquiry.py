import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/remittanceInquiry" % (IP_PORT)

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
	"refferenceNum": "S06MERC00134416 ",
	"counterAdvis": "ITR013441",
	"status": "0",
	"amountCurrency": "IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68",
	"session": "%s"
  }
  """ %(session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('coreJournal') != None
  assert resp.get('refferenceNum') != None
  assert resp.get('counterAdvis') != None
  assert resp.get('trxDate') != None
  assert resp.get('trxStatus') != None
  assert resp.get('remmAmount') != None
  assert resp.get('remmAmountCurrency') != None
  assert resp.get('remmAmountStr') != None
  assert resp.get('trxCharges') != None
  assert resp.get('refundCharge') != None
  assert resp.get('rateType') != None
  assert resp.get('beneficiaryName') != None
  assert resp.get('beneficiaryAddress') != None
  assert resp.get('senderName') != None
  assert resp.get('senderAddress') != None
  assert resp.get('nonSTPReason') != None
  assert resp.get('naration') != None
  assert resp.get('senderBank') != None
  assert resp.get('coveringBank') != None
  assert resp.get('coverRefference') != None
  assert resp.get('coverAccount') != None
  assert resp.get('branchNum') != None
  assert resp.get('debitAccountNum') != None
  assert resp.get('creditAccountNum') != None
  assert resp.get('chargeType') != None
  assert resp.get('amdCharges') != None
  assert resp.get('xtrCharges') != None
  assert resp.get('totTrxCharges') != None
  assert resp.get('totTrxChargesStr') != None
  assert resp.get('paymentCurrency') != None
  assert resp.get('creditAmount') != None
  assert resp.get('creditAmountStr') != None
  assert resp.get('paymentType') != None
  assert resp.get('errorNum') != None
  

  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
  "kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"refferenceNum": "S06MERC00134 ",
	"counterAdvis": "ITR013",
	"status": "0",
	"amountCurrency": "IDR",
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
  assert resp.get('errorNum') != None
  assert resp.get('message') != None

### TC Abnormal - Session Not Found ###
#######################################
def test_abnormal_session_not_found():
  post_data = """{
  "kode_mitra": "IPY",
	"kode_cabang": "014",
	"kode_loket": "00005",
	"refferenceNum": "S06MERC00134 ",
	"counterAdvis": "ITR013",
	"status": "0",
	"amountCurrency": "IDR",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
	"ip_server": "68",
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
	"refferenceNum": "S06MERC00134 ",
	"counterAdvis": "ITR013",
	"status": "0",
	"amountCurrency": "IDR",
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
	"refferenceNum": "S06MERC00134416 ",
	"counterAdvis": "ITR013441",
	"status": "0",
	"amountCurrency": "IDR"
  }
  """
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('coreJournal') != None
  assert resp.get('refferenceNum') != None
  assert resp.get('counterAdvis') != None
  assert resp.get('trxDate') != None
  assert resp.get('trxStatus') != None
  assert resp.get('remmAmount') != None
  assert resp.get('remmAmountCurrency') != None
  assert resp.get('remmAmountStr') != None
  assert resp.get('trxCharges') != None
  assert resp.get('refundCharge') != None
  assert resp.get('rateType') != None
  assert resp.get('beneficiaryName') != None
  assert resp.get('beneficiaryAddress') != None
  assert resp.get('senderName') != None
  assert resp.get('senderAddress') != None
  assert resp.get('nonSTPReason') != None
  assert resp.get('naration') != None
  assert resp.get('senderBank') != None
  assert resp.get('coveringBank') != None
  assert resp.get('coverRefference') != None
  assert resp.get('coverAccount') != None
  assert resp.get('branchNum') != None
  assert resp.get('debitAccountNum') != None
  assert resp.get('creditAccountNum') != None
  assert resp.get('chargeType') != None
  assert resp.get('amdCharges') != None
  assert resp.get('xtrCharges') != None
  assert resp.get('totTrxCharges') != None
  assert resp.get('totTrxChargesStr') != None
  assert resp.get('paymentCurrency') != None
  assert resp.get('creditAmount') != None
  assert resp.get('creditAmountStr') != None
  assert resp.get('paymentType') != None
  assert resp.get('errorNum') != None
