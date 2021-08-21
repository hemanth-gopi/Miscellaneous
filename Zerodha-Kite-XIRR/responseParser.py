import json


f = open('Zerodha-Kite-XIRR/responseInput.json',)
response = json.load(f)


for trade in response['data']['result']:
  print(trade['order_execution_time'], trade['quantity'], trade['price'])
  print()