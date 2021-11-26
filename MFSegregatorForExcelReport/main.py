
import json
import requests
from MFTypes import mf_types,EQUITY,ELSS,DEBT


fundTypes={
  EQUITY:[],
  ELSS:[],
  DEBT:[]
}

PORTFOLIO_URI="https://coin.zerodha.com/api/dashboard_details"

HEADERS = dict({
  "cookie": "",
  "x-csrftoken":""
})




def parsePortfolio(response):
  try:
    for fund in response['data']['portfolio']:
      print(fund['scheme_name'])
      print(fund['net'])
      temp_fund={
        'scheme_name':fund['scheme_name'],
        'net': fund['net']
      }


      if mf_types[fund['scheme_name']]==EQUITY:
        fundTypes[EQUITY].append(temp_fund)
      elif mf_types[fund['scheme_name']]==ELSS:
        fundTypes[ELSS].append(temp_fund)
      elif mf_types[fund['scheme_name']]==DEBT:
        fundTypes[DEBT].append(temp_fund)
    

    print(":: Funds Totals ::\n")
    for fundType in fundTypes.keys():
      total=0
      print(":: " + fundType + " ::\n")
      for fund in fundTypes[fundType]:
        print(fund['scheme_name'] + " - " + str(fund["net"]))
        print()
        total+=fund['net']
        print()
      print(f'The total for the scheme type {fundType} is {total}')
      print()
  except Exception as e:
    print("!! Error in parsing the MF portfolio breakdown !!")
    print(e)
    # raise e
  finally:
    pass

  
  

def getMfBreakdown():
  try:
    print("::::::::::  Getting Portfolio :::::::::::::")
    print("::::::::::  Enter the session_token :::::::")
    session_token=input().strip()
    portfolio_uri_w_session_token=f'{PORTFOLIO_URI}?session_token={session_token}'
    print(f'Portfolio URI ========> {portfolio_uri_w_session_token}')
    portfolio = requests.get(portfolio_uri_w_session_token, headers=HEADERS)
    portfolio_json = portfolio.json()
    print(f'Session token validation :: {portfolio_json["status"]}')
    parsePortfolio(portfolio_json)

  except Exception as e:
    print("!! Error in getting the MF portfolio breakdown !!")
    print(e)
    # raise
  else:
    pass
  finally:
    print(":::::::::::::Completed::::::::::::::::")
    pass
  


getMfBreakdown()
