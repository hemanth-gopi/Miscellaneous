
import json
from MFTypes import mf_types,EQUITY,ELSS,DEBT

f = open('MFSegregatorForExcelReport/input.json',)
response = json.load(f)


fundTypes={
  EQUITY:[],
  ELSS:[],
  DEBT:[]
}

for fund in response['data']['portfolio']:
  # print(fund['scheme_name'])
  # print(fund['net'])
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
  print(total)
  print()
  
