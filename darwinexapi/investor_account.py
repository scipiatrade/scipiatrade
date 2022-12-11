import requests
import pandas as pd
import common

__base_url = 'https://api.darwinex.com/investoraccountinfo/2.0'
headers = {}

class InvestorAccount:
    def __init__(self, id, available, available_to_invest, leverage, equity, open_pnl, invested, currency, max_risk, risk, name, manager = None, follower = None):
        self.id = id
        self.available = available
        self.available_to_invest = available_to_invest
        self.leverage = leverage
        self.equity = equity
        self.open_pnl = open_pnl
        self.invested = invested
        self.currency = currency
        self.max_risk = max_risk
        self.risk = risk
        self.name = name
        self.manager = manager
        self.follower = follower

    def can_invest(self, amount):
        return self.available_to_invest >= amount
    
    def get_leverage(self):
        return self.leverage

    def update_account(self):
        investor_account = _get_investoraccount(self.id)

        try:
            self.available = investor_account['available']
            self.available_to_invest = investor_account['availableToInvest']
            self.leverage = investor_account['leverage']
            self.equity = investor_account['equity']
            self.open_pnl = investor_account['openPnL']
            self.invested = investor_account['invested']
            self.currency = investor_account['currency']
            self.max_risk = investor_account['maxRisk']
            self.risk = investor_account['risk']
            self.name = investor_account['name']
        except:
            print('There was an error updating the selected investor account')
            return False
        
        return True

def _get_investoraccount(investor_account_id):
    url = __base_url + '/investoraccounts/' + str(investor_account_id)

    req = requests.get(url, headers=headers)
    
    status_code = req.status_code
    response_body = req.json()

    if status_code != 200:
        return common.not_successful(status_code, response_body)

    return response_body

def get_investoraccounts():
    url = __base_url + '/investoraccounts'

    req = requests.get(url, headers=headers)

    status_code = req.status_code
    response_body = req.json()

    if status_code != 200:
        return common.not_successful(status_code, response_body)
    
    columns = response_body[0].keys()
    investor_accounts = [ia for ia in response_body]

    return pd.DataFrame(investor_accounts, columns=columns)