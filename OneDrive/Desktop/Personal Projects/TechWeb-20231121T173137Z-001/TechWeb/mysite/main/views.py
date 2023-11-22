from django.shortcuts import render
from ConnectingToAVAPI import Data
from .models import GraphData
from django.http import HttpResponse
from wikipediasp500 import clean_data
import plotly.express as px


def index(response, id):

    ls = GraphData.objects.get(id=id)
    return render(response, "main/base.html", {'ls':ls})

def home(response):

    companies = clean_data()
    return render(response, 'main/home.html', {'companies': companies})

def company_graph_lch(request, ticker, period):

    data_instance = Data(ticker)
    description = data_instance.fetch_description()  
    overview = data_instance.fetch_overview()
    income_statement = data_instance.fetch_income_statement()
    balance_sheet = data_instance.fetch_balance_sheet() 
    close = data_instance.get_close_over_period_wd(period)
    low = data_instance.get_low_over_period_wd(period)
    high = data_instance.get_high_over_period_wd(period)
    
    table_data = {
        "Name": overview['Name'],
        "Asset Type": overview['AssetType'],
        "Exchange": overview['Exchange'],
        "Currency": overview['Currency'],
        "MarketCap": overview['MarketCapitalization'],
        "Dividend Yield": overview['DividendYield'],
        "Beta": overview['Beta'],
        "PERatio" : overview['PERatio']
    }

    income = {
        "fiscalDateEnding":  [income_statement[0]['fiscalDateEnding'], income_statement[1]['fiscalDateEnding'], income_statement[2]['fiscalDateEnding'], income_statement[3]['fiscalDateEnding']],
        "grossProfit":  [income_statement[0]['grossProfit'], income_statement[1]['grossProfit'], income_statement[2]['grossProfit'], income_statement[3]['grossProfit']],
        "totalRevenue":  [income_statement[0]['totalRevenue'], income_statement[1]['totalRevenue'], income_statement[2]['totalRevenue'], income_statement[3]['totalRevenue']],
        "costOfRevenue":  [income_statement[0]['costOfRevenue'], income_statement[1]['costOfRevenue'], income_statement[2]['costOfRevenue'], income_statement[3]['costOfRevenue']],
        "costofGoodsAndServicesSold":  [income_statement[0]['costofGoodsAndServicesSold'], income_statement[1]['costofGoodsAndServicesSold'], income_statement[2]['costofGoodsAndServicesSold'], income_statement[3]['costofGoodsAndServicesSold']],
        "operatingIncome":  [income_statement[0]['operatingIncome'], income_statement[1]['operatingIncome'], income_statement[2]['operatingIncome'], income_statement[3]['operatingIncome']],
        "sellingGeneralAndAdministrative":  [income_statement[0]['sellingGeneralAndAdministrative'], income_statement[1]['sellingGeneralAndAdministrative'], income_statement[2]['sellingGeneralAndAdministrative'], income_statement[3]['sellingGeneralAndAdministrative']],
        "researchAndDevelopment":  [income_statement[0]['researchAndDevelopment'], income_statement[1]['researchAndDevelopment'], income_statement[2]['researchAndDevelopment'], income_statement[3]['researchAndDevelopment']],
        "operatingExpenses": [income_statement[0]['operatingExpenses'], income_statement[1]['operatingExpenses'], income_statement[2]['operatingExpenses'], income_statement[3]['operatingExpenses']],
        "investmentIncomeNet": [income_statement[0]['investmentIncomeNet'], income_statement[1]['investmentIncomeNet'], income_statement[2]['investmentIncomeNet'], income_statement[3]['investmentIncomeNet']],
        "netInterestIncome": [income_statement[0]['netInterestIncome'], income_statement[1]['netInterestIncome'], income_statement[2]['netInterestIncome'], income_statement[3]['netInterestIncome']],
        "interestIncome": [income_statement[0]['interestIncome'], income_statement[1]['interestIncome'], income_statement[2]['interestIncome'], income_statement[3]['interestIncome']],
        "interestExpense": [income_statement[0]['interestExpense'], income_statement[1]['interestExpense'], income_statement[2]['interestExpense'], income_statement[3]['interestExpense']],
        "nonInterestIncome": [income_statement[0]['nonInterestIncome'], income_statement[1]['nonInterestIncome'], income_statement[2]['nonInterestIncome'], income_statement[3]['nonInterestIncome']],
        "otherNonOperatingIncome": [income_statement[0]['otherNonOperatingIncome'], income_statement[1]['otherNonOperatingIncome'], income_statement[2]['otherNonOperatingIncome'], income_statement[3]['otherNonOperatingIncome']],
        "depreciation": [income_statement[0]['depreciation'], income_statement[1]['depreciation'], income_statement[2]['depreciation'], income_statement[3]['depreciation']],
        "depreciationAndAmortization": [income_statement[0]['depreciationAndAmortization'], income_statement[1]['depreciationAndAmortization'], income_statement[2]['depreciationAndAmortization'], income_statement[3]['depreciationAndAmortization']],
        "incomeBeforeTax": [income_statement[0]['incomeBeforeTax'], income_statement[1]['incomeBeforeTax'], income_statement[2]['incomeBeforeTax'], income_statement[3]['incomeBeforeTax']],
        "incomeTaxExpense": [income_statement[0]['incomeTaxExpense'], income_statement[1]['incomeTaxExpense'], income_statement[2]['incomeTaxExpense'], income_statement[3]['incomeTaxExpense']],
        "interestAndDebtExpense": [income_statement[0]['interestAndDebtExpense'], income_statement[1]['interestAndDebtExpense'], income_statement[2]['interestAndDebtExpense'], income_statement[3]['interestAndDebtExpense']],
        "ebitda": [income_statement[0]['ebitda'], income_statement[1]['ebitda'], income_statement[2]['ebitda'], income_statement[3]['ebitda']],
        "netIncome": [income_statement[0]['netIncome'], income_statement[1]['netIncome'], income_statement[2]['netIncome'], income_statement[3]['netIncome']],
    }
    
    balance = {"fiscalDateEnding":  [balance_sheet[0]['fiscalDateEnding'], balance_sheet[1]['fiscalDateEnding'], balance_sheet[2]['fiscalDateEnding'], balance_sheet[3]['fiscalDateEnding']],
        "totalCurrentAssets":  [balance_sheet[0]['totalCurrentAssets'], balance_sheet[1]['totalCurrentAssets'], balance_sheet[2]['totalCurrentAssets'], balance_sheet[3]['totalCurrentAssets']],
        "cashAndCashEquivalentsAtCarryingValue":  [balance_sheet[0]['cashAndCashEquivalentsAtCarryingValue'], balance_sheet[1]['cashAndCashEquivalentsAtCarryingValue'], balance_sheet[2]['cashAndCashEquivalentsAtCarryingValue'], balance_sheet[3]['cashAndCashEquivalentsAtCarryingValue']],
        "cashAndShortTermInvestments":  [balance_sheet[0]['cashAndShortTermInvestments'], balance_sheet[1]['cashAndShortTermInvestments'], balance_sheet[2]['cashAndShortTermInvestments'], balance_sheet[3]['cashAndShortTermInvestments']],
        "inventory":  [balance_sheet[0]['inventory'], balance_sheet[1]['inventory'], balance_sheet[2]['inventory'], balance_sheet[3]['inventory']],
        "currentNetReceivables":  [balance_sheet[0]['currentNetReceivables'], balance_sheet[1]['currentNetReceivables'], balance_sheet[2]['currentNetReceivables'], balance_sheet[3]['currentNetReceivables']],
        "totalNonCurrentAssets":  [balance_sheet[0]['totalNonCurrentAssets'], balance_sheet[1]['totalNonCurrentAssets'], balance_sheet[2]['totalNonCurrentAssets'], balance_sheet[3]['totalNonCurrentAssets']],
        "intangibleAssets": [balance_sheet[0]['intangibleAssets'], balance_sheet[1]['intangibleAssets'], balance_sheet[2]['intangibleAssets'], balance_sheet[3]['intangibleAssets']],
        "longTermInvestments": [balance_sheet[0]['longTermInvestments'], balance_sheet[1]['longTermInvestments'], balance_sheet[2]['longTermInvestments'], balance_sheet[3]['longTermInvestments']],
        "shortTermInvestments": [balance_sheet[0]['shortTermInvestments'], balance_sheet[1]['shortTermInvestments'], balance_sheet[2]['shortTermInvestments'], balance_sheet[3]['shortTermInvestments']],
        "otherCurrentAssets": [balance_sheet[0]['otherCurrentAssets'], balance_sheet[1]['otherCurrentAssets'], balance_sheet[2]['otherCurrentAssets'], balance_sheet[3]['otherCurrentAssets']],
        "totalLiabilities": [balance_sheet[0]['totalLiabilities'], balance_sheet[1]['totalLiabilities'], balance_sheet[2]['totalLiabilities'], balance_sheet[3]['totalLiabilities']],
        "currentAccountsPayable": [balance_sheet[0]['currentAccountsPayable'], balance_sheet[1]['currentAccountsPayable'], balance_sheet[2]['currentAccountsPayable'], balance_sheet[3]['currentAccountsPayable']],
        "deferredRevenue": [balance_sheet[0]['deferredRevenue'], balance_sheet[1]['deferredRevenue'], balance_sheet[2]['deferredRevenue'], balance_sheet[3]['deferredRevenue']],
        "shortTermDebt": [balance_sheet[0]['shortTermDebt'], balance_sheet[1]['shortTermDebt'], balance_sheet[2]['shortTermDebt'], balance_sheet[3]['shortTermDebt']],
        "longTermDebt": [balance_sheet[0]['longTermDebt'], balance_sheet[1]['longTermDebt'], balance_sheet[2]['longTermDebt'], balance_sheet[3]['longTermDebt']],
        "totalShareholderEquity": [balance_sheet[0]['totalShareholderEquity'], balance_sheet[1]['totalShareholderEquity'], balance_sheet[2]['totalShareholderEquity'], balance_sheet[3]['totalShareholderEquity']],
        "retainedEarnings": [balance_sheet[0]['retainedEarnings'], balance_sheet[1]['retainedEarnings'], balance_sheet[2]['retainedEarnings'], balance_sheet[3]['retainedEarnings']],
        "commonStock": [balance_sheet[0]['commonStock'], balance_sheet[1]['commonStock'], balance_sheet[2]['commonStock'], balance_sheet[3]['commonStock']],
        "commonStockSharesOutstanding": [balance_sheet[0]['commonStockSharesOutstanding'], balance_sheet[1]['commonStockSharesOutstanding'], balance_sheet[2]['commonStockSharesOutstanding'], balance_sheet[3]['commonStockSharesOutstanding']],
        }

    fig = px.line(x=list(close.keys()), y=[list(close.values()), list(low.values()), list(high.values())], 
                    labels={'x': 'Dates', 'y': 'Values'},)
   
  
    newnames = {'wide_variable_0':'Close Values', 'wide_variable_1': 'Low Values', 'wide_variable_2': 'High Values'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name], legendgroup = newnames[t.name], 
                                        hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

    fig.update_layout(
        width=1600, 
        font=dict(family="Times New Roman", size=14),  
        legend=dict(title_text="Legend", font=dict(family="Times New Roman", size=12)),  
        xaxis=dict(tickfont=dict(family="Times New Roman", size=12)), 
        yaxis=dict(tickfont=dict(family="Times New Roman", size=12)), 
    )

    interactive_plot = fig.to_html(full_html=False)

    context = {
        'ticker': ticker,
        'period': period,
        'interactive_plot': interactive_plot,
        'description' : description,
        'table_data' : table_data,
        'income' : income, 
        'balance' : balance,
    }
       
    return render(request, 'main/day_graph_lch.html', context)

    
