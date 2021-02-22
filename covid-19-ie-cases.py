from matplotlib import pyplot as plt
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import jinja2

# Variables
population = 4937786
days = 7
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

# Format columns
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['7DayAverage'] = df['7DayAverage'].round(0).astype(pd.Int64Dtype())
df['14DayAverage'] = df['14DayAverage'].round(0).astype(pd.Int64Dtype())
df['7DayPer100K'] = df['7DayPer100K'].round(0).astype(pd.Int64Dtype())
df['14DayPer100K'] = df['14DayPer100K'].round(0).astype(pd.Int64Dtype())

# Filter data for table
df = df.tail(days)
table = df[["Date", "ConfirmedCovidCases", "7DayAverage","14DayAverage", "7DayPer100K", "14DayPer100K"]]

# Make column names friendly
#table.rename(columns={"ConfirmedCovidCases": "Cases",
#                      "7DayAverage": "7 Day Average",
#                      "14DayAverage": "14 Day Average",
#                      "7DayPer100K": "7-day case notifications per 100K",
#                      "14DayPer100K": "14-day case notifications per 100K"}, inplace=True)

# Format HTML table
def color_rising(s):
    is_rising = s.pct_change() > 0
    return ['background-color: red' if v else '' for v in is_rising]

table_html = table.style.apply(color_rising, subset=['7DayAverage','14DayAverage','7DayPer100K','14DayPer100K']).hide_index().render()

# Render template
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

# Write HTML file
file = open(output_file, "w")
file.write (template.render(table=table_html))
file.close()
