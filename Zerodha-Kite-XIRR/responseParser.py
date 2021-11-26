import requests
import datetime
from utils import getInstrumentsIdsFromEquities, xirr, getPortfolioValue

ZERODHA_CONSOLE_API_BASE="https://console.zerodha.com/api/reports/holdings"

PORTFOLIO="/portfolio"
BREAKDOWN="/breakdown"

TODAY_DATE = datetime.date.today()
GET_PORTOLIO_URI = ZERODHA_CONSOLE_API_BASE + PORTFOLIO + "?date=" + str(TODAY_DATE)

HEADERS = dict({
  "cookie": "",
  "x-csrftoken":""
})

def calculateXIRR():

  print("::::::::::  Getting Portfolio :::::::::::::")
  print(f'Portfolio URI ========> {GET_PORTOLIO_URI}')
  portfolio = requests.get(GET_PORTOLIO_URI, headers=HEADERS)
  print(portfolio.json()['status'])

  equities = portfolio.json()['data']['result']['eq']
  print(len(equities))
  instrument_ids = map(getInstrumentsIdsFromEquities, equities)
  total_portfolio_value = sum(list(map(getPortfolioValue, equities)))
  instrument_ids = list(instrument_ids)

  print(f'\nInstrument IDS  =============> {instrument_ids}')

  trade_log= {}
  tas=[]
  for instrument_id in instrument_ids:
    GET_BREAKDOWN_URI = ZERODHA_CONSOLE_API_BASE +BREAKDOWN + "?instrument_id=" + instrument_id + "&segment=EQ"

    breakdown = requests.get(GET_BREAKDOWN_URI, headers=HEADERS)
    breakdown= breakdown.json()['data']['result']
    for segment in breakdown:
      inflow_date = segment['order_execution_time'].split("T")[0]
      amount = segment['price']*segment["quantity"]
      print(f'{segment["tradingsymbol"]} =====> {amount} :: {inflow_date}')
      days = TODAY_DATE-datetime.datetime.strptime(inflow_date, "%Y-%m-%d").date()

      if segment['tradingsymbol'] not in trade_log.keys():
        trade_log[segment['tradingsymbol']]=[]

      trade_log[segment['tradingsymbol']].append(dict({
        "days":days,
        "price":segment['price'],
        "quantity": segment["quantity"]
      }))
      
      tas.append((datetime.datetime.strptime(inflow_date, "%Y-%m-%d").date(), -amount))

  # for key in trade_log.keys():
  #   print(trade_log[key])

  tas.append((TODAY_DATE, total_portfolio_value))
  for tax in tas:
    print(f'{tax[0]},{tax[1]}')
  print(xirr(tas))


# Checking whether XIRR calculation is correct or not
# The following values correspond to 10% CAGR
# tas2=[
#   (datetime.datetime.strptime("2019-01-01", "%Y-%m-%d").date(),-1000),
#   (datetime.datetime.strptime("2020-01-01", "%Y-%m-%d").date(),-1000),(datetime.datetime.strptime("2021-01-01", "%Y-%m-%d").date(),2310)]


# print(xirr(tas2)*100)


calculateXIRR()