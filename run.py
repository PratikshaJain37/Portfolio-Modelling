"""
run.py - run models here
@authors: Pratiksha Jain
"""
# --------------------------------- #

# Imports needed
from classes import Portfolio
from models import randomWeightsModel, weightedSumOptimizationModel, markowitzEfficientFrontierModel, optimizeRiskForReturnModel

# --------------------------------- #

# Initializing
stockNames = ["ONGC", "HDBK", "TISC"]
portfolio = Portfolio(stockNames)

# --------------------------------- #

# Running Various Models

model = randomWeightsModel(portfolio)
model = weightedSumOptimizationModel(portfolio)

model = markowitzEfficientFrontierModel(portfolio)
model = optimizeRiskForReturnModel(portfolio, 1.7)

model.runAlgorithm()
model.showGraph()

# --------------------------------- #