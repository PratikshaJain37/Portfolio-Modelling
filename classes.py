"""
classes.py - for stock, portfolio classes and functions
@authors: Pratiksha Jain
"""
# --------------------------------- #

# Imports needed
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from helpers import loadStock, prettyPrint
import cvxopt as opt
from cvxopt import solvers

solvers.options['show_progress'] = False
np.random.seed(420)
warnings.filterwarnings("ignore")

# --------------------------------- #

class Stock:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.historicalData = loadStock(ticker)
        self.historicalReturns = self.historicalData.pct_change()[1:]

        self.calculateRisk()
        self.calculateReturn()


    def calculateRisk(self):
        self.risk = self.historicalReturns.std()[0]
        print(f"{self.ticker:6s} Risk   : {self.risk:.6f}")
        return self.risk
    
    def calculateReturn(self):

        self.expectedReturn = self.historicalReturns.mean()[0]
        print(f"{self.ticker:6s} Return : {self.expectedReturn:.6f}")
        return self.expectedReturn
    
    def plotReturn(self):
        plt.plot(self.historicalReturns)
        plt.show()

# --------------------------------- #


class Portfolio:

    def __init__(self, stockNames) -> None:
        self.stockNames = stockNames
        self.numberOfAssets = len(stockNames)
        self.stockData = {stock:Stock(stock) for stock in stockNames}
        self.dictionary = {}

        self.generateIndividualReturns()
        self.generateIndividualRisks()
        self.generateHistoricalData()
        self.calculateCovarianceMatrix()
        self.calculateMatrixM()
        self.calculateMatrixE()


    def assignWeights(self, weights):
        # check -> self.weights is numpy matrix
        # and that its shape is nx1
        if type(weights) == np.ndarray:
            if weights.shape == (self.numberOfAssets,):
                self.weights = weights
            elif weights.shape == (self.numberOfAssets,1):
                self.weights = weights.reshape((self.numberOfAssets,))
            else:
                print("Wrong shape of weights: ", weights.shape, " instead of ")
    
    def generateIndividualReturns(self):
        self.individualReturns = [self.stockData[stock].expectedReturn for stock in self.stockNames]

    def generateIndividualRisks(self):
        self.individualRisks = [self.stockData[stock].expectedReturn for stock in self.stockNames]

    def generateHistoricalData(self):
        self.stockHistoricalData = pd.concat(
            [self.stockData[stock].historicalReturns
            for stock in self.stockNames], 
            axis=1)
        
    def calculateCovarianceMatrix(self):
        stockHistoricalData = self.stockHistoricalData.to_numpy().T
        self.covMatrix = np.cov(stockHistoricalData)
        # print(covMatrix)
    
    def calculateMinimumVariancePoint(self):
        e = self.e
        cinve = self.calculateCinve().reshape((self.numberOfAssets,))
        weightMatrix = cinve/(np.matmul(e.T, cinve)[0])
        self.assignWeights(weightMatrix)
        minRisk = self.calculatePortfolioRisk()
        minReturn = self.calculatePortfolioReturn()

        prettyPrint(minRisk, minReturn, weightMatrix, self.stockNames,"Point of minimum risk (Calculated)")

        return minRisk, minReturn 

    def calculatePortfolioRisk(self, weights=None):
        if weights is not None:
            w = np.asmatrix(weights)
        else:
            w = np.asmatrix(self.weights)
        c = np.asmatrix(self.covMatrix)
        portfolioVar = w * c * w.T
        # print(portfolioVar.shape)
        portfolioVols = np.sqrt(portfolioVar)[0,0]
        return portfolioVols

    def calculatePortfolioReturn(self, weights=None):
        if weights is not None:
            return np.dot(weights, self.individualReturns) 
        else:
            return np.dot(self.weights, self.individualReturns) 
        

    def calculatePortfolioCharacteristics(self, weightCombinations, sharpeRatio=False):
        x = [] 
        y = []
        for weights in weightCombinations:
            self.assignWeights(weights)
            x.append(self.calculatePortfolioRisk())
            y.append(self.calculatePortfolioReturn())
        
        if not sharpeRatio:
            return x, y
        else:
            sharpe = [x[i]/y[i] for i in range(len(x))]
            return x,y, sharpe


    #  expected return vector 
    def calculateMatrixM(self):
        self.m = np.array(self.individualReturns)

    # unit vector
    def calculateMatrixE(self):
        self.e = np.ones((self.numberOfAssets,1))

    def calculateCinvm(self):
        return np.matmul(np.linalg.inv(self.covMatrix),self.m)

    def calculateCinve(self):
        return np.matmul(np.linalg.inv(self.covMatrix),self.e)

# --------------------------------- #
