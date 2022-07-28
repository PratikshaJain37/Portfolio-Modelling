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
model.runAlgorithm()
model.showGraph()

# model = weightedSumOptimizationModel(portfolio)
# model.runAlgorithm()
# model.showGraph()

# model = markowitzEfficientFrontierModel(portfolio)
# model.runAlgorithm()
# model.showGraph()

# model = optimizeRiskForReturnModel(portfolio, 1.7)
# model.runAlgorithm()
# model.showGraph()

# --------------------------------- #