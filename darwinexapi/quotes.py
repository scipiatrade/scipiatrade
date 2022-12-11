import requests
import pandas as pd
import datetime
import common

__base_url = 'https://api.darwinex.com/quotes/1.0'
headers = {}

def get_quotes(products):
    url = __base_url + '/quotes'

    request_body = {
        'productNames': products
    }

    print(request_body)
    req = requests.post(url=url, headers=headers, json=request_body)

    status_code = req.status_code
    print(req)
    response_body = req.json()

    if status_code != 200:
        return common.not_successful(status_code, response_body)

    print(response_body)
    return None