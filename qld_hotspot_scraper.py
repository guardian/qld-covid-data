import pandas as pd 
import requests 
from modules.yachtCharter import yachtCharter
import os
import re
data_path = os.path.dirname(__file__) 
pd.set_option("display.max_rows", None, "display.max_columns", None)

headers = {'user-agent': 'The Guardian'}
html = requests.get('https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/contact-tracing', headers=headers).text
tables = pd.read_html(html)
table_labels = ["Close contact", "Historical casual contact", "Casual contact", "Low risk contact"]


# print(tables[2])
# print(len(tables))

listo = []
for i in range(0, len(table_labels)):
    inter = tables[i]
    inter['Type'] = table_labels[i]
    listo.append(inter)


df = pd.concat(listo)


df['Place'] = df['Place'].astype(str)

## Fix issues from lack of whitespace
import re
df['Place'] = df['Place'].apply(lambda x: re.sub(r'([a-zA-Z])(\()', r'\1 \2', x))
df['Place'] = df['Place'].apply(lambda x: re.sub(r'(\))([a-zA-Z])', r'\1 \2', x))

df['Place'] = df['Place'].apply(lambda x: re.sub(r'([1-9])(\()', r'\1 \2', x))
df['Place'] = df['Place'].apply(lambda x: re.sub(r'(\))([1-9])', r'\1 \2', x))

df['Place'] = df['Place'].apply(lambda x: re.sub(r'([a-zA-Z])([1-9])', r'\1 \2', x))

# Sort descending

try:
    df['Sort'] = pd.to_datetime(df['Date'], format="%A %d %B") + pd.offsets.DateOffset(years=121)
    df = df.sort_values(by=["Sort", "Type"], ascending=False)
except:
    pass

df = df[['Date', 'Place', 'Suburb', 'Arrival time', 'Departure time', 'Type']]

# Drop blank row in casual contacts table
df.dropna(inplace=True)


# Parse times

# df['Arrival sort'] = df['Arrival time'].apply(lambda x: pd.to_datetime(x.replace(" ", ''), format="%I.%M%p") if "." in x else pd.to_datetime(x, format="%I%p"))
# df['Departure sort'] = df['Departure time'].apply(lambda x: pd.to_datetime(x.replace(" ", ''), format="%I.%M%p") if "." in x else pd.to_datetime(x, format="%I%p"))

# df['Arrival sort'] = df['Arrival sort'].dt.strftime("%H:%M")
# df['Departure sort'] = df['Departure sort'].dt.strftime("%H:%M")

with open(f"{data_path}/hotspots.csv", "w") as f:
    df.to_csv(f, index=False, header=True)

def makeTestingLine(df):
	
    template = [
            {
                "title": "Queensland Covid Hotspots",
                "subtitle": f"""""",
                "footnote": "",
                "source": "| Sources: Queensland Department of Health",
                "yScaleType":"",
                "minY": "0",
                "maxY": "",
                "x_axis_cross_y":"",
                "periodDateFormat":"",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10"
            }
        ]
    key = []
    # labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    labels = []


    yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"table"}], 
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "TRUE","enableSort": "TRUE"}], chartName="qld_covid_hotspots")

makeTestingLine(df)


