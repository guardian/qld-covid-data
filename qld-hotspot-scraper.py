import pandas as pd 
import requests 
from modules.yachtCharter import yachtCharter
import os
# from html2text import unescape
data_path = os.path.dirname(__file__) 

headers = {'user-agent': 'The Guardian'}
html = requests.get('https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/contact-tracing', headers=headers).text
tables = pd.read_html(html)
table_labels = ["Close contact", "Casual contact", "Low risk contact"]

listo = []
for i in range(0, len(table_labels)):
    inter = tables[i]
    inter['Type'] = table_labels[i]
    listo.append(inter)


df = pd.concat(listo)
df['Place'] = df['Place'].astype(str)
# print(df['Place'].dtype)
# df['Place'] = df['Place'].str.decode('UTF-8')
# df = df.astype(str)


# with open(f"{data_path}/hotspots.csv", "w") as f:
#     df.to_csv(f, index=False, header=True)

print(df.loc[df['Place'].str.contains("Spinnaker")])

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
    options=[{"colorScheme":"guardian"}, {"format": "scrolling"}, {"enableSearch": "TRUE"}, {"enableSort": "TRUE"}], chartName="qld_covid_hotspots")

makeTestingLine(df)


