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
    "kode_mitra": "BNI",
    "kode_cabang": "259",
    "kode_loket": "50299",
    "ket": "SAMSAT DIGITAL NASIONAL",
    "reffNum": "20210913102201050299",
    "paymentCode": "123456789012345678",
    "customerIdCardNumber": "1234567890123456",
    "adminBank": "000010000",
    "languageCode": "0",
    "nomorRangka": "98765432",
    "nomorMesin": "",
    "namaPemilik": "I PUTU MEGA SUMANTARA",
    "alamatPemilik": "",
    "nomorPolisi": "DK279FF",
    "warnaPlat": "MERAH",
    "milikKenamaa": "001",
    "jenisKendaraan": "MBL.SEDAN/SEJEN",
    "namaMerekKB": "HONDA",
    "namaModelKB": "SEDAN",
    "tahunBuatan": "1992",
    "tanggalAkhirPajakLama": "20150730",
    "tanggalAkhirPajakBaru": "20180730",
    "pokokBBN": "000000000000",
    "dendaBBN": "000000000000",
    "pokokPKB": "000000200000",
    "dendaPKB": "000000000000",
    "pokokSWD": "000000200000",
    "dendaSWD": "000000000000",
    "PNBP": "000000050000",
    "pokokAdminTNKB": "000000000000",
    "jumlah": "000000457500",
    "keteranganNamaSamsat": "DIGITAL NASIONAL",
    "keteranganTanggalBerlaku": "03102021",
    "keteranganLain": "",
    "reserved_01": "12345",
    "NTP": "NTP030500001111",
    "amount": "250000",
    "accountNum": "1231",
    "pin_transaksi": "12345",
	"session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
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


