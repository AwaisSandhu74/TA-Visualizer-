import requests
import yfinance as yf 
from datetime import datetime, timedelta
from wikipediasp500 import clean_data
import json
from mplcursors import cursor
from alpha_vantage.techindicators import TechIndicators


clean = clean_data()

class Data(object):
    api_key = 'O8FZWSKFXV1J6CFJ'
    url = f'https://www.alphavantage.co/query'
    tech_indi = TechIndicators(key=api_key)

    def __init__(self, ticker):

        if ticker in clean:
            self.__ticker = ticker
            self.__last_n = []
        else:
            raise ValueError("Invalid ticker symbol. Please enter a valid company symbol.") 


    def fetch_data(self):

        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.__ticker,
            'apikey': Data.api_key,
        }
        response = requests.get(Data.url, params=params)
        data = response.json()
        if 'Time Series (Daily)' not in data:
            raise ValueError("Data not available for the specified ticker symbol.")
        
        return data