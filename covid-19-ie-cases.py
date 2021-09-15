from matplotlib import pyplot as plt
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import jinja2

# Constants
population = 4757976 #2016 Census
days = 14
output_file = "covid-19-ie-cases.html"

# Get latest data in csv format
filename = 'covid-19-ie-cases.csv'

data_url = 'https://opendata.arcgis.com/datasets/d8eb52d56273413b84b0187a4e9117be_0.csv'

data_content = requests.get(data_url).content
csv_file = open(filename, 'wb')
csv_file.write(data_content)
csv_file.close()

df = pd.read_csv(filename)

# Calculations
df['7DayAverage'] = df['ConfirmedCovidCases'].rolling(7).mean()
df['14DayAverage'] = df['ConfirmedCovidCases'].rolling(14).mean()
df['7DayPer100K'] = df['ConfirmedCovidCases'].rolling(7).sum() / population * 100000
df['14DayPer100K'] = df['ConfirmedCovidCases'].rolling(14).sum() / population * 100000

df['Is7DayAverageRising'] = df['7DayAverage'].pct_change() > 0
df['Is14DayAverageRising'] = df['14DayAverage'].pct_change() > 0
df['Is7DayPer100KRising'] = df['7DayPer100K'].pct_change() > 0
df['Is14DayPer100KRising'] = df['14DayPer100K'].pct_change() > 0

# Format columns
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['7DayAverage'] = df['7DayAverage'].round(0).astype(pd.Int64Dtype())
df['14DayAverage'] = df['14DayAverage'].round(0).astype(pd.Int64Dtype())
df['7DayPer100K'] = df['7DayPer100K'].round(0).astype(pd.Int64Dtype())
df['14DayPer100K'] = df['14DayPer100K'].round(0).astype(pd.Int64Dtype())

# Make column names friendly
df.rename(columns={ "ConfirmedCovidCases": "Cases",
                    "7DayAverage": "Num7DayAverage",
                    "14DayAverage": "Num14DayAverage",
                    "7DayPer100K": "Num7DayPer100K",
                    "14DayPer100K": "Num14DayPer100K"}, inplace=True)

# Filter data for table
df = df.tail(days)

# Load template
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

# Convert DataFrame to dictionary
rows = (
    df
    .to_dict(orient='records')
)[:days]

# Write HTML file
file = open(output_file, "w")
file.write (template.render(days=days, rows=rows))
file.close()

# Plot Moving Averages
ax = plt.gca()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
plt.ylabel('Cases/100K')
df.plot(kind='line',x='Date',y='Num7DayPer100K',ax=ax)
df.plot(kind='line',x='Date',y='Num14DayPer100K', ax=ax)
ax.legend(["7 Day Moving Average", "14 Day Moving Average"])
plt.savefig('covid-19-ie-cases.png')
