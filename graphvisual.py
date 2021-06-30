import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates 
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web 
import seaborn as sns
import os.path 
from os import path
style.use('ggplot')

STOCK_TICKER = input("Please Enter Stock Symbol (Ticker)")

# Intialize Dates for stock using user input

start_year, start_month, start_day = input("Enter Year,Month,Date:").split(',')
end_year, end_month, end_day = input("Enter Year,Month,Date:").split(',')
start = dt.datetime(int(start_year),int(start_month),int(start_day))
end = dt.datetime(int(end_year),int(end_month),int(end_day))

# Grab Desired Data + Create Csv File Name for Querying

stock_vars = web.DataReader(STOCK_TICKER,'yahoo',start ,end)
csv_name = STOCK_TICKER.lower() + '.csv'

# Check if csv already exists if so, overwrite or append, else create a new csv

if path.exists(csv_name):
  # O - Overwrite , A - Append , N - Neither(Just Passes Through)
  override_or_append = input("Would you like to Overwrite, Append or Neither? O or A or N")
  if override_or_append == "O":
    stock_vars.to_csv(csv_name)
  elif override_or_append == "A":
    stock_vars.to_csv(csv_name, mode='a',header = False)
else:
  stock_vars.to_csv(csv_name) 

#Read in CSV created from above 

df_inital = pd.read_csv(csv_name,parse_dates=True, index_col = 0)

#Remove Duplicates 
df_unique = (df_inital.drop_duplicates()).copy()


# Using MplFinance, Create Candlestick Graph 
mpf.plot(df_unique, type = "candle", volume= True, mav = 2)

#Create 20 moving average value 
df_unique['20ma'] = df_unique['Adj Close'].rolling(window = 20).mean()

# Remove, NaN's from Data Frame 
df_no_NaN = df_unique[df_unique['20ma'].notna()]


# Create subplot graph
ax1 = plt.subplot2grid((6,1),(0,0), rowspan = 5, colspan =1 )

#Plot Graphs for Adj Close and Moving Average
ax1.plot(df_unique.index, df_unique['Adj Close'] , label = 'Adj Close')
ax1.plot(df_unique.index, df_unique['20ma'], label = "Moving Average")

#Added Graph Legend + Axis Description 
ax1.legend(loc='best')
ax1.set_ylabel('Price in $')


#Ouputs plot's for Adj Close & Moving Average 
plt.show()