def company_graph_3type(request, indicator_type, ticker, window):

    if indicator_type == 'aroon':
        raise ValueError("Indicator type must not be aroon. Please enter a valid indicator type or use company_graph_aroon.")
    else:
        data_instance = Data(ticker)
        indicator_data = data_instance.three_type_indicator(indicator_type, window)

        fig = px.line(x=list(indicator_data.keys()), y=[list(indicator_data.values())],
                        labels={'x': 'Dates', 'y': 'Values'}, 
                    )

        newnames = {'wide_variable_0':f'{indicator_type} values'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name], legendgroup = newnames[t.name], 
                                            hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

        fig.update_layout(
            width=1600,  # Adjust the width of the graph
            font=dict(family="Times New Roman", size=14),  # Change font family and size
            legend=dict(title_text="Legend", font=dict(family="Times New Roman", size=12)),  # Customize legend font
            xaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize x-axis tick font
            yaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize y-axis tick font
        )

        interactive_plot = fig.to_html(full_html=False)

        context = {
            'ticker': ticker,
            'window': window,
            'indicator_type' : indicator_type,
            'interactive_plot': interactive_plot,
        }
        
        return render(request, 'main/company_graph_3type.html', context)


def company_graph_4type(request, indicator_type, ticker, window):

    if indicator_type == 'bbands':
        raise ValueError("Indicator type must not be bbands. Please enter a valid indicator type or use company_graph_bbands.")
    else:
        data_instance = Data(ticker)
        indicator_data = data_instance.four_type_indicator(indicator_type, window)

        fig = px.line(x=list(indicator_data.keys()), y=[list(indicator_data.values())],
                        labels={'x': 'Dates', 'y': 'Values'}, 
                        title=f"{ticker}'s {indicator_type} data",
                    )

        newnames = {'wide_variable_0':f'{indicator_type} values'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name], legendgroup = newnames[t.name], 
                                            hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

        fig.update_layout(
            width=1600,  # Adjust the width of the graph
            font=dict(family="Times New Roman", size=14),  # Change font family and size
            legend=dict(title_text="Legend", font=dict(family="Times New Roman", size=12)),  # Customize legend font
            xaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize x-axis tick font
            yaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize y-axis tick font
        )

        interactive_plot = fig.to_html(full_html=False)

        context = {
            'ticker': ticker,
            'window': window,
            'interactive_plot': interactive_plot,
        }
        
        return render(request, 'main/company_graph_4type.html', context)


