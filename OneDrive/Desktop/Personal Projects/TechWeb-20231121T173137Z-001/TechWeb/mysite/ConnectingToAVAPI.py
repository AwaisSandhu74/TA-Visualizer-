import requests
import yfinance as yf 
from datetime import datetime, timedelta
from wikipediasp500 import clean_data
import json
from mplcursors import cursor
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

clean = clean_data()

class Data(object):
    api_key = '' 
    url = f'https://www.alphavantage.co/query'
    tech_indi = TechIndicators(key=api_key)

    def __init__(self, ticker):

        if ticker in clean:
            self.__ticker = ticker
            self.__last_n = []
        else:
            raise ValueError("Invalid ticker symbol. Please enter a valid company symbol.") 


    def fetch_description(self):
 
        params = {
            'function': 'OVERVIEW',
            'symbol': self.__ticker,  
            'apikey': Data.api_key,
        }

        response = requests.get(Data.url, params=params)
        data = response.json()

        return data['Description']
    

    def fetch_overview(self):

        params = {
            'function': 'OVERVIEW',
            'symbol': self.__ticker,  
            'apikey': Data.api_key,
        }

        response = requests.get(Data.url, params=params)
        data = response.json()
    
        return data


    def get_news_and_sentiments_general(self):
        new = []
        params = {
            'function': 'NEWS_SENTIMENT',
            'sort': 'LATEST',
            'apikey': Data.api_key,
        }
        response = requests.get(Data.url, params=params)
        data = response.json()["feed"][:15]
        for i in data:
            new.append({'title': i['title'], 'url' : i['url'], 'authors' : i['authors'], 'summary' : i['summary'], 'topics': i['topics'], 'banner_image' : i['banner_image'], 'overall_sentiment_score' : i['overall_sentiment_score'], 'overall_sentiment_label' : i['overall_sentiment_label'], 'ticker_sentiment' : i['ticker_sentiment']})
        
        return new

    
    def fetch_income_statement(self):
        
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': self.__ticker,  
            'apikey': Data.api_key,
        }
        
        response = requests.get(Data.url, params=params)
        data = response.json()
        filtered = data["quarterlyReports"][:4]

        return filtered
    
    
    def fetch_balance_sheet(self):

        params = {
            'function': 'BALANCE_SHEET',
            'symbol': self.__ticker,  
            'apikey': Data.api_key,
        }
        
        response = requests.get(Data.url, params=params)
        data = response.json()
        filtered = data["quarterlyReports"][:4]

        return filtered


    def fetch_data(self):

        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.__ticker,
            'apikey': Data.api_key,
        }
        response = requests.get(Data.url, params=params)
        data = response.json()
        print(data)
        if 'Time Series (Daily)' not in data:
            raise ValueError("Data not available for the specified ticker symbol.")
        
        return data
    

    def get_close_over_period(self, window):

        data = self.fetch_data()
        close_over_period = []
        for item in data['Time Series (Daily)'].values():
            if len(close_over_period) < window:
                close_over_period.append(float(item['4. close']))
            else:
                break
    
        return close_over_period


    def get_low_over_period(self, window):

        data = self.fetch_data()
        low_over_period = []
        for item in data['Time Series (Daily)'].values():
            if len(low_over_period) < window:
                low_over_period.append(float(item['3. low']))
            else:
                break
    
        return low_over_period

    
    def get_high_over_period(self, window):

        data = self.fetch_data()
        high_over_period = []
        for item in data['Time Series (Daily)'].values():
            if len(high_over_period) < window:
                high_over_period.append(float(item['2. high']))
            else:
                break
    
        return high_over_period

    
    def get_close_over_period_wd(self, window):

        close_over_period = {}
        data = self.fetch_data()
        for date, value in data['Time Series (Daily)'].items():
            if len(close_over_period) < window:
                close_over_period[date] = float(value['4. close'])
            else:
                break
    
        return close_over_period


    def get_low_over_period_wd(self, window):

        low_over_period = {}
        data = self.fetch_data()
        for date, value in data['Time Series (Daily)'].items():
            if len(low_over_period) < window:
                low_over_period[date] = float(value['3. low'])
            else:
                break
    
        return low_over_period

    
    def get_high_over_period_wd(self, window):

        high_over_period = {}
        data = self.fetch_data()
        for date, value in data['Time Series (Daily)'].items():
            if len(high_over_period) < window:
                high_over_period[date] = float(value['2. high'])
            else:
                break
    
        return high_over_period


    def fetch_sma(self, window):

        sma_list = self.get_sma_data(window)
        return f"{(sum(sma_list)/len(sma_list)):.2f}"


    def get_sma_data(self, window):

        close_data = []
        if window < 1:
            raise ValueError("The period must not be less than 1")
        close_data = self.get_close_over_period(window)
        
        return close_data


    def exponential_moving_average_macd(self, data, window):

        smoothing_constant = 2 / (1 + window)
        ema = [sum(data[:window]) / window]  

        for i in range(1, len(data)):
            ema_value = (data[i] * smoothing_constant) + (ema[-1] * (1 - smoothing_constant))
            ema.append(ema_value)

        return ema


    def calculate_macd(self):
        
        ema12 = self.exponential_moving_average(12)
        ema26 = self.exponential_moving_average(26)

        common_dates = []
        for date in ema12:
            if date in ema26:
                common_dates.append(date)
        
        macd_line = []
        for date in common_dates:
            macd_line.append(ema12[date] - ema26[date])

        signal_line = self.exponential_moving_average_macd(macd_line, 9)
        macd_histogram = [macd_line[i] - signal_line[i] for i in range(len(signal_line))]

        return macd_line, signal_line, macd_histogram


    def retrieve_last_n_trading_days(self, n):

        data = self.fetch_data()
        for date, values in data['Time Series (Daily)'].items():
            if len(self.__last_n) >= n:
                break
            self.__last_n.append(
                (
                    date,
                    float(values['1. open']),
                    float(values['2. high']),
                    float(values['3. low']),
                    float(values['4. close'])
                )
            )
        return self.print_data()


    def four_type_indicator(self, indicator_type, window):

        if indicator_type.lower() not in ('rsi', 'ema', 'bbands', 'trima'):
            raise ValueError("indicator type must be: rsi, ema, bbands, or trima")
        else:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=window - 1)  

            if indicator_type.lower() == 'rsi':
                c = Data.tech_indi.get_rsi(symbol=self.__ticker, time_period=window, interval='daily', series_type='close')[0]
                rsi_data = {date: float(values['RSI']) for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
            
                return rsi_data
            
            elif indicator_type.lower() == 'ema':
                c = Data.tech_indi.get_ema(symbol=self.__ticker, time_period=window, interval='daily', series_type='close')[0]
                ema_data = {date: float(values['EMA']) for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
            
                return ema_data

            elif indicator_type.lower() == 'trima':
                c = Data.tech_indi.get_trima(symbol=self.__ticker, time_period=window, interval='daily', series_type='close')[0]
                trima_data = {date: float(values['TRIMA']) for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
            
                return trima_data

            else:
                if indicator_type.lower() == 'bbands':
                    c = Data.tech_indi.get_bbands(symbol=self.__ticker, time_period=window, interval='daily', series_type='close')[0]
                    bbands_data = {}

                    for date, values in c.items():
                        if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date:
                            bbands_values = (
                                float(values['Real Upper Band']),
                                float(values['Real Middle Band']),
                                float(values['Real Lower Band'])
                            )
                            bbands_data[date] = bbands_values

                    return bbands_data


    def three_type_indicator(self, indicator_type, window):

        if indicator_type.lower() not in ('willr', 'adx', 'cci', 'aroon', 'ad', 'obv'):
            raise ValueError("indicator type must be: willr, adx, cci, aroon, ad, or obv")
        else:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=window - 1)

            if indicator_type.lower() == 'willr':
                c = Data.tech_indi.get_willr(symbol=self.__ticker, time_period=window, interval='daily')[0]
                willr_data = {date: float(values['WILLR']) for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
            
                return willr_data
            
            elif indicator_type.lower() == 'adx':
                c = Data.tech_indi.get_adx(symbol=self.__ticker, time_period=window, interval='daily')[0]
                adx_data = {date: float(values['ADX']) for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
                
                return adx_data

            elif indicator_type.lower() == 'cci':
                c = Data.tech_indi.get_cci(symbol=self.__ticker, time_period=window, interval='daily')[0]
                cci_data = {date: float(values['CCI']) for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
                
                return cci_data
            
            elif indicator_type.lower() == 'aroon':
                c = Data.tech_indi.get_aroon(symbol=self.__ticker, time_period=window, interval='daily')[0]
                aroons_data = {}
    
                for date, values in c.items():
                    if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date:
                        aroons_values = (
                            float(values['Aroon Down']),
                            float(values['Aroon Up'])
                        )
                        aroons_data[date] = aroons_values

                return aroons_data
            
            elif indicator_type.lower() == 'ad':
                c = Data.tech_indi.get_ad(symbol=self.__ticker, interval='daily')[0]
                ad_data = {}
        
                for date, values in c.items():
                    if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date:
                        ad_value = float(values['Chaikin A/D']) if 'Chaikin A/D' in values else float(values)
                        ad_data[date] = ad_value

                return ad_data
            
            else:
                if indicator_type.lower() == 'obv':
                    c = Data.tech_indi.get_obv(symbol=self.__ticker, interval='daily')[0]
                    obv_data = {date: float(values['OBV']) for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
                    
                    return obv_data
                

    def rsi_av(self, window=14):

        return self.four_type_indicator('rsi', window)
    

    def exponential_moving_average(self, window):

        return self.four_type_indicator('ema', window)


    def bbands_av(self, window):
        
        return self.four_type_indicator('bbands', window)
    
    def trima_av(self, window):

        return self.four_type_indicator('trima', window)


    def willr_av(self, window):

        return self.three_type_indicator('willr', window)


    def adx_av(self, window):

        return self.three_type_indicator('adx', window)


    def cci_av(self, window):

        return self.three_type_indicator('cci', window)

    
    def aroon_av(self, window):

        return self.three_type_indicator('aroon', window)

    
    def ad_av(self, window):

        return self.three_type_indicator('ad', window)

    
    def obv_av(self, window):

        return self.three_type_indicator('obv', window)

    
    def sar_av(self, window):

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=window - 1)  

        c = Data.tech_indi.get_sar(symbol=self.__ticker, interval='daily')[0]
        sar_data = {date: values['SAR'] for date, values in c.items() if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date}
        
        return sar_data


    def calculate_stochastic_oscillator(self, window=14):

        close_prices = self.get_close_over_period(window)
        low_prices = self.get_low_over_period(window)
        high_prices = self.get_high_over_period(window)
        
        latest_close = close_prices[0]  
        lowest_low = min(low_prices)
        highest_high = max(high_prices)
        
        K = ((latest_close - lowest_low) / (highest_high - lowest_low)) * 100
        d_values = self.exponential_moving_average_macd([K], 3) 
        
        return float(f"{K:.2f}"), float(f"{d_values[0]:.2f}") 


    def print_data(self):

        output = ""
        for tup in self.__last_n:
            output += f"({tup[0]}): Open: {tup[1]}, High: {tup[2]}, Low: {tup[3]}, Close: {tup[4]}\n"
        
        return output.rstrip()




print(Data("AMZN").fetch_top20())

