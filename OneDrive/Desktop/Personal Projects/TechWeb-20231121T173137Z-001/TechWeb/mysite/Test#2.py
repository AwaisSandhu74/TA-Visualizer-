import requests

# Replace with your Alpha Vantage API key
api_key = 'YOUR_API_KEY'

# Define the endpoint URL for Alpha Intelligence News
base_url = 'https://www.alphavantage.co/query'
endpoint = 'ALPHA_NEWS'

# Define the parameters for the request
params = {
    'function': 'OVERVIEW',
    'symbol': 'AAPL',  # Replace with the stock symbol you want news for
    'apikey': api_key,
}

# Make the API request
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    news_data = response.json()  # Parse the JSON response
    # Now you can work with the news data as needed
    print(news_data)
else:
    print(f"Error: {response.status_code}")


    