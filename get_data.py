'''import pandas as pd
import yahooquery as yhq

tickers = [
    'MGLU3.SA', 'VVAR3.SA', 'ITSA4.SA', 'ITUB4.SA', 'VALE3.SA', 'COGN3.SA',
    'AZUL4.SA', 'IRBR3.SA', 'ABEV3.SA', 'BTOW3.SA', 'EMBR3.SA', 'FLRY3.SA'
]

data = yhq.Ticker(tickers, asynchronous=True)
df = data.history(period='60d', interval='2m')

df.to_csv('./b3_data.csv')'''
