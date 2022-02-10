import re
import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/samsatInquiry" % (IP_PORT)

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

reffNum = time.strftime("%Y%m%d%H%M%S") + '050299'
### TC Normal ###
#################
def test_normal():
  session = login_user("agen")
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"paymentCode": "123456789012345678",
	"customerIdCardNumber": "1234567890123456",
	"session": "%s"
  }
  """ %(reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('reffNum') != None
  assert resp.get('paymentCode') != None
  assert resp.get('customerIdCardNumber') != None
  assert resp.get('adminBank') != None
  assert resp.get('languageCode') != None
  assert resp.get('nomorRangka') != None
  assert resp.get('nomorMesin') != None
  assert resp.get('namaPemilik') != None
  assert resp.get('alamatPemilik') != None
  assert resp.get('nomorPolisi') != None
  assert resp.get('warnaPlat') != None
  assert resp.get('jenisKendaraan') != None
  assert resp.get('namaMerekKB') != None
  assert resp.get('namaModelKB') != None
  assert resp.get('tahunBuatan') != None
  assert resp.get('tanggalAkhirPajakLama') != None
  assert resp.get('tanggalAkhirPajakBaru') != None
  assert resp.get('pokokBBN') != None
  assert resp.get('dendaBBN') != None
  assert resp.get('pokokPKB') != None
  assert resp.get('dendaPKB') != None
  assert resp.get('pokokSWD') != None
  assert resp.get('dendaSWD') != None
  assert resp.get('PNBP') != None
  assert resp.get('pokokAdminTNKB') != None
  assert resp.get('jumlah') != None
  assert resp.get('keteranganNamaSamsat') != None
  assert resp.get('keteranganTanggalBerlaku') != None
  assert resp.get('keteranganLain') != None
  assert resp.get('reserved_01') != None
  assert resp.get('NTP') != None
  assert resp.get('amount') != None
  
  
### TC Abnormal - Error SOA ###
###############################
def test_abnormal_error_soa():
  session = login_user("agen")
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "20210913092201050299",
	"paymentCode": "123456789012345678",
	"customerIdCardNumber": "1234567890123456",
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
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"paymentCode": "123456789012345678",
	"customerIdCardNumber": "1234567890123456",
    "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web"
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
  session = "12345"
  post_data = """{
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"paymentCode": "123456789012345678",
	"customerIdCardNumber": "1234567890123456",
    "browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web",
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
	"kode_mitra": "BNI",
	"kode_cabang": "259",
	"kode_loket": "50299",
	"reffNum": "%s",
	"paymentCode": "123456789012345678",
	"customerIdCardNumber": "1234567890123456"
  }
  """%(reffNum)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('error') == False
  assert resp.get('ket') != None
  assert resp.get('reffNum') != None
  assert resp.get('paymentCode') != None
  assert resp.get('customerIdCardNumber') != None
  assert resp.get('adminBank') != None
  assert resp.get('languageCode') != None
  assert resp.get('nomorRangka') != None
  assert resp.get('nomorMesin') != None
  assert resp.get('namaPemilik') != None
  assert resp.get('alamatPemilik') != None
  assert resp.get('nomorPolisi') != None
  assert resp.get('warnaPlat') != None
  assert resp.get('jenisKendaraan') != None
  assert resp.get('namaMerekKB') != None
  assert resp.get('namaModelKB') != None
  assert resp.get('tahunBuatan') != None
  assert resp.get('tanggalAkhirPajakLama') != None
  assert resp.get('tanggalAkhirPajakBaru') != None
  assert resp.get('pokokBBN') != None
  assert resp.get('dendaBBN') != None
  assert resp.get('pokokPKB') != None
  assert resp.get('dendaPKB') != None
  assert resp.get('pokokSWD') != None
  assert resp.get('dendaSWD') != None
  assert resp.get('PNBP') != None
  assert resp.get('pokokAdminTNKB') != None
  assert resp.get('jumlah') != None
  assert resp.get('keteranganNamaSamsat') != None
  assert resp.get('keteranganTanggalBerlaku') != None
  assert resp.get('keteranganLain') != None
  assert resp.get('reserved_01') != None
  assert resp.get('NTP') != None
  assert resp.get('amount') != None