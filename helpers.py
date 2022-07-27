"""
helpers.py - helper function for loading historical data from investpy and pretty formatting

@authors: Pratiksha Jain
"""
# --------------------------------- #

# Imports needed
from re import T
import numpy as np
import pandas as pd
import investpy
import os
import warnings

warnings.filterwarnings("ignore")

# --------------------------------- #

DATAPATH = os.path.join(os.getcwd(), "stockDetails")

# --------------------------------- #

# Checks if stock is in investpy database
def verifyStock(stock):
    stocks = investpy.stocks.get_stocks_list(country='India')
    if not stock in stocks:
        raise Exception("Stock Ticker not found.")
    return True

# Check if we have already downloaded the csv file
def stockFileExists(stock):
    if os.path.exists(os.path.join(DATAPATH, stock)+'.csv'):
        return True
    else:
        return False

# Loads historical data of stock
def loadHistoricalData(stock, fromDate='30/04/2017', toDate='25/05/2022'):
    df = investpy.get_stock_historical_data(stock=stock,
                                        country='India',
                                        from_date=fromDate,
                                        to_date=toDate,
                                        interval="Monthly")
    df = df.drop(['Currency','Open',"High","Low","Volume"], axis=1)
    if not os.path.isdir(DATAPATH):
        os.mkdir(DATAPATH)

    df.to_csv(os.path.join(DATAPATH, stock)+'.csv')
    return df

# Loads stock and verifies it exists
def loadStock(stock):
    verifyStock(stock)
    if stockFileExists(stock):
        print("\nStock exists:: ",stock)
        # historicalData = loadHistoricalData(stock)
        historicalData = pd.read_csv(os.path.join(DATAPATH, stock)+'.csv', index_col="Date")
    else:
        print("Stock to be downloaded:: ",stock)
        historicalData = loadHistoricalData(stock)

    print(stock, ' loaded')
    return historicalData


# --------------------------------- #

# because i like this way of printing
def prettyPrint(risk, expectedReturn, weightCombination, stockNames, text):
    dictionary = {}
    dictionary['Returns'] = expectedReturn
    dictionary["Risks"] = risk

    for counter, ticker in enumerate(stockNames):
        dictionary[ticker+' weight'] = weightCombination[counter]

    prettyPrint = pd.DataFrame(dictionary, index=[""])
    
    print("\n",text)
    print(prettyPrint)


# --------------------------------- #

## TESTING ##


# --------------------------------- #
