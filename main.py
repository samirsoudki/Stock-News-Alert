STOCK = "TSLA"
Stock_2 = "NTDOY"
COMPANY_NAME = "Tesla Inc"
company_name_2 = "Nintendo CO Ltd"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
import os
import requests
import datetime as dt
from twilio.rest import Client
account_sid = "ACc35916683193c0054bc09ddfea632c5c"
auth_token = os.environ.get("auth_token")
phone_number_us = "+18508163986"
phone_number_ua = "+380992016236"
today = dt.datetime.now()
day = (today.day - 1)
month = (f"{today.month}")
year = (today.year)
stock_key = os.environ.get("stock_key")
stock_news_key = os.environ.get("stock_news_key")
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={Stock_2}&apikey={stock_key}'
r = requests.get(url)
data = r.json()
data_date = data.get("Time Series (Daily)")

yesterday=f"{year}-0{month}-{day}"
data_date_11 = data_date.get(yesterday)
data_11_close_price = float(data_date_11.get("4. close"))
before_yesterday = f"{year}-0{month}-{day-1}"
data_date_10 = data_date.get(before_yesterday)
data_10_close_price = float(data_date_10.get("4. close"))
data_results = data_11_close_price - data_10_close_price
data_results_percentage = (data_results/data_11_close_price)*100
data_results_percentage_new = '{:,.2f}'.format(abs(data_results_percentage))

params_news = {
    "sources": "bloomberg",
    "q": company_name_2,
    "apiKey": stock_news_key
}

response = requests.get(url=NEWS_ENDPOINT, params=params_news)
response.raise_for_status()
data_news = response.json()
data_news_articles = data_news.get("articles")
news_title = data_news_articles[0].get("title")
news_description = data_news_articles[0].get("description")
client = Client(account_sid, auth_token)
if data_results_percentage < 0:
    message = client.messages \
        .create(
        body=f"{Stock_2}: 🔻{data_results_percentage_new}%\n\nTitle:{news_title}\n\nDescription:{news_description}",
        from_=phone_number_us,
        to=phone_number_ua
    )

    print(message.sid)
else:
    message = client.messages \
        .create(
        body=f"{Stock_2}: 🔺{data_results_percentage_new}%\n\nTitle:{news_title}\n\nDescription:{news_description}",
        from_=phone_number_us,
        to=phone_number_ua
    )

    print(message.sid)






