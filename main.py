# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 09:07:08 2024

@author: fuwenyue
"""
import requests
import json
import time


gaode_key = ''

#获取全国范围内某详细地址的行政区域信息
def get_city(address, max_retries=3, delay=5):
    if not isinstance(address, str):
        return None, None, None

    address = address.split('#')[0]
    if not address:
        return None, None, None

    url = 'https://restapi.amap.com/v3/geocode/geo?address=' + address + f'&output=JSON&key={gaode_key}'
    
    for i in range(max_retries):
        try:
            request = requests.get(url).text
            result = json.loads(request)
            geocodes = result['geocodes']
            if len(geocodes) > 0:
                if geocodes[0]['district'] == []:
                    geocodes[0]['district'] = None
                if geocodes[0]['city'] == []:
                    geocodes[0]['city'] = None
                return geocodes[0]['province'], geocodes[0]['city'], geocodes[0]['district']
            else:
                return None, None, None
        except (requests.exceptions.RequestException, KeyError) as e:
            print(f"Error fetching data for address '{address}': {e}")
            if i < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to fetch data for address '{address}' after {max_retries} attempts")
                return None, None, None
