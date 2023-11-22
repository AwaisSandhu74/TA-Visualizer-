import requests
import yfinance as yf 
import datetime as DT 
#from datetime import datetime, timedelta
from wikipediasp500 import clean_data
import json

clean = clean_data()

class Data(object):
    api_key = 'O8FZWSKFXV1J6CFJ'
    url = f'https://www.alphavantage.co/query'

    def __init__(self, ticker):

        if ticker in clean:
            self.__ticker = ticker
            self.__last_100, self.__last_30, self.__last_7  = [], [], []
        else:
            raise ValueError("Invalid ticker symbol. Please enter a valid company from the S&P 500.") 


    def fetch_data(self):

        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.__ticker,
            'apikey': Data.api_key,
        }
        response = requests.get(Data.url, params=params)
        data = response.json()
        return data
    

    def get_close_over_peiod(self, window):

        data = self.fetch_data()
        close_over_peiod = []
        for item in data['Time Series (Daily)'].values():
            if len(close_over_peiod) < window:
                close_over_peiod.append(float(item['4. close']))
            else:
                break
    
        return close_over_peiod


    def fetch_sma(self, window):

        sma_list = self.get_sma_data(window)
        return f"{(sum(sma_list)/len(sma_list)):.2f}"


    def get_sma_data(self, window):

        close_data = []
        if window < 1:
            raise ValueError("The period must not be less than 1")
        close_data = self.get_close_over_peiod(window)
        
        return close_data


    def exponential_moving_average(self, window):   

        close_data = self.get_close_over_peiod(window)[::-1]
        smoothing_constant = 2 / (1 + window)
        ema = [sum(close_data[:window]) / window]  # Initial SMA value

        for i in range(1, len(close_data)):
            ema_value = (close_data[i] * smoothing_constant) + (ema[-1] * (1-smoothing_constant))
            ema.append(ema_value)

        return ema


    def exponential_moving_average_macd(self, data, window):

        smoothing_constant = 2 / (1 + window)
        ema = [sum(data[:window]) / window]  # Initial SMA value

        for i in range(1, len(data)):
            ema_value = (data[i] * smoothing_constant) + (ema[-1] * (1 - smoothing_constant))
            ema.append(ema_value)

        return ema


    def calculate_macd(self):
        
        ema12 = self.exponential_moving_average(12)
        ema26 = self.exponential_moving_average(26)

        macd_line = [ema12[i] - ema26[i] for i in range(len(ema12))]
        signal_line = self.exponential_moving_average_macd(macd_line, 9)
        macd_histogram = [macd_line[i] - signal_line[i] for i in range(len(signal_line))]

        return macd_line, signal_line, macd_histogram


    def last_100_trading_days(self):
        data = self.fetch_data()
        for date, values in data['Time Series (Daily)'].items():
            if len(self.__last_100) >= 100:
                break
            self.__last_100.append((date, values['1. open'], values['2. high'], values['3. low'], values['4. close']))
        self.print_data(self.__last_100)


    def last_30_trading_days(self):
        data = self.fetch_data()
        for date, values in data['Time Series (Daily)'].items():
            if len(self.__last_30) >= 30:
                break
            self.__last_30.append((date, values['1. open'], values['2. high'], values['3. low'], values['4. close']))
        self.print_data(self.__last_30)


    def last_7_trading_days(self):
        data = self.fetch_data()
        for date, values in data['Time Series (Daily)'].items():
            if len(self.__last_7) >= 7:
                break
            self.__last_7.append((date, values['1. open'], values['2. high'], values['3. low'], values['4. close']))
        self.print_data(self.__last_7)
    
    
    def calculate_rsi(self, period=14):
        data = self.fetch_data()
        temp = data['Time Series (Daily)']
        close_prices = []
        price_changes = []
        up_changes = []
        down_changes = []

        for date in temp:
            if len(close_prices) >= period:
                break
            day_data = temp[date]
            close_prices.append(float(day_data['4. close']))

        for i in range(1, len(close_prices)):
            change = close_prices[i] - close_prices[i - 1]

            if change > 0:
                up_changes.append(change)
            elif change < 0:
                down_changes.append(change)
        
        avg_up = sum(up_changes) / 14
        avg_down = sum(down_changes) / 14

        if avg_down != 0:
            rs = avg_up / avg_down  
        else:
            rs = 0

        rsi = 100 - (100 / (1 + rs))
        
        return rsi










  
    
clo = Data("AAPL")
smaa_data = clo.calculate_macd()
print(smaa_data)

