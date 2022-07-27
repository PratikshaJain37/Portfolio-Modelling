"""
run.py - run models here
@authors: Pratiksha Jain
"""
# --------------------------------- #

# Imports needed
from classes import Portfolio
from models import 

# --------------------------------- #

# Initializing
stockNames = ["ONGC", "HDBK", "TISC"]
portfolio = Portfolio(stockNames)

for stock in stockNames:
    portfolio.stockData[stock].plotReturn() # make neater lol

# --------------------------------- #