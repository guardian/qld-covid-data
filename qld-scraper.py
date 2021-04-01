import requests
import scraperwiki
import lxml.html
import time
import pandas as pd 
import os
# cd /Users/josh_nicholas/github/qld-covid-data/
data_path = os.path.dirname(__file__) 

url = 'https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/statistics'
html = requests.get(url).content
# historical = f'{data_path}/qld-historical.csv' 


## SAVE HISTORICAL DATA TO SQL 

previous_data = f'{data_path}/qld-covid.csv'
previous_data = pd.read_csv(previous_data)
previous_data = previous_data.melt(id_vars = "date", value_vars =['Overseas acquired', 'Locally Acquired—close contact with confirmed case',
      'Locally Acquired—no known contact','Interstate acquired', 'Under investigation', 'Total cases'])
previous_data.columns = ['date', 'header', 'count']
previous_data['date'] = pd.to_datetime(previous_data['date'])
previous_data['date'] = previous_data['date'].dt.strftime('%d/%m/%Y')

for row in previous_data.index:
	newRow = {}
	newRow["header"] = previous_data.loc[row, 'header']
	newRow["count"] = str(previous_data.loc[row,'count'])
	newRow["date"] = previous_data.loc[row,'date']
	# print(newRow)
	scraperwiki.sqlite.save(unique_keys=["header","date"], data=newRow, table_name="source")




# ### SCRAPE AND COMBINE INFECTION DATA

parser = lxml.html.HTMLParser(encoding="utf-8")
dom = lxml.html.fromstring(html, parser=parser)

source_trs = dom.cssselect('#QLD_Cases_Sources_Of_Infection tr')
source_date = dom.cssselect('#QLD_Cases_Sources_Of_Infection caption')[0].text.replace("Data as at ","").replace(". Refer to ", "")

source_data = []
print(source_date)
for tr in source_trs:
	newRow = {}
	newRow["header"] = tr.cssselect('th')[0].text
	newRow["count"] = tr.cssselect('td')[0].text.replace(",","")
	newRow["date"] = source_date
	# print(newRow)
	scraperwiki.sqlite.save(unique_keys=["header","date"], data=newRow, table_name="source")


# ### SCRAPE HHS CASES

hhs_table = pd.read_html(html, attrs = {'id': 'QLD_Cases_By_HHS'})[0]
hhs_table.columns = ["HHS", "Total cases", "Active cases","Total recovered","Total deaths"]
# hhs_table = hhs_table[["HHS", "Total cases", "Active cases"]]
hhs_table = hhs_table.melt(id_vars = "HHS", value_vars =["Total cases", "Active cases", "Total recovered", "Total deaths"])
hhs_table.columns = ["HHS", "header", "count"]

for row in hhs_table.index:
	newRow = {}
	newRow['HHS'] = hhs_table.loc[row, 'HHS']
	newRow["header"] = hhs_table.loc[row, 'header']
	newRow["count"] = str(hhs_table.loc[row,'count'])
	newRow["date"] = source_date
	# print(newRow)
	scraperwiki.sqlite.save(unique_keys=["header",'HHS',"date"], data=newRow, table_name="hhs_counts")





### old stuff for sorting out tables 

# previous = pd.read_csv(previous_data)
# # historical = pd.read_csv(historical)
# # historical.columns = ['date', 'Overseas acquired', 'Locally Acquired—close contact with confirmed case',
# #        'Locally Acquired—no known contact','Interstate acquired', 'Under investigation']

# # historical['Overseas acquired'] = historical['Overseas acquired'].str.replace(",", "")
# # historical['Overseas acquired'] = pd.to_numeric(historical['Overseas acquired'])
# # historical['Total cases'] = historical.sum(axis=1)


# combo = previous.append(new)
# combo['date'] = pd.to_datetime(combo['date'])
# combo.drop_duplicates(subset=["date"], inplace=True)

# with open(previous_data, "w") as f:
# 	combo.to_csv(f, index=False, header=True)