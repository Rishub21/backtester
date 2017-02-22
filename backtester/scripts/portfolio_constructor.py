import pandas_datareader.data as web
import os
import datetime
import time
from urllib2 import Request, urlopen
import pandas as pd
import matplotlib.pyplot as plt

""" 1)get adjusted close reads the data for each stock with the DataRader and then creates a dataframe which is just the adj_close of every stock
    2) portfolio value => takes this lasta data frame and standardizes it and applies weights so we can actually figure out how much our value shifted
    3) The porfolio value is what we are going to use in our cumulative_return function """


current_directory = os.getcwd()
data_directory = str(current_directory) + "/stock_data"

if not os.path.exists(data_directory):  # will make the sub directory for stock data if its not already there, good for initally running
    os.makedirs(data_directory)

def get_adjusted_close(tickers,start,end):
    d = {}
    for ticker in tickers:
        d[ticker] = web.DataReader(ticker,"yahoo",start,end)
    pan = pd.Panel(d)
    df_adj_close = pan.minor_xs('Adj Close') # panel will only hold the adjusted close data for each stock, this is essentially a dataframe that has the categories as the stocks and the values as just the close price. We essentially extracted the close price column from every previous dataframe to make this one
    # keep in mind that it is this close price data frame we just made that is going to assist us in calculating the portfolio value
    #print "THIS IS D"
    #print d
    return df_adj_close


def plot_stocks(stock_frame,show='no'):
    plt.style.use('ggplot')
    stock_frame.plot()
    plt.title('Stock Performance')
    plt.ylabel('Stock Price')
    plt.xlabel('Date')
    plt.legend(loc='upper left', prop={'size':6}, bbox_to_anchor=(1,1))
    plt.tight_layout(pad=7)
    if show == 'yes':
        plt.show()
    plt.savefig('stock_performance.png')
    return

def portfolio_Value(stock_frame, shares_list, initial_investment):
    # shares list will be the number of stocks for each ticker
    weights = []

    for quantitiy in shares_list:
        weights.append(quantitiy/(float(sum(shares_list))))

    standardized = stock_frame/ stock_frame.ix[0] # dividing every single column (stock )of the data frame by the first stock so you have a standard to go off of
    weighted_stand = standardized * weights # THIS IS STILL A DATA FRAME, multiplying that standardized data frame by the proportion of the total portfolio that
    cash_return = weighted_stand * initial_investment # this is a data frame that takes those propotions and multiplies with the scalar that was our inital cash
    series_rowsum = cash_return.sum(axis = 1) # you are just adding up each row of stocks at that point of time and making a series
    # again please remember that axis one means horiztonal across the columns
    #print series_rowsum
    return series_rowsum # remember this is a series, not a 2d dataframe

def plot_portfolio(value_rowsum, show = "no"):
    plt.style.use("ggplot")
    value_rowsum.plot()
    plt.title("Portfolio Performance")
    plt.ylabel("Total Value")
    plt.xlabel("Date")
    plt.legend(loc='upper left', prop={'size':6}, bbox_to_anchor=(1,1))
    if show == 'yes':
        plt.show()
    plt.savefig('portfolio_performance.png')
    return



def scraperFundamental(tickers, metrics):
    fundamental_dict = { 'bid':'b','close':'p','open':'o','dividend_yield':'y','dollar_change':'c1','percent_change':'p2',
         'days_low':'g','days_high':'h','1_year_target_price':'t8','200_day_ma_dollar_change':'m5',
         '200_day_ma_percent_change':'m6','50_day_ma_dollar_change':'m7','50_day_ma_percent_change':'m8',
        '200_day_ma':'m4','50_day_ma':'m3','revenue':'s6','52_week_high':'k','52_week_low':'j','52_week_range':'w',
         'market_cap':'j1','float_shares':'f6','name':'n','symbol':'s','exchange':'x','shares_outstanding':'j2',
         'volume':'v','ask_size':'a5','bid_size':'b6','last_trade_size':'k3','average_daily_volume':'a2','eps':'e',
         'current_eps_estimate':'e7','next_year_eps_estimate':'e8','next_quarter_eps_estimate':'e9','book_value':'b4',
         'ebitda':'j4','price_to_sales':'p5','price_to_book':'p6','pe':'r','peg':'r5','short_ratio':'s7'
    }  # these values are actually code that Yahoo finance gives us to grab the financial data, the keys are what statistic those "codes" stand for

    #  yes you can type in individual metrics like p5 or price_to_book but if its all then we should know to include all of them

    if metrics == "all":
        codes = fundamental_dict.values()
        metrics = fundamental_dict.keys()
    else :
        for metric in metrics :
            codes = fundamental_dict[metric]

    ticker_dictionary = {}
    metric_dictionary= {}

    count = 1
    for ticker in tickers:
        for metric in metrics :
            link = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (ticker, metric) # will fill in the %s places
            response = urlopen(link) # makes a response object
            content = response.read() # content now includes all the html of the response
            metric_dictionary[metric] = content

        ticker_dictionary[ticker] = metric_dictionary
        metric_dictionary = {}
        count  +=1
        if count % 50 ==0 :
            time.sleep(10)
    return ticker_dictionary



def downloadHistoric(tickers, startDate, endDate, all_Data = False):
    count  = 1
    if all_Data == True :
        end= datetime.datetime.now()
        end = '%s-%s-%s' % (end.month,end.day,end.year)
        start = '01-01-1970' # the earliest that Yahoo finance has trading data for

    # creating a directory just for all the stock data
    data_dict = {}
    for ticker in tickers:
        filename = data_directory + "/" + ticker + ".csv"
        data_dict[ticker] = web.DataReader(ticker, "yahoo", start, end)
        data_dict[ticker].to_csv(filename)
        count +=1
        if count % 50 ==0:
            time.sleep(10) # this will ensure that after every stocks our program  takes a 10 second
    return

if __name__ == '__main__': # testing populator method
    tickers = ['AAPL','BAC','GILD','MSFT']
    start = '2014-01-01'
    end = '2016-12-21'
    downloadHistoric(tickers, start, end, all_Data=True)
    metrics = ['pe','peg','average_daily_volume','eps']
    test = scraperFundamental(tickers, metrics)
    df_adj_close = get_adjusted_close(tickers,start,end)
    print df_adj_close
    print df_adj_close["AAPL"]["2014-01-02"]
    plot_stocks(df_adj_close,show='yes')
    sharelist = [100,100,100,100]
    initialcash = 100000
    portval = portfolio_Value(df_adj_close, sharelist, initialcash )
    #print portval.values
    plot_portfolio(portval,show = "yes")
