import streamlit as st
import time
import json
import requests

def getData(id):
    r = dict()
    r['is_ok'] = 1

    resp = requests.get(st.secrets['server'], params={'id': id})
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