def company_graph_bbands(request, ticker, window):

    data_instance = Data(ticker)
    indicator_data = data_instance.four_type_indicator('bbands', window)
    real_upper, real_middle, real_lower = [], [], []

    for key, value in indicator_data.items():
        real_upper.append(indicator_data[key][0])
        real_middle.append(indicator_data[key][1])
        real_lower.append(indicator_data[key][2])

    fig = px.line(x=list(indicator_data.keys()), y=[real_upper, real_middle, real_lower],
                    labels={'x': 'Dates', 'y': 'Values'}, 
                    title=f"{ticker}'s bbands data",
                   )
    
    newnames = {'wide_variable_0':'real upper', 'wide_variable_1':'real middle', 'wide_variable_2':'real lower' }
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name], legendgroup = newnames[t.name], 
                                        hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

    fig.update_layout(
        width=1600,  # Adjust the width of the graph
        font=dict(family="Times New Roman", size=14),  # Change font family and size
        legend=dict(title_text="Legend", font=dict(family="Times New Roman", size=12)),  # Customize legend font
        xaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize x-axis tick font
        yaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize y-axis tick font
    )

    interactive_plot = fig.to_html(full_html=False)

    context = {
        'ticker': ticker,
        'window': window,
        'interactive_plot': interactive_plot,
    }
       
    return render(request, 'main/company_graph_bbands.html', context)


