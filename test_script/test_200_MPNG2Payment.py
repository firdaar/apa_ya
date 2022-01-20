import requests
import logging
import json
import os
import pytest
import time

logging.basicConfig(level=logging.DEBUG)

IP_PORT = os.getenv("IP_PORT", "10.70.152.25:3000")
USER = os.getenv("USER", "agen")

http_endpoint = "http://%s/MPNG2Payment" % (IP_PORT)

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
	  "kode_loket": "50299",
	  "kode_cabang": "259",
	  "ket": "Pembayaran MPN G2 - DJP",
	  "reffNum": "%s",
	  "h_billingId": "115030016764845",
	  "h_npwp": "021076427077000",
	  "h_nama": "NPWP DUMMY BADAN DUA",
	  "h_alamat": "JL.MESJID IV NO.19,JAKARTA UTARA",
	  "h_akun": "411122",
	  "h_kdJnsSetoran": "100",
	  "h_masaPajak": "03032014",
	  "h_nomorSK": "000000000000000",
	  "h_nop": "900019191818181778",
	  "h_jnsDokumen": "",
	  "h_nmrDokumen": "",
	  "h_tglDokumen": "",
	  "h_kdKpbc": "",
	  "h_kodeKL": "",
	  "h_unitEselon": "",
	  "h_kdSatker": "",
	  "h_currency": "IDR",
	  "c_adminBank": "0",
	  "h_tagihan": "1111111123",
	  "c_totalBayar": "1111111123",
	  "accountNum": "1231",
	  "pin_transaksi": "12345",
	  "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	  "ip_address": "10.70.9.199",
    "id_api":"web",
	  "ip_server": "68",
	  "req_id": "1568173118939741",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '122'
  assert resp.get('status') == 'success'
  assert resp.get('data') != None
  assert resp.get('data').get('error') == False
  assert resp.get('data').get('reffNum') != None
  assert resp.get('data').get('ket') != None
  assert resp.get('data').get('h_billingId') != None
  assert resp.get('data').get('h_npwp') != None
  assert resp.get('data').get('h_nama') != None
  assert resp.get('data').get('h_alamat') != None
  assert resp.get('data').get('h_akun') != None
  assert resp.get('data').get('h_kdJnsSetoran') != None
  assert resp.get('data').get('h_masaPajak') != None
  assert resp.get('data').get('h_nomorSK') != None
  assert resp.get('data').get('h_nop') != None
  assert resp.get('data').get('h_jnsDokumen') != None
  assert resp.get('data').get('h_nmrDokumen') != None
  assert resp.get('data').get('h_tglDokumen') != None
  assert resp.get('data').get('h_kdKpbc') != None
  assert resp.get('data').get('h_kodeKL') != None
  assert resp.get('data').get('h_unitEselonI') != None
  assert resp.get('data').get('h_kdSatker') != None
  assert resp.get('data').get('h_currency') != None
  assert resp.get('data').get('h_tagihan') != None
  assert resp.get('data').get('h_ntpn') != None
  assert resp.get('data').get('h_ntb') != None
  assert resp.get('data').get('stan') != None
  assert resp.get('data').get('tglBuku') != None
  assert resp.get('data').get('mataAnggaran') != None
  assert resp.get('data').get('nomorKttpn') != None
  assert resp.get('data').get('waktuTrx') != None
  assert resp.get('data').get('nmCabangTrx') != None
  assert resp.get('data').get('kdCabangTrx') != None
  assert resp.get('data').get('c_totalBayar') != None
  assert resp.get('data').get('nominalHuruf') != None
  assert resp.get('data').get('c_adminBank') != None
  assert resp.get('data').get('financialJournal') != None
  assert resp.get('data').get('errorNum') != None
  assert resp.get('result') != None
  assert resp.get('result').get('kode_loket') != None
  assert resp.get('result').get('kd_lkt') != None
  assert resp.get('result').get('nama') != None
  assert resp.get('result').get('kode_cabang') != None
  assert resp.get('result').get('kode_mitra') != None
  assert resp.get('result').get('alamat') != None
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
	"ket": "Pembayaran MPN G2 - DJP",
	"reffNum": "%s",
	"h_billingId": "115030016764845",
	"h_npwp": "021076427077000",
	"h_nama": "NPWP DUMMY BADAN DUA",
	"h_alamat": "JL.MESJID IV NO.19,JAKARTA UTARA",
	"h_akun": "411122",
	"h_kdJnsSetoran": "100",
	"h_masaPajak": "03032014",
	"h_nomorSK": "000000000000000",
	"h_nop": "900019191818181778",
	"h_jnsDokumen": "",
	"h_nmrDokumen": "",
	"h_tglDokumen": "",
	"h_kdKpbc": "",
	"h_kodeKL": "",
	"h_unitEselon": "",
	"h_kdSatker": "",
	"h_currency": "IDR",
	"c_adminBank": "0",
	"h_tagihan": "1111111123",
	"c_totalBayar": "1111111123",
	"accountNum": "1231",
	"pin_transaksi": "12345",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
  "id_api":"web",
	"ip_server": "68",
	"req_id": "1568173118939741",
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
  post_data = """{
    "kode_mitra": "BNI",
	  "kode_loket": "50299",
	  "kode_cabang": "259",
	  "ket": "Pembayaran MPN G2 - DJP",
	  "reffNum": "%s",
	  "h_billingId": "115030016764845",
	  "h_npwp": "021076427077000",
	  "h_nama": "NPWP DUMMY BADAN DUA",
	  "h_alamat": "JL.MESJID IV NO.19,JAKARTA UTARA",
	  "h_akun": "411122",
	  "h_kdJnsSetoran": "100",
	  "h_masaPajak": "03032014",
	  "h_nomorSK": "000000000000000",
	  "h_nop": "900019191818181778",
	  "h_jnsDokumen": "",
	  "h_nmrDokumen": "",
	  "h_tglDokumen": "",
	  "h_kdKpbc": "",
	  "h_kodeKL": "",
	  "h_unitEselon": "",
	  "h_kdSatker": "",
	  "h_currency": "IDR",
	  "c_adminBank": "0",
	  "h_tagihan": "11111111",
	  "c_totalBayar": "1111111123",
	  "accountNum": "1231",
	  "pin_transaksi": "125",
	  "browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	  "ip_address": "10.70.9.199",
    "id_api":"web",
	  "ip_server": "68",
	  "req_id": "1568173118939741",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '122'
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
	"kode_loket": "50299",
	"kode_cabang": "259",
	"ket": "Pembayaran MPN G2 - DJP",
	"reffNum": "%s",
	"h_billingId": "1150300",
	"h_npwp": "021076427077000",
	"h_nama": "NPWP DUMMY BADAN DUA",
	"h_alamat": "JL.MESJID IV NO.19,JAKARTA UTARA",
	"h_akun": "411122",
	"h_kdJnsSetoran": "100",
	"h_masaPajak": "03032014",
	"h_nomorSK": "000000000000000",
	"h_nop": "900019191818181778",
	"h_jnsDokumen": "",
	"h_nmrDokumen": "",
	"h_tglDokumen": "",
	"h_kdKpbc": "",
	"h_kodeKL": "",
	"h_unitEselon": "",
	"h_kdSatker": "",
	"h_currency": "IDR",
	"c_adminBank": "0",
	"h_tagihan": "1111111123",
	"c_totalBayar": "1111111123",
	"accountNum": "1231",
	"pin_transaksi": "12345",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
  "id_api":"web",
	"ip_server": "68",
	"req_id": "1568173118939741",
    "session": "%s"
  }
  """ % (reffNum,session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '122'
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
  post_data = """{
  "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"ket": "Pembayaran MPN G2 - DJP",
	"reffNum": "%s",
	"h_billingId": "115030016764845",
	"h_npwp": "021076427077000",
	"h_nama": "NPWP DUMMY BADAN DUA",
	"h_alamat": "JL.MESJID IV NO.19,JAKARTA UTARA",
	"h_akun": "411122",
	"h_kdJnsSetoran": "100",
	"h_masaPajak": "03032014",
	"h_nomorSK": "000000000000000",
	"h_nop": "900019191818181778",
	"h_jnsDokumen": "",
	"h_nmrDokumen": "",
	"h_tglDokumen": "",
	"h_kdKpbc": "",
	"h_kodeKL": "",
	"h_unitEselon": "",
	"h_kdSatker": "",
	"h_currency": "IDR",
	"c_adminBank": "0",
	"h_tagihan": "1111111123",
	"c_totalBayar": "1111111123",
	"accountNum": "1231",
	"pin_transaksi": "12345",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
  "id_api":"web",
	"ip_server": "68",
	"req_id": "1568173118939741"
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
  post_data = """{
    "kode_mitra": "BNI",
	"kode_loket": "50299",
	"kode_cabang": "259",
	"ket": "Pembayaran MPN G2 - DJP",
	"reffNum": "%s",
	"h_billingId": "115030016764845",
	"h_npwp": "021076427077000",
	"h_nama": "NPWP DUMMY BADAN DUA",
	"h_alamat": "JL.MESJID IV NO.19,JAKARTA UTARA",
	"h_akun": "411122",
	"h_kdJnsSetoran": "100",
	"h_masaPajak": "03032014",
	"h_nomorSK": "000000000000000",
	"h_nop": "900019191818181778",
	"h_jnsDokumen": "",
	"h_nmrDokumen": "",
	"h_tglDokumen": "",
	"h_kdKpbc": "",
	"h_kodeKL": "",
	"h_unitEselon": "",
	"h_kdSatker": "",
	"h_currency": "IDR",
	"c_adminBank": "0",
	"h_tagihan": "1111111123",
	"c_totalBayar": "1111111123",
	"accountNum": "1231",
	"pin_transaksi": "12345",
	"browser_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
	"ip_address": "10.70.9.199",
  "id_api":"web",
	"ip_server": "68",
	"req_id": "1568173118939741",
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
	  "kode_loket": "50299",
	  "kode_cabang": "259",
	  "ket": "Pembayaran MPN G2 - DJP",
	  "reffNum": "%s",
	  "h_billingId": "115030016764845",
	  "h_npwp": "021076427077000",
	  "h_nama": "NPWP DUMMY BADAN DUA",
	  "h_alamat": "JL.MESJID IV NO.19,JAKARTA UTARA",
	  "h_akun": "411122",
	  "h_kdJnsSetoran": "100",
	  "h_masaPajak": "03032014",
	  "h_nomorSK": "000000000000000",
	  "h_nop": "900019191818181778",
	  "h_jnsDokumen": "",
	  "h_nmrDokumen": "",
	  "h_tglDokumen": "",
	  "h_kdKpbc": "",
	  "h_kodeKL": "",
	  "h_unitEselon": "",
	  "h_kdSatker": "",
	  "h_currency": "IDR",
	  "c_adminBank": "0",
	  "h_tagihan": "1111111123",
	  "c_totalBayar": "1111111123",
	  "accountNum": "1231",
	  "pin_transaksi": "12345"
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
