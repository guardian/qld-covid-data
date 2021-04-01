import scraperwiki
import pandas as pd 
from modules.yachtCharter import yachtCharter
from modules.numberFormat import numberFormat

data = scraperwiki.sqlite.select("* from source")
new = pd.DataFrame(data)

## Pivot dataframe
pivoted = new.pivot(index="date", columns="header")['count'].reset_index()
pivoted = pivoted[['date', 'Interstate acquired',
       'Locally Acquired—close contact with confirmed case',
       'Locally Acquired—no known contact', 'Overseas acquired','Under investigation']]
pivoted['date'] = pd.to_datetime(pivoted['date'])
pivoted = pivoted.sort_values(by="date", ascending=True)
pivoted.columns = ['Date', 'Interstate', 'Local', 'Local unknown', 'Overseas', 'Under investigation']


pivoted['Date'] = pivoted['Date'].dt.strftime('%Y-%m-%d')


## Work out the difference in the cumulative figures
cols = ['Interstate', 'Local', 'Local unknown', 'Overseas', 'Under investigation']

for col in cols:
    pivoted[col] = pd.to_numeric(pivoted[col]).diff(periods=1)
    pivoted.loc[pivoted[col] < 0, col] = 0
    # pivoted[col] = pd.to_numeric(pivoted[col]) + pd.to_numeric(pivoted[col]).diff(periods=1)

# print(pivoted)

last_date = pivoted.iloc[-1:]["Date"].values[0]
# print(last_date)
def makeTestingLine(df):
	
    template = [
            {
                "title": "Source of Covid-19 infections in Queensland",
                "subtitle": f"""Showing the daily count of new cases by the source of infection. {last_date}""",
                "footnote": "",
                "source": "| Sources: Covidlive.com.au, Queensland Department of Health",
                "dateFormat": "%Y-%m-%d",
                "minY": "0",
                "maxY": "",
                "xAxisDateFormat":"%b %d",
                "tooltip":"<strong>{{#nicerdate}}{{/nicerdate}}</strong><br/>{{group}}: {{groupValue}}<br/>Total: {{total}}",
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


    yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"stackedbar"}], chartName="qld_covid_infection_source")

makeTestingLine(pivoted)

