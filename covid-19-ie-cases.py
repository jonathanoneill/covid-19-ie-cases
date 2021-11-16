import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import jinja2

# Constants
POPULATION = 4757976 #2016 Census
DAYS = 14
DATA_URL = 'https://opendata.arcgis.com/datasets/d8eb52d56273413b84b0187a4e9117be_0.csv'
DATA_FILE = 'covid-19-ie-cases.csv'
HTML_FILE = "covid-19-ie-cases.html"
PNG_FILE = 'covid-19-ie-cases.png'
TEMPLATE_FILE = 'template.html'

# Get latest data in csv format
data_content = requests.get(DATA_URL).content
csv_file = open(DATA_FILE, 'wb')
csv_file.write(data_content)
csv_file.close()
df = pd.read_csv(DATA_FILE)

# Calculations
df['Num7DayAverage'] = df['ConfirmedCovidCases'].rolling(7).mean()
df['Num14DayAverage'] = df['ConfirmedCovidCases'].rolling(14).mean()
df['Num7DayPer100K'] = df['ConfirmedCovidCases'].rolling(7).sum() / POPULATION * 100000
df['Num14DayPer100K'] = df['ConfirmedCovidCases'].rolling(14).sum() / POPULATION * 100000

df['Is7DayAverageRising'] = df['Num7DayAverage'].pct_change() > 0
df['Is14DayAverageRising'] = df['Num14DayAverage'].pct_change() > 0
df['Is7DayPer100KRising'] = df['Num7DayPer100K'].pct_change() > 0
df['Is14DayPer100KRising'] = df['Num14DayPer100K'].pct_change() > 0

# Format columns
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Num7DayAverage'] = df['Num7DayAverage'].round(0).astype(pd.Int64Dtype())
df['Num14DayAverage'] = df['Num14DayAverage'].round(0).astype(pd.Int64Dtype())
df['Num7DayPer100K'] = df['Num7DayPer100K'].round(0).astype(pd.Int64Dtype())
df['Num14DayPer100K'] = df['Num14DayPer100K'].round(0).astype(pd.Int64Dtype())

# Filter data for table
df = df.tail(DAYS)

# Load template
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)

# Convert DataFrame to dictionary
rows = (
    df
    .to_dict(orient='records')
)[:DAYS]

# Write HTML file
file = open(HTML_FILE, "w")
file.write (template.render(days=DAYS, rows=rows))
file.close()

# Plot Moving Averages
ax = plt.gca()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
plt.ylabel('Cases/100K')
df.plot(kind='line',x='Date',y='Num7DayPer100K',ax=ax)
df.plot(kind='line',x='Date',y='Num14DayPer100K', ax=ax)
ax.legend(["7 Day Moving Average", "14 Day Moving Average"])
plt.savefig(PNG_FILE)