def company_graph_aroon(request, ticker, window):

    data_instance = Data(ticker)
    indicator_data = data_instance.three_type_indicator('aroon', window)
    aroon_down, aroon_upper = [], []
    date_list = list(indicator_data.keys())

    for key, value in indicator_data.items():
        aroon_down.append(indicator_data[key][0])
        aroon_upper.append(indicator_data[key][1])

    fig = px.line(x=date_list, y=[aroon_down, aroon_upper],
                    labels={'x': 'Dates', 'y': 'Values'}, 
                    title=f"{ticker}'s aroon data",
                   )
    
    newnames = {'wide_variable_0':'aroon down', 'wide_variable_1':'aroon upper'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name], legendgroup = newnames[t.name], 
                                        hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))

    fig.update_layout(
        width=1600,  # Adjust the width of the graph
        font=dict(family="Times New Roman", size=14),  # Change font family and size
        legend=dict(title_text="Legend", font=dict(family="Times New Roman", size=12)),  # Customize legend font
        xaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize x-axis tick font
        yaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  # Customize y-axis tick font
    )

    interactive_plot = fig.to_html(full_html=False)

    context = {
        'ticker': ticker,
        'window': window,
        'interactive_plot': interactive_plot,
    }
       
    return render(request, 'main/company_graph_aroon.html', context)


