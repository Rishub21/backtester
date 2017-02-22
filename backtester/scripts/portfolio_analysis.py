from portfolio_constructor import * # importing all the functions and libraries from our portfolio_constructor file
import numpy as np


def cumulative_return(closeprice_dataframe):
    return(closeprice_dataframe[-1]/closeprice_dataframe[0]) # this is the last day in our portfolio value data set / the first day => essentially our net return

def daily_returns(df): # where df is our portfolio value dataframe remember portfilio value dataframe is technically just a list of the end value of each day()
    dr = (df/df.shift(1)) - 1  #divide current day by day before
    dr = dr[1:]  # return first row on
    return dr

    """
    what this is doing is taking in the data the portfolio value dataframe and then dividng each column value by the one under it which is technically the next day so you can find out if you made daily returns or not
    .shift(1) shifts all indexes down by one
    we have to start from 1st row : because of the shift down our new 0 would technically be undefined
    """

def average_daily_returns(df):
    dr = daily_returns(df)
    return dr.mean() # we are not putting an axis parameter because by defaultit will go down and calculate the average for each row so we will know the average return for each day

def volatility(df):
    dr = daily_returns(df)
    return dr.std()


"""
The sharpe_Ratio is defined as the average portfolio return - the risk free rate and that quantitity divided by the standard deviation of returns on that portfolio
it is essentially how much return you make above the risk free rate (US treasury bonds) per unit of risk. It is used
to figure out the risk adjusted rate so you can understand of what you are getting into is actually smart, or is it just riskier
the higher the sharpe_Ratio the better, but we like to keep the minimum passing at 1

BOTTOM LINE : HOW MUCH BETTER YOUR PORTFILIO IS DOING THAN RISK FREE INVESTMENT
"""

def Sharpe_Ratio(df,rf): # where rf is the risk free rate, the rate of the US treasury bond
    sample = 252 # trading days per year
    average = (average_daily_returns(df) - rf).mean() # we are taking the average return of each stock, subtracting the risk free rate, and then taking the average of that to get our final average
    vol = volatility(df)
    sharpe_ratio = (average / vol)
    annualized_sharp_ratio = np.sqrt(sample) * sharpe_ratio
    return annualized_sharp_ratio

"""
The beta is a HISTORICAL measure of how volatile a stock or portfolio is compared to the market as a whole. Market gains x beta = estimated movement of the stock or portfolio.
High beta means higher risk and potentially higher reward
"""

"""
Honestly the Treynor_Ratio is alot like the Sharpe Ratio but instead of how much better than the risk free rate per unit of risk,
it calculates how much better than the entire equity market, or a subselection of the equity market per unit of risk, you divide by
beta not standard deviation  to find it

BOTTOM LINE : HOW MUCH BETTER YOUR PORTFILIO IS DOING THAN EQUITY MARKET AS A whole

"""
def BTR(pv,comp,start,end,shares,cash,rf=0):
    """
    pv = portfolio value dataframe
    comp =  bench march , you can use a specific set of tickers, or the entire index as a whole
    """
    tickers = [comp]
    comp_adj_close = get_adjusted_close(tickers,start,end)
    comp_pv = Portfolio_Value(comp_adj_close,shares,cash) # portfolio value of comp stock selection
    comp_returns = daily_returns(comp_pv) # daily returns is a list of the percentage gain of each day
    port_returns = daily_returns(pv) # where pv is our portfolio
    covariance = np.cov(port_returns,comp_returns)[0][1]
    variance = np.var(comp_returns)
    beta = covariance/variance
    Treynor_Ratio = (cumulative_returns(pv) - rf)/beta
    return beta,Treynor_Ratio
