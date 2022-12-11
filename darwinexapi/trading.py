import requests
import common
import info

_base_url = 'https://api.darwinex.com/trading/1.1'
_minimum_amount = 200.0
headers = {}

class Trader:
    def __init__(self, investor_account):
        self.investor_account = investor_account

    def buy(self, amount, product_name, stop_loss, take_profit):
        if not info.get_productstatus(product_name, 'BUY'):
            print('BUY operation for product {} not allowed'.format(product_name))
            return None

        if amount < _minimum_amount:
            print('Minimum amount for any operation is {}'.format(_minimum_amount))
            return None

        if not self.investor_account.can_invest(amount):
            print('Requested amount ({}) is higher than the available to invest ({})'.format(amount, self.investor_account.available_to_invest))
            return None

        url = _base_url + '/investoraccounts/' + str(self.investor_account.id) + '/orders/buy'
        request_body = {
            'amount': amount,
            'productName': product_name,
            'thresholdParameters': {
                'quoteStopLoss': stop_loss,
                'quoteTakeProfit': take_profit
            }
        }

        req = requests.post(url, headers=headers, json=request_body)

        status_code = req.status_code
        response_body = req.json()

        if status_code != 200:
            return common.not_successful(status_code, response_body)

        print('Bought {} {}. SL: {}, TP: {}'.format(amount, product_name, stop_loss, take_profit))
        return None

    def sell(self, amount, product_name):
        if not info.get_productstatus(product_name, 'SELL'):
            print('SELL operation for product {} not allowed'.format(product_name))
            return None

        if amount < _minimum_amount:
            print('Minimum amount for any operation is {}'.format(_minimum_amount))

        url = _base_url + '/investoraccounts/' + str(self.investor_account.id) + '/orders/sell'
        request_body = {
            'amount': amount,
            'productName': product_name
        }

        req = requests.post(url, headers=headers, json=request_body)

        status_code = req.status_code
        response_body = req.json()

        if status_code != 200:
            return common.not_successful(status_code, response_body)

        print('Sold {} {}.'.format(amount, product_name))
        return None

    def update_leverage(self, new_leverage):
        url = _base_url + '/investoraccounts/' + str(self.investor_account.id) + '/leverage'

        request_body = {
            'leverage': new_leverage
        }

        req = requests.put(url, headers=headers, json=request_body)

        status_code = req.status_code
        response_body = req.json()

        if status_code != 200:
            return common.not_successful(status_code, response_body)

        self.investor_account.update_account()

        print('Leverage for investor account updated to {}'.format(new_leverage))
        return None