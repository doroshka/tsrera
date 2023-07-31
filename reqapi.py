import time
import json
import requests

def getData(id):
    r = dict()
    r['is_ok'] = 1

    resp = requests.get('http://38.105.232.175:3001/api/0b06d7a7-a049-4739-be8e-8454ae90d638', params={'id': id})
    r['status_code'] = resp.status_code
    if resp.status_code != requests.codes.ok:
       r['is_ok'] = 0
       r['error'] = f"Api not accessible. Status code: [{resp.status_code}]"
       return r

    r['response'] = resp.json()
    if not r['response']['meta']['success']:
       r['is_ok'] = 0
       r['error'] = f"{r['response']['meta']['message']}"
       return r


    return r
