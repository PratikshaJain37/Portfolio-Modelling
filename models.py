"""
models.py - code models here
@authors: Pratiksha Jain
"""
# --------------------------------- #

# Imports needed
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from helpers import prettyPrint
from cvxopt import solvers

solvers.options['show_progress'] = False
np.random.seed(42)
warnings.filterwarnings("ignore")


# --------------------------------- #

class randomWeightsModel:

    def __init__(self, portfolio) -> None:
        self.portfolio = portfolio
    
    def runAlgorithm(self):
        # def findBestReturnWithMinimumRisk(x, y, weightCombinations):
        dictionary = {}
        dictionary['Returns'] = y
        dictionary["Risks"] = x
        dictionary["Weights"] = weightCombinations

        for counter, ticker in enumerate(self.portfolio.stockNames):
            dictionary[ticker+' weight'] = [w[counter] for w in weightCombinations]

        portfolioDf = pd.DataFrame(dictionary)
        minRiskPortfolio = portfolioDf.iloc[portfolioDf['Risks'].idxmin()]

        plt.plot(minRiskPortfolio["Risks"], minRiskPortfolio["Returns"],'r-p', label="Minimum risk with randomly generated points")

        prettyPrint(
            minRiskPortfolio["Risks"], 
            minRiskPortfolio["Returns"], 
            minRiskPortfolio["Weights"], 
            self.portfolio.stockNames, 
            "Point of minimum risk with randomly generated points:")


    def showGraph(self):
        pass

    def prettyPrint(self):
        pass

    def generateWeights(n):
        weightCombinations = [generateRandomWeights(len(stockNames)) for _ in range(n)]
        return weightCombinations

    def generateRandomWeights(size):
        # weights are between 0 and 1 and sum to 1
        weights = np.random.rand(size)
        weights = weights/sum(weights)
        return weights




def plotReturns(weightCombinations, portfolio):
    x = [] 
    y = []
    xEdge = []
    yEdge = []
    for weights in weightCombinations:
        portfolio.assignWeights(weights)
        x.append(portfolio.calculatePortfolioRisk())
        y.append(portfolio.calculatePortfolioReturn())
    for weights in [np.array([0,0,1]), np.array([0,1,0]), np.array([1,0,0])]:
        portfolio.assignWeights(weights)
        xEdge.append(portfolio.calculatePortfolioRisk())
        yEdge.append(portfolio.calculatePortfolioReturn())
    
    findBestReturnWithMinimumRisk(x,y, weightCombinations)
    # plt.scatter(x,y, s=10)
    # plt.scatter(xEdge, yEdge, s=10, color='r')
    # plt.show()

    return x, y, xEdge, yEdge




weightCombinations = generateWeights(1000)
minRisk, minReturn = portfolio.calculateMinimumVariancePoint()

x, y, xEdge, yEdge = plotReturns(weightCombinations, portfolio)
plt.scatter(x,y,color='g', s=5, label="Randomly generated weights")
plt.scatter(xEdge, yEdge, color='r',marker="*", label="Individual Stocks")
plt.plot(minRisk, minReturn, 'r-s', label="Minimum risk (calculated)")
# plt.ylabel('mean')
# plt.xlabel('std')
# plt.show()


# --------------------------------- #