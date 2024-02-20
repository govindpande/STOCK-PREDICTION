import pandas as pd
import streamlit as st
#import altair as alt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objs as go
from prophet import Prophet
import ydata_profiling
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import numpy as np


st.sidebar.header("Developed by Govind Pande")
st.sidebar.write("Guided by Dr Cheng")


# Update page selection to include "Weekly Volatility & ^INDIAVIX"
page_select = st.sidebar.selectbox("Choose Section", ["Project Overview", "Stock Visualizations", "Share Holders Visualization", "Compare Stocks", "Price Prediction", "Bring your own data","Weekly Volatility & ^INDIAVIX", "Weekly Volatility Prediction with Prophet"])



def mainn():
  if page_select== "Project Overview":

    st.title("Stock Price Analysis and Price Preddiction Project")

    st.header("Introduction:")
    st.write("The main objective of this project is to build a data visualization web application using Streamlit that can help users visualize and analyze stock market data. The project is divided into four main sections, each focusing on a specific aspect of stock market analysis. These sections include stock visualization, shareholder visualization, compare stocks, and price prediction. In this project, we have used various libraries such as yfinance for getting the data, Facebook Prophet for price prediction, and Plotly graph objects and Matplotlib for visualization.")

    st.header("Stock Visualization:")
    st.write("The stock visualization section allows users to visualize the historical performance of a particular stock. The user can select the stock they are interested in from a dropdown menu, and the application will display a line chart of the stock's performance over a specified period. The user can also customize the chart by selecting various options such as the chart type, timeframe, and whether to include volume data.")

    st.header("Shareholder Visualization:")
    st.write("The shareholder visualization section allows users to visualize the distribution of a company's shareholder base. The user can select a company from a dropdown menu, and the application will display a pie chart that shows the percentage of ownership for each shareholder. The user can also filter the data by the shareholder's country, size of the holding, or type of shareholder.")

    st.header("Compare Stocks:")
    st.write("The compare stocks section allows users to compare the performance of multiple stocks side-by-side. The user can select up to five stocks from a dropdown menu, and the application will display a line chart that shows the performance of each stock over a specified period. The user can also customize the chart by selecting various options such as the chart type, timeframe, and whether to include volume data.")

    st.header("Price Prediction:")
    st.write("The price prediction section allows users to predict the future price of a particular stock. The user can select the stock they are interested in from a dropdown menu, and the application will display a line chart of the stock's performance over a specified period. The user can also select a timeframe for the prediction and adjust the confidence interval. The application uses Facebook Prophet, a forecasting library, to generate the predictions.")

    st.header("Conclusion:")
    st.write("Overall, this project aims to provide users with a comprehensive visualization and analysis tool for stock market data. The application is designed to be user-friendly and intuitive, allowing users to easily explore and analyze stock market data. By leveraging various libraries such as yfinance, Facebook Prophet, Plotly graph objects, and Matplotlib, I have created an application that provides users with a powerful set of tools for stock market analysis.")







  if page_select== "Stock Visualizations":
    ticker = st.sidebar.text_input('Enter a stock ticker (e.g. AAPL)',value="GOOGL")
    start_date = st.sidebar.date_input("Select start date", value=pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input("Select end date", value=pd.to_datetime('today'))
    
    df = yf.download(ticker, start=start_date, end=end_date)

    chart_type = st.selectbox("Select chart type", ["Line Chart", "Candlesticks"])

    # If the user selects a line chart
    if chart_type == "Line Chart":
      # Create a line chart using Plotly
      fig = go.Figure()
      fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'))

      # Set the chart title and axis labels
      fig.update_layout(title=f"{ticker} Close Price", xaxis_title='Date', yaxis_title='Price')

      # Display the chart in Streamlit
      st.plotly_chart(fig)
      st.write(df)




    # If the user selects a bar chart
    if chart_type == "Candlesticks":
        def get_stock_data(ticker, freq, start_date, end_date):
          data = yf.download(ticker, interval=freq, start=start_date, end=end_date)
          return data
        # Define a dictionary to map frequency strings to yfinance intervals
        interval_map = {
            "1 day": "1d",
            "1 week": "1wk",
            "1 month": "1mo"
        }

        # Ask the user to enter a stock ticker and select a frequency, start date, and end date
        #ticker = st.text_input('Enter a stock ticker (e.g. AAPL)')
        freq = st.selectbox("Select candle frequency", options=list(interval_map.keys()))
        #start = st.date_input("Select start date", value=pd.to_datetime('2020-01-01'))
        #end = st.date_input("Select end date", value=pd.to_datetime('today'))

        # Display the selected stock ticker, frequency, start date, and end date
        if ticker:
            st.write(f"You selected: {ticker}")
            st.write(f"Candle frequency: {freq}")
            st.write(f"Start date: {start_date}")
            st.write(f"End date: {end_date}")
            interval = interval_map[freq]
            stock_data = get_stock_data(ticker, interval, start_date, end_date)
            fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                                 open=stock_data['Open'],
                                                 high=stock_data['High'],
                                                 low=stock_data['Low'],
                                                 close=stock_data['Close'])])
            st.plotly_chart(fig)

      
  if page_select == "Share Holders Visualization":
        pie_type = st.selectbox("Select type", ["Institutional Ownership Pie Chart","View Shareholders Data",])
        ticker = st.sidebar.text_input('Enter a stock ticker symbol:', 'AAPL')
        

        def get_institutional_holders(ticker):
                stock = yf.Ticker(ticker)
                holders = stock.institutional_holders
                institutional_holders = holders
                return institutional_holders

        if pie_type=="View Shareholders Data":
            
            df1 = get_institutional_holders(ticker)
            st.write(df1)


        if pie_type=="Institutional Ownership Pie Chart":

          st.title('Institutional Shareholders Pie Chart')
          #ticker = st.sidebar.text_input('Enter a stock ticker symbol:', 'AAPL')

          institutional_holders = get_institutional_holders(ticker)

          if institutional_holders.empty:
              st.warning(f'No institutional holders data found for {ticker}.')
          else:
              st.write(f'Institutional holders data for {ticker}.')
              labels = institutional_holders['Holder'].tolist()

              #use both options for the final dashboard
              values = institutional_holders['% Out'].tolist()
            
              fig = go.Figure(data=[go.Pie(labels=labels, values=values, textfont=dict(size=20, color='white'),textposition='inside', textinfo='label+percent')])
              fig.update_layout(width=800, height=600)


              st.plotly_chart(fig)



  if page_select== "Compare Stocks":
    # Define a list of stock symbols to plot
    symbols = ['AAPL', 'AMZN', 'GOOG', 'MSFT', 'TSLA', 'NVDA', 'JNJ', 'V', 'PG']

    # Allow the user to input new symbols to plot
    new_symbols = st.text_input('Enter new symbols to plot (separated by commas)')
    if new_symbols:
        symbols.extend(new_symbols.split(','))

    # Allow the user to select the stocks to plot using a multiselect widget
    selected_symbols = st.multiselect('Select stocks to plot', symbols,  default=['AAPL','MSFT'])

    # Define Streamlit widgets for the start and end dates
    start_date = st.sidebar.date_input('Start date', value=pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('End date', value=pd.to_datetime('today'))

    # Load the stock data for each selected symbol into a Pandas DataFrame
    dfs = []
    for symbol in selected_symbols:
        df = yf.download(symbol, start=start_date, end=end_date)
        df['Symbol'] = symbol
        dfs.append(df)
    df = pd.concat(dfs)

    # Create a Plotly figure for each selected stock symbol
    figures = []
    for symbol in selected_symbols:
        df_symbol = df[df['Symbol'] == symbol]
        fig = go.Figure(data=go.Scatter(x=df_symbol.index, y=df_symbol['Close'], name=symbol))
        figures.append(fig)

    # Combine all figures into a single Plotly figure
    fig_combined = go.Figure()
    for fig in figures:
        for trace in fig.data:
            fig_combined.add_trace(trace)

    # Set the chart title and axis labels
    fig_combined.update_layout(title='Stock Prices', xaxis_title='Date', yaxis_title='Price')

    # Show the chart in Streamlit
    st.plotly_chart(fig_combined)





  if page_select== "Price Prediction":

    plt.style.use('dark_background') # Set plot style to dark background

    # Get user input for stock symbol and time period
    symbol = st.sidebar.text_input("Enter stock symbol (e.g. AAPL)", value="AAPL")
    start_date = st.sidebar.date_input("Enter start date", value=pd.to_datetime('2021-01-01'))
    end_date = st.sidebar.date_input("Enter end date", value=pd.to_datetime('today'))
    forecast_days = st.sidebar.slider("Select number of days to forecast", min_value=1, max_value=365, value=30)

    # Download stock data
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    # Prepare data for Prophet
    df = pd.DataFrame()
    df['ds'] = stock_data.index
    df['y'] = stock_data['Close'].values

    # Train Prophet model
    m = Prophet(daily_seasonality=True)
    m.fit(df)

    # Predict future prices
    future = m.make_future_dataframe(periods=forecast_days)
    fcst = m.predict(future)

    # Plot predicted prices
    fig, ax = plt.subplots(figsize=(12, 8)) # Set figure size to 12x8 inches
    ax.plot(df['ds'], df['y'], label='Actual')
    ax.plot(fcst['ds'], fcst['yhat'], label='Predicted')
    ax.fill_between(fcst['ds'], fcst['yhat_lower'], fcst['yhat_upper'], alpha=0.3, color='gray')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.set_title('Stock Price Prediction')
    ax.legend()

    # Format x-axis to show date labels vertically
    ax.tick_params(axis='x', rotation=40)
    ax.xaxis_date()  # Treat x-axis values as dates

    st.pyplot(fig)

    
  if page_select== "Bring your own data":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    #dataf = pd.read_csv(uploaded_file)
    if uploaded_file is not None:
      dataf = pd.read_csv(uploaded_file)
      if st.button("Generate Report"):
        pr = dataf.profile_report()
        st_profile_report(pr)
    
# Function to calculate weekly volatility for each week
def calculate_weekly_volatility(df):
    weekly_returns = df['Close'].resample('W').last().pct_change().dropna()
    weekly_volatility = weekly_returns * np.sqrt(52)  # Removing the annualization
    return weekly_volatility
    

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df
# Function to fetch ^INDIAVIX data
def fetch_indiavix_data(start_date, end_date):
    vix = yf.download('^VIX', start=start_date, end=end_date)
    return vix['Close'].resample('W').last()

if page_select == "Weekly Volatility & ^INDIAVIX":
    st.title("Weekly Volatility of Stock and ^INDIAVIX Comparison")

    # User inputs for stock ticker and date range
    ticker = st.sidebar.text_input('Enter a stock ticker (e.g. TCS)', value="TCS")
    start_date = st.sidebar.date_input("Select start date", value=pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input("Select end date", value=pd.to_datetime('today'))

    if ticker:
        # Fetch stock and ^INDIAVIX data
        df_stock = fetch_stock_data(ticker, start_date, end_date)
        df_indiavix = fetch_indiavix_data(start_date, end_date)

        if not df_stock.empty:
            # Calculate weekly volatility for the stock
            weekly_volatility_stock = calculate_weekly_volatility(df_stock)

            # Plot weekly volatility for the stock
            fig_stock = go.Figure()
            fig_stock.add_trace(go.Scatter(x=weekly_volatility_stock.index, y=weekly_volatility_stock, mode='lines+markers', name=f'{ticker} Weekly Volatility'))
            fig_stock.update_layout(title=f"Weekly Volatility for {ticker}", xaxis_title='Date', yaxis_title='Volatility', legend_title='Legend')
            st.plotly_chart(fig_stock)

        if not df_indiavix.empty:
            # Plot ^INDIAVIX
            fig_indiavix = go.Figure()
            fig_indiavix.add_trace(go.Scatter(x=df_indiavix.index, y=df_indiavix, mode='lines', name='^INDIAVIX'))
            fig_indiavix.update_layout(title="^INDIAVIX Weekly Close", xaxis_title='Date', yaxis_title='^INDIAVIX Close', legend_title='Legend')
            st.plotly_chart(fig_indiavix)
        else:
            st.write("No data available for the selected ticker or ^INDIAVIX.") 
        if not df_stock.empty:
          # Calculate weekly volatility for the stock without annualizing
          weekly_returns = df_stock['Close'].pct_change().dropna()  # Daily returns
          weekly_volatility = weekly_returns.resample('W').std() * 100  # Convert to percentage
      
          # Prepare weekly volatility for plotting
          weekly_volatility = weekly_volatility.dropna()  # Ensure no NaN values
      
          # Plot weekly volatility for the stock
          fig_stock = go.Figure()
          fig_stock.add_trace(go.Scatter(x=weekly_volatility.index, y=weekly_volatility, mode='lines+markers', name=f'{ticker} Weekly Volatility'))
          fig_stock.update_layout(title=f"Weekly Volatility for {ticker} (Percentage)", xaxis_title='Date', yaxis_title='Weekly Volatility (%)', legend_title='Legend')
          st.plotly_chart(fig_stock)

if page_select == "Weekly Volatility Prediction with Prophet":
    plt.style.use('dark_background')  # Set plot style to dark background

    # Get user input for stock symbol and time period
    symbol = st.sidebar.text_input("Enter stock symbol (e.g. AAPL)", value="AAPL")
    start_date = st.sidebar.date_input("Enter start date", value=pd.to_datetime('2021-01-01'))
    end_date = st.sidebar.date_input("Enter end date", value=pd.to_datetime('today'))
    forecast_days = st.sidebar.slider("Select number of days to forecast", min_value=1, max_value=365, value=30)

    # Download stock data
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    # Ensure the index is datetime for resampling
    stock_data.index = pd.to_datetime(stock_data.index)

    # Calculate daily returns
    daily_returns = stock_data['Close'].pct_change().dropna()

    # Calculate weekly volatility
    weekly_volatility = daily_returns.resample('W').std() * np.sqrt(52)

    # Prepare data for Prophet
    df_prophet = pd.DataFrame({'ds': weekly_volatility.index, 'y': weekly_volatility.values})

    # Train Prophet model
    m = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=True)
    m.fit(df_prophet)

    # Predict future volatility
    future = m.make_future_dataframe(periods=forecast_days, freq='W')
    fcst = m.predict(future)

    # Plot predicted volatility
    fig = m.plot(fcst)
    plt.title('Weekly Volatility Prediction')
    plt.ylabel('Volatility')
    plt.xlabel('Date')

    # Show the plot in Streamlit
    st.pyplot(fig)




def main():
  mainn()

  ##########
  #pr = df.profile_report()

  #st_profile_report(pr)

main()