def render_news_and_sentiment(request):
    news_and_sentiment = Data("AMZN").get_news_and_sentiments_general()
    context = {
        'news_and_sentiment_general': news_and_sentiment
    }
    return render(request, 'main/home.html', context)


def render_topic_graph(request, number):
    news_and_sentiment = Data("AMZN").get_news_and_sentiments_general()
    n = news_and_sentiment[number]["topics"]
    keys = []
    values = []

    for dictionary in n:
        keys.append(dictionary["topic"])
        values.append(float(dictionary["relevance_score"]))
    

    fig = px.bar(x=keys, y=values,
                    labels={'x': 'Topic', 'y': 'Relevance Score'})

    fig.update_layout(
        width=1700,  
        font=dict(family="Times New Roman", size=14),  
        legend=dict(title_text="Legend", font=dict(family="Times New Roman", size=12)),  
        xaxis=dict(tickfont=dict(family="Times New Roman", size=12)), 
        yaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  
    )

    interactive_plot = fig.to_html(full_html=False)

    context = {
        'z' : zip(keys, values), 
        'interactive_plot': interactive_plot,
    }
       
    return render(request, 'main/topic_graph.html', context)


def render_sentiment_graph(request, number):
    news_and_sentiment = Data("AMZN").get_news_and_sentiments_general()
    n = news_and_sentiment[number]["ticker_sentiment"]
    keys = []
    values = []

    for dictionary in n:
        keys.append(dictionary["ticker"])
        values.append(float(dictionary["ticker_sentiment_score"]))
    

    fig = px.bar(x=keys, y=values,
                    labels={'x': 'Ticker', 'y': 'Ticker Sentiment Score'})

    fig.update_layout(
        width=1700,  
        font=dict(family="Times New Roman", size=14),  
        legend=dict(title_text="Legend", font=dict(family="Times New Roman", size=12)),  
        xaxis=dict(tickfont=dict(family="Times New Roman", size=12)), 
        yaxis=dict(tickfont=dict(family="Times New Roman", size=12)),  
    )

    interactive_plot = fig.to_html(full_html=False)

    context = {
        'z': zip(keys, values),
        'interactive_plot': interactive_plot,
    }
       
    return render(request, 'main/ticker_sentiment.html', context)
