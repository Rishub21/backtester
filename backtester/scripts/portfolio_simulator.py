import csv
from portfolio_constructor import *
from portfolio_analysis import *


def simulation(orders, start, end, starting_cash):
    symbols = []
    order_list = []
    with open (orders, "r") as inlist:
        for index, row in enumerate(inlist):
            row = row.split(",")
            order_list.append(row)

        order_list.pop(0)
        #print order_list
        # essentially order_list is a list of lists, with each sublist being the info of one trade
        for stocklist in order_list:
            symbols.append(str(stocklist[1]))
        symbols = list(set(symbols)) # we want the symbols to still be a list but we want it to be only unique elements, hence the set() function
        dates_list = pd.date_range(start, end) # default frequency will naturally be by day
        close_df = get_adjusted_close(symbols, start, end)
        close_df["cash"] = 1.0
        df_trades = close_df.copy()

        df_trades[:] = 0 # [:] all columns

        for stocklist in order_list:
            date = pd.to_datetime(str(stocklist[0]))
            if date in dates_list:
                symbol = stocklist[1]
                trade = stocklist[2] # whether its a buy or a sell
                shares = int(stocklist[3])
            if trade == "SELL":
                shares = shares * -1
            df_trades[symbol][date] = df_trades[symbol][date] + shares
            df_trades["cash"][date] = df_trades["cash"][date] + -1*(df_trades[symbol][date] * close_df[symbol][date])
            # think of it like this, df_trades[symbol][date] = quantity of shares in transaction
            #                        df[symbol][date] = price of each share, remember df is just our adjusted close dataframe
            df_holdings = get_adjusted_close(symbols,start,end) # another adjusted close price dataframe
            df_holdings['cash'] = 1.0
            df_holdings[:] = 0 # setting all prices to zero
            df_holdings['cash'][start] = starting_capital # initial cash = our well initial starting cash

            for stocklist in order_list:
                date=  pd.to_datetime(str(stocklist[0]))
                if date in dates_list :
                    symbol = stocklist[1]
                df_holdings[symbol][date] = df_holdings[symbol][date]+df_trades[symbol][date]
                df_holdings['cash'][date] = df_holdings['cash'][date] + -1*(df_holdings[symbol][date]* close_df[symbol][date])

        df_holdings = df_holdings.cumsum()
        df_value = df_holdings*close_df
        portvals = df_value.sum(axis=1)
    return portvals

if __name__ == "__main__":
    f = 'orders.csv'
    start = '2011-01-05'
    end = '2011-12-20'
    starting_capital = 100000
    pv = simulation(f,start,end,starting_capital)
    print pv
    cr = cumulative_return(pv)
    dr = daily_returns(pv)
    adr = average_daily_returns(pv)
    vol = volatility(pv)
    sr = Sharpe_Ratio(pv,.5)
    print '------- Performance -------\n'
    print 'Cumulative Return: ' + str(cr) +'\n'
    print 'Daily Returns: \n'
    print dr
    print '\n'
    print 'Average Daily Return:' + str(adr) + '\n'
    print 'Volatility: ' + str(vol) + '\n'
    print 'Sharpe Ratio: ' + str(sr) + '\n'
