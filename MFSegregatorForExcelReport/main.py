
import json
import MFTypes from './MFTypes.py'

f = open('MFSegregatorForExcelReport/input.json',)
response = json.load(f)


for trade in response['data']['portfolio']:
  print(trade['order_execution_time'], trade['quantity'], trade['price'])
  print()