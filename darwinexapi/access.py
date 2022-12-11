import requests
import base64
import datetime

__access_token = 'fb3acec4-85b6-38d9-9944-19793d75a059'
__consumer_key = 'b7ERamM0uYuImSqDIelJGsNf7T0a'
__consumer_secret = 'T6fFtB6Yx5tkpaYWYMwomN3lzO8a'
__refresh_token = '40deabae-6e25-3691-a8a8-9fa15137ebae'
__request_time = datetime.datetime(2022, 12, 7, 16, 30, 00)
__expire_time = __request_time + datetime.timedelta(seconds = 3600)

def getAccessToken():
  return __access_token

def getExpireTime():
  return __expire_time

def refreshAccessToken():
  global __access_token
  global __refresh_token
  global __expire_time

  message = __consumer_key + ':' + __consumer_secret
  message_bytes = message.encode('ascii')
  base64_bytes = base64.b64encode(message_bytes)
  base64_message = base64_bytes.decode('ascii')
  url = 'https://api.darwinex.com/token?grant_type=refresh_token&refresh_token=' + __refresh_token
  config = {
      'Authorization': 'Basic ' + base64_message,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  req = requests.post(url, headers = config)
  if req.status_code == 200:
    req_json = req.json()
    __access_token = req_json['access_token']
    __refresh_token = req_json['refresh_token']
    __expire_time = datetime.datetime.now() + datetime.timedelta(seconds = req_json['expires_in'])
    return True
  else:
    print(req.json())
  
  return False