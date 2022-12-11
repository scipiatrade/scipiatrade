import requests
import pandas as pd
import datetime
import common

__base_url = 'https://api.darwinex.com/darwininfo/2.1'
headers = {}

def post_products():
    page_number = 0
    url = __base_url + '/products?status=ACTIVE'

    products = []
    columns = []
    first = True

    while True:
        body = {
            "filter": [
                {
                    "name": "divergence",
                    "options": [
                        {
                            "min": -0.5,
                            "period": "actual"
                        }
                    ]
                },
                {
                    "name": "d-score",
                    "options": [
                        {
                            "min": 65,
                            "period": "actual"
                        }
                    ]
                },
                {
                    "name": "trader_equity",
                    "options": [
                        {
                            "min": 10000.00,
                            "period": "actual"
                        }
                    ]
                },
                {
                    "name": "days_in_darwinex",
                    "options": [
                        {
                            "min": 730,
                            "period": "actual"
                        }
                    ]
                },
                {
                    "name": "return_drawdown",
                    "options": [
                        {
                            "min": 2,
                            "period": "2y"
                        }
                    ]
                },
                {
                    "name": "investors",
                    "options": [
                        {
                            "min": 5,
                            "period": "actual"
                        }
                    ]
                }
            ],
            "order": "ASC",
            "orderField": "productName",
            "page": page_number,
            "perPage": 100,
            "period": "1m"
        }

        req = requests.post(url, headers=headers, json = body)

        status_code = req.status_code
        response_body = req.json()

        if req.status_code != 200:
            common.not_successful(status_code, response_body)
            break
        
        page_number += 1

        if len(response_body) == 0:
            break

        for product in response_body:
            if first:
                first = False
                columns = product.keys()
            products.append([product[c] for c in columns])


    df_products = pd.DataFrame(products, columns=columns)
    df_products['quoteDate'] = df_products['quoteDate'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    return df_products
    

def get_candles(product_name, from_date, to_date, resolution = '1m'):
    valid_resolutions = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1mn']
    if resolution not in valid_resolutions:
        print('You must select a valid resolution. Valid resolutions:', valid_resolutions)
        return None
    
    try:
        from_date = datetime.datetime.strptime(from_date, '%d/%m/%Y %H:%M:%S')
    except:
        print('"From date" format is not valid (valid format is DD/MM/YYYY HH:mm:ss)')
        return None

    try:
        to_date = datetime.datetime.strptime(to_date, '%d/%m/%Y %H:%M:%S')
    except:
        print('"To date" format is not valid (valid format is DD/MM/YYYY HH:mm:ss)')
        return None
    
    if from_date > to_date:
        print('"From date" cannot be greater than "To date"')
        return None

    from_date = int(datetime.datetime.timestamp(from_date))
    to_date = int(datetime.datetime.timestamp(to_date))

    url = __base_url + '/products/' + product_name + '/candles?resolution=' + resolution +'&from=' + str(from_date) + '&to=' + str(to_date)
    req = requests.get(url, headers=headers)
    
    status_code = req.status_code
    response_body = req.json()

    if status_code != 200:
        return common.not_successful(status_code, response_body)

    response_candles = response_body['candles']

    columns = list(response_candles[0]['candle'].keys())
    columns.append('timestamp')
    candles = []

    for candle in response_candles:
        c = list([candle['candle'][c] for c in columns if c != 'timestamp'])
        c.append(candle['timestamp'])
        candles.append(c)

    df_candles = pd.DataFrame(candles, columns=columns)
    
    df_candles['timestamp'] = df_candles['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    return df_candles

def get_productstatus(product_name, operation = 'SELL'):

    operation = operation.upper()

    valid_operations = {
        'BUY': 'buyAllowed',
        'SELL': 'sellAllowed'
    }

    if operation not in valid_operations.keys():
        print('You must select a valid operation. Valid operations:', valid_operations)
        return None
        
    url = __base_url + '/products/' + product_name + '/status'

    req = requests.get(url, headers=headers)

    status_code = req.status_code
    response_body = req.json()

    if status_code != 200:
        if status_code != 404:
            return common.not_successful(status_code, response_body)
        return None
    
    return response_body[valid_operations[operation]]