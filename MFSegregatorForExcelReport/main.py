
import json
import requests
from MFTypes import mf_types,EQUITY,ELSS,DEBT


fundTypes={
  EQUITY:[],
  ELSS:[],
  DEBT:[]
}

PORTFOLIO_URI="https://coin.zerodha.com/api/mf/holdings"

HEADERS = dict({
  "cookie": "",
  "x-csrftoken":""
})




def parsePortfolio(response):
  try:
    for fund in response['data']:
      print(fund['fund'])
      print(fund['quantity'])
      temp_fund={
        'scheme_name':fund['fund'],
        'net': fund['last_price'] * fund['quantity']
      }

      print(temp_fund)

      if mf_types[temp_fund['scheme_name']]==EQUITY:
        fundTypes[EQUITY].append(temp_fund)
      elif mf_types[temp_fund['scheme_name']]==ELSS:
        fundTypes[ELSS].append(temp_fund)
      elif mf_types[temp_fund['scheme_name']]==DEBT:
        fundTypes[DEBT].append(temp_fund)

      print(f'Done handling {temp_fund["scheme_name"]}')


    print(":: Funds Totals ::\n")
    for fundType in fundTypes.keys():
      total=0
      print(" ***************** " + fundType + " ***********************\n")
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
    
    print("::::::::::  Enter the cookie :::::::")
    cookie=input().strip()
    HEADERS["cookie"]=cookie 
    
    print("::::::::::  Enter the csrf token :::::::")
    csrf_token=input().strip()
    HEADERS["x-csrftoken"]=csrf_token

    portfolio = requests.get(PORTFOLIO_URI, headers=HEADERS)
    portfolio_json = portfolio.json()
    print(portfolio_json)
    print(f'API Response validation :: {portfolio_json["status"]}')
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
