import wikipedia as wp
import pandas as pd

def clean_data():
    html = wp.page("List of S&P 500 companies").html().encode("UTF-8")
    df = pd.read_html(html)[0]
    first_column = df.iloc[:, 0]
    first_column = list(first_column.to_string(index=False).split("  "))
    cleaned_tickers = []
    
    for item in first_column:
        tickers = item.split('\n')
        cleaned_tickers.extend([ticker.strip() for ticker in tickers if ticker.strip()])

    return cleaned_tickers