### TC Abnormal - Transaction Already Done ###
##############################################
def test_abnormal_already_done():
  session = login_user("agen")
  post_data = """{
    "kode_mitra": "BNI",
    "kode_cabang": "259",
    "kode_loket": "50299",
    "ket": "SAMSAT DIGITAL NASIONAL",
    "reffNum": "20210913102201050299",
    "paymentCode": "123456789012345678",
    "customerIdCardNumber": "1234567890123456",
    "adminBank": "000010000",
    "languageCode": "0",
    "nomorRangka": "98765432",
    "nomorMesin": "",
    "namaPemilik": "I PUTU MEGA SUMANTARA",
    "alamatPemilik": "",
    "nomorPolisi": "DK279FF",
    "warnaPlat": "MERAH",
    "milikKenamaa": "001",
    "jenisKendaraan": "MBL.SEDAN/SEJEN",
    "namaMerekKB": "HONDA",
    "namaModelKB": "SEDAN",
    "tahunBuatan": "1992",
    "tanggalAkhirPajakLama": "20150730",
    "tanggalAkhirPajakBaru": "20180730",
    "pokokBBN": "000000000000",
    "dendaBBN": "000000000000",
    "pokokPKB": "000000200000",
    "dendaPKB": "000000000000",
    "pokokSWD": "000000200000",
    "dendaSWD": "000000000000",
    "PNBP": "000000050000",
    "pokokAdminTNKB": "000000000000",
    "jumlah": "000000457500",
    "keteranganNamaSamsat": "DIGITAL NASIONAL",
    "keteranganTanggalBerlaku": "03102021",
    "keteranganLain": "",
    "reserved_01": "12345",
    "NTP": "NTP030500001111",
    "amount": "250000",
    "accountNum": "1231",
    "pin_transaksi": "12345",
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
    "ket": "SAMSAT DIGITAL NASIONAL",
    "reffNum": "20210913102201050299",
    "paymentCode": "123456789012345678",
    "customerIdCardNumber": "1234567890123456",
    "adminBank": "000010000",
    "languageCode": "0",
    "nomorRangka": "98765432",
    "nomorMesin": "",
    "namaPemilik": "I PUTU MEGA SUMANTARA",
    "alamatPemilik": "",
    "nomorPolisi": "DK279FF",
    "warnaPlat": "MERAH",
    "milikKenamaa": "001",
    "jenisKendaraan": "MBL.SEDAN/SEJEN",
    "namaMerekKB": "HONDA",
    "namaModelKB": "SEDAN",
    "tahunBuatan": "1992",
    "tanggalAkhirPajakLama": "20150730",
    "tanggalAkhirPajakBaru": "20180730",
    "pokokBBN": "000000000000",
    "dendaBBN": "000000000000",
    "pokokPKB": "000000200000",
    "dendaPKB": "000000000000",
    "pokokSWD": "000000200000",
    "dendaSWD": "000000000000",
    "PNBP": "000000050000",
    "pokokAdminTNKB": "000000000000",
    "jumlah": "000000457500",
    "keteranganNamaSamsat": "DIGITAL NASIONAL",
    "keteranganTanggalBerlaku": "03102021",
    "keteranganLain": "",
    "reserved_01": "12345",
    "NTP": "NTP030500001111",
    "amount": "250000",
    "accountNum": "1231",
    "pin_transaksi": "145",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  print(resp)
  assert resp.get('trxType') == '71'
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
    "ket": "SAMSAT DIGITAL NASIONAL",
    "reffNum": "20210913102201050299",
    "paymentCode": "123456789012345678",
    "customerIdCardNumber": "123456789012356",
    "adminBank": "000010000",
    "languageCode": "0",
    "nomorRangka": "98765432",
    "nomorMesin": "",
    "namaPemilik": "I PUTU MEGA SUMANTARA",
    "alamatPemilik": "",
    "nomorPolisi": "DK279FF",
    "warnaPlat": "MERAH",
    "milikKenamaa": "001",
    "jenisKendaraan": "MBL.SEDAN/SEJEN",
    "namaMerekKB": "HONDA",
    "namaModelKB": "SEDAN",
    "tahunBuatan": "1992",
    "tanggalAkhirPajakLama": "20150730",
    "tanggalAkhirPajakBaru": "20180730",
    "pokokBBN": "000000000000",
    "dendaBBN": "000000000000",
    "pokokPKB": "000000200000",
    "dendaPKB": "000000000000",
    "pokokSWD": "000000200000",
    "dendaSWD": "000000000000",
    "PNBP": "000000050000",
    "pokokAdminTNKB": "000000000000",
    "jumlah": "000000457500",
    "keteranganNamaSamsat": "DIGITAL NASIONAL",
    "keteranganTanggalBerlaku": "03102021",
    "keteranganLain": "",
    "reserved_01": "12345",
    "NTP": "NTP030500001111",
    "amount": "250000",
    "accountNum": "1231",
    "pin_transaksi": "12345",
    "session": "%s"
  }
  """ % (session)
  logging.debug(post_data)
  logging.debug(http_endpoint)
  req = requests.post(http_endpoint, json=json.loads(post_data))
  resp = req.json()
  logging.debug(resp)
  assert resp.get('trxType') == '71'
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
    "kode_mitra": "BNI",
    "kode_cabang": "259",
    "kode_loket": "50299",
    "ket": "SAMSAT DIGITAL NASIONAL",
    "reffNum": "20210913102201050299",
    "paymentCode": "123456789012345678",
    "customerIdCardNumber": "1234567890123456",
    "adminBank": "000010000",
    "languageCode": "0",
    "nomorRangka": "98765432",
    "nomorMesin": "",
    "namaPemilik": "I PUTU MEGA SUMANTARA",
    "alamatPemilik": "",
    "nomorPolisi": "DK279FF",
    "warnaPlat": "MERAH",
    "milikKenamaa": "001",
    "jenisKendaraan": "MBL.SEDAN/SEJEN",
    "namaMerekKB": "HONDA",
    "namaModelKB": "SEDAN",
    "tahunBuatan": "1992",
    "tanggalAkhirPajakLama": "20150730",
    "tanggalAkhirPajakBaru": "20180730",
    "pokokBBN": "000000000000",
    "dendaBBN": "000000000000",
    "pokokPKB": "000000200000",
    "dendaPKB": "000000000000",
    "pokokSWD": "000000200000",
    "dendaSWD": "000000000000",
    "PNBP": "000000050000",
    "pokokAdminTNKB": "000000000000",
    "jumlah": "000000457500",
    "keteranganNamaSamsat": "DIGITAL NASIONAL",
    "keteranganTanggalBerlaku": "03102021",
    "keteranganLain": "",
    "reserved_01": "12345",
    "NTP": "NTP030500001111",
    "amount": "250000",
    "accountNum": "1231",
    "pin_transaksi": "12345",
	"browser_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"ip_address": "127.0.0.1",
	"id_api": "web"
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
    "ket": "SAMSAT DIGITAL NASIONAL",
    "reffNum": "20210913102201050299",
    "paymentCode": "123456789012345678",
    "customerIdCardNumber": "1234567890123456",
    "adminBank": "000010000",
    "languageCode": "0",
    "nomorRangka": "98765432",
    "nomorMesin": "",
    "namaPemilik": "I PUTU MEGA SUMANTARA",
    "alamatPemilik": "",
    "nomorPolisi": "DK279FF",
    "warnaPlat": "MERAH",
    "milikKenamaa": "001",
    "jenisKendaraan": "MBL.SEDAN/SEJEN",
    "namaMerekKB": "HONDA",
    "namaModelKB": "SEDAN",
    "tahunBuatan": "1992",
    "tanggalAkhirPajakLama": "20150730",
    "tanggalAkhirPajakBaru": "20180730",
    "pokokBBN": "000000000000",
    "dendaBBN": "000000000000",
    "pokokPKB": "000000200000",
    "dendaPKB": "000000000000",
    "pokokSWD": "000000200000",
    "dendaSWD": "000000000000",
    "PNBP": "000000050000",
    "pokokAdminTNKB": "000000000000",
    "jumlah": "000000457500",
    "keteranganNamaSamsat": "DIGITAL NASIONAL",
    "keteranganTanggalBerlaku": "03102021",
    "keteranganLain": "",
    "reserved_01": "12345",
    "NTP": "NTP030500001111",
    "amount": "250000",
    "accountNum": "1231",
    "pin_transaksi": "12345",
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
    "kode_mitra": "BNI",
    "kode_cabang": "259",
    "kode_loket": "50299",
    "ket": "SAMSAT DIGITAL NASIONAL",
    "reffNum": "20210913102201050299",
    "paymentCode": "123456789012345678",
    "customerIdCardNumber": "1234567890123456",
    "adminBank": "000010000",
    "languageCode": "0",
    "nomorRangka": "98765432",
    "nomorMesin": "",
    "namaPemilik": "I PUTU MEGA SUMANTARA",
    "alamatPemilik": "",
    "nomorPolisi": "DK279FF",
    "warnaPlat": "MERAH",
    "milikKenamaa": "001",
    "jenisKendaraan": "MBL.SEDAN/SEJEN",
    "namaMerekKB": "HONDA",
    "namaModelKB": "SEDAN",
    "tahunBuatan": "1992",
    "tanggalAkhirPajakLama": "20150730",
    "tanggalAkhirPajakBaru": "20180730",
    "pokokBBN": "000000000000",
    "dendaBBN": "000000000000",
    "pokokPKB": "000000200000",
    "dendaPKB": "000000000000",
    "pokokSWD": "000000200000",
    "dendaSWD": "000000000000",
    "PNBP": "000000050000",
    "pokokAdminTNKB": "000000000000",
    "jumlah": "000000457500",
    "keteranganNamaSamsat": "DIGITAL NASIONAL",
    "keteranganTanggalBerlaku": "03102021",
    "keteranganLain": "",
    "reserved_01": "12345",
    "NTP": "NTP030500001111",
    "amount": "250000",
    "accountNum": "1231",
    "pin_transaksi": "12345"
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
