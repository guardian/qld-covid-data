import scraperwiki
import pandas as pd 
from modules.yachtCharter import yachtCharter
from modules.numberFormat import numberFormat
import numpy as np 
import datetime

#%%

# Work out sixty days ago to truncate chart
today = datetime.datetime.today()
sixty_ago = today - datetime.timedelta(60)
chart_truncate =  sixty_ago.date()

data = scraperwiki.sqlite.select("* from source")
new = pd.DataFrame(data)

old = pd.read_csv('qld-covid.csv')


## Pivot dataframe
pivoted = new.pivot(index="date", columns="header")['count'].reset_index()
pivoted = pivoted[['date', 'Interstate acquired',
       'Locally Acquired—close contact with confirmed case',
       'Locally Acquired—no known contact', 'Overseas acquired','Under investigation']]
pivoted = pivoted.append(old)
pivoted['date'] = pd.to_datetime(pivoted['date'], format="%d/%m/%Y")
pivoted = pivoted.sort_values(by="date", ascending=True)

#%%
pivoted.columns = ['Date', 'Interstate', 'Local', 'Local unknown', 'Overseas', 'Under investigation']


pivoted['Overseas'] = pd.to_numeric(pivoted['Overseas'])

pivoted['Local'] = pd.to_numeric(pivoted['Local'])
pivoted['Local unknown'] = pd.to_numeric(pivoted['Local unknown'])
pivoted['Under investigation'] = pd.to_numeric(pivoted['Under investigation'])

#%%
pivoted['Local & under investigation'] = pivoted['Local'] + pivoted['Local unknown'] + pivoted['Under investigation']

## Work out the difference in the cumulative figures and calculate rolling average

pivoted['New overseas cases'] = pivoted['Overseas'].diff(periods=1)
pivoted.loc[pivoted['New overseas cases'] < 0, 'New overseas cases'] = 0
pivoted['Overseas, 7 day rolling average'] = round(pivoted['New overseas cases'].rolling(7).mean(),0)

pivoted['New local & under investigation cases'] = pivoted['Local & under investigation'].diff(periods=1)
pivoted.loc[pivoted['New local & under investigation cases'] < 0, 'New local & under investigation cases'] = 0

pivoted['Local & under investigation cases, 7 day rolling average'] = round(pivoted['New local & under investigation cases'].rolling(7).mean(),0)

avg = pivoted[['Date', 'Overseas, 7 day rolling average', 'Local & under investigation cases, 7 day rolling average']]

avg = avg.loc[avg['Date'] >= np.datetime64(chart_truncate)]
avg['Date'] = avg['Date'].dt.strftime('%Y-%m-%d')
last_date = avg.iloc[-1:]["Date"].values[0]
# print(pivoted)

def makeTestingLine(df):
	
    template = [
            {
                "title": "Trend in local and overseas-related transmission of Covid-19 in QLD, last 60 days",
                "subtitle": f"""Showing the 7 day rolling average of locally and overseas-acquired cases, with those under investigation added to the local category. Last updated {last_date}""",
                "footnote": "",
                "source": "| Sources: Covidlive.com.au, Queensland Department of Health",
                "dateFormat": "%Y-%m-%d",
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
    periods = []
    # labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    labels = []


    yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"linechart"}], 
    options=[{"colorScheme":"guardian"}], chartName="qld_covid_locally_acquired_trend")

makeTestingLine(avg)