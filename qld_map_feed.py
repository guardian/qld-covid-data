import scraperwiki
import pandas as pd 
from modules.syncData import syncData

data = scraperwiki.sqlite.select("* from hhs_counts")

new = pd.DataFrame(data)

# Cut down
new = new.loc[(new['header'] == 'Active cases') & (new['HHS'] != "Queensland") & (new['HHS'] != "Interstate/Other")]
new = new[['HHS', 'count', 'date']]

# Clean
new.columns = ["place", "count", "date"]
new['date'] = pd.to_datetime(new['date'])
new['date'] = new['date'].dt.strftime('%Y-%m-%d')


jsony = new.to_json(orient="records")


syncData(jsony, "covidfeeds", "queensland-hhs-covid-cases")