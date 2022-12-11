import datetime

import info
import quotes
import trading
import investor_account
import access

remaining_token_time = int((datetime.datetime.now() - access.getExpireTime()).total_seconds())

if remaining_token_time >= 0:
    print('Token is outdated, ending execution')
    exit()

if remaining_token_time >= -900:
    print(str(remaining_token_time) + ' seconds remaining, refreshing access token')
    if access.refreshAccessToken():
        print('Access token refreshed')           
    else:
        print('Access token could not be refreshed, exiting')
        exit()
else:
    print(str(remaining_token_time) + ' seconds remaining, no need to refresh the access token')

headers = {
        'accepts': 'application/json',
        'Authorization': 'Bearer ' + access.getAccessToken()
    }
info.headers = headers
investor_account.headers = headers
trading.headers = headers
quotes.headers = headers

############ INFO
products = info.post_products()
print(products.head())
print('{} products retrieved.'.format(len(products)))

test_product = products.iloc[0]['productName']
#candles = info.get_candles(test_product, from_date = '23/11/2022 00:00:00', to_date = '24/11/2022 00:00:00')
#print(candles.head())
#print('{} candles retrieved.'.format(len(candles)))

#print(info.get_productstatus(test_product, 'BUY'))

########### INVESTOR_ACCOUNT

investor_accounts = investor_account.get_investoraccounts()
#print(investor_accounts.head())

investorAccount = investor_account.InvestorAccount(
    investor_accounts.iloc[0]['id'],
    investor_accounts.iloc[0]['available'],
    investor_accounts.iloc[0]['availableToInvest'],
    investor_accounts.iloc[0]['leverage'],
    investor_accounts.iloc[0]['equity'],
    investor_accounts.iloc[0]['openPnL'],
    investor_accounts.iloc[0]['invested'],
    investor_accounts.iloc[0]['currency'],
    investor_accounts.iloc[0]['maxRisk'],
    investor_accounts.iloc[0]['risk'],
    investor_accounts.iloc[0]['name']
)

investorAccount.update_account()

trader = trading.Trader(investorAccount)
#trader.update_leverage(3)
#trader.buy(400, test_product, 10, 400)
#trader.sell(200, test_product)

quotes.get_quotes(['BLM.5.10'])