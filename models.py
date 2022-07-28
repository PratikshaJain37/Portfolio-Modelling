"""
models.py - code models here
@authors: Pratiksha Jain
"""
# --------------------------------- #

# Imports needed
from cProfile import label
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from helpers import prettyPrint
from cvxopt import solvers
from classes import Portfolio
import cvxopt as opt
from scipy.optimize import minimize

solvers.options['show_progress'] = False
np.random.seed(42)
warnings.filterwarnings("ignore")


# --------------------------------- #

class portfolioModel:

    def __init__(self, portfolio) -> None:
        self.portfolio = portfolio

    def runAlgorithm(self, numberOfRandomDataPoints=1000):
        self.weightCombinations = self.generateWeights(numberOfRandomDataPoints, self.portfolio.numberOfAssets)

        self.risks, self.returns, self.sharpeRatios = self.portfolio.calculatePortfolioCharacteristics(self.weightCombinations, sharpeRatio=True)


    def showGraph(self):
        plt.scatter(self.risks, self.returns, c=self.sharpeRatios, cmap='viridis', label="Randomly Generated Weights")
        plt.colorbar(label='Sharpe Ratio')
        
        edgeWeights = np.identity(self.portfolio.numberOfAssets)
        xEdge, yEdge = self.portfolio.calculatePortfolioCharacteristics(edgeWeights)
        plt.scatter(xEdge, yEdge, s=20, color='y', label="Points of portfolio with  one stock")
        plt.xlabel('Risks')
        plt.ylabel('Return')


    @staticmethod
    def generateWeights(randomDataPoints, size):
        weightCombinations = [np.random.rand(size) for _ in range(randomDataPoints)]
        weightCombinations = [i/sum(i) for i in weightCombinations]
        return weightCombinations



# --------------------------------- #

class randomWeightsModel(portfolioModel):

    def __init__(self, portfolio) -> None:
        super().__init__(portfolio)

    def runAlgorithm(self, numberOfRandomDataPoints=1000):

        super().runAlgorithm(numberOfRandomDataPoints=1000)
 
        self.risks, self.returns, self.weightCombinations = zip(*sorted(zip(self.risks, self.returns, self.weightCombinations)))

        self.minRiskPortfolio = {"Risks":self.risks[0], "Returns":self.returns[0], "Weights":self.weightCombinations[0]}

        prettyPrint(
            self.minRiskPortfolio["Risks"], 
            self.minRiskPortfolio["Returns"], 
            self.minRiskPortfolio["Weights"], 
            self.portfolio.stockNames, 
            "Point of minimum risk with randomly generated points:")

    def showGraph(self):

        super().showGraph()

        plt.plot(self.minRiskPortfolio["Risks"], self.minRiskPortfolio["Returns"],'r-p', label="Point of minimum risk")
        plt.title("Output of randomly generating weights for Portfolio")

        plt.legend()
        plt.show()


# --------------------------------- #

class weightedSumOptimizationModel(portfolioModel):

    def __init__(self, portfolio) -> None:
        self.portfolio = portfolio
    
    def runAlgorithm(self, lenOfLambdas=20):

        super().runAlgorithm()
        # convert to single objective optimization problem - 

        # The format of solvers.qp(P, q, G, h, A, b)
        # solving:
        # minimize: (1/2)xTPx + qTx
        # subject to: Gx <= h
        # and Ax = b

        # minimize (lam)*wT*C*w + (1-lam)*(-1)*mTW
        # so P = 2*lam*C
        # q = -mu*lab
        # G = (-1) -> -w <= 0 -> w >= 0
        # A = 1, b = 1 -> eTw = 1

        # we solve this for each lambda 

        portfolio = self.portfolio
        n = portfolio.numberOfAssets
        lambdas = np.linspace(0,1, lenOfLambdas)
        C = opt.matrix(portfolio.covMatrix) # cov matrix
        mu = opt.matrix(np.mean(portfolio.stockHistoricalData)) # returns matrix

        # Create constraint matrices
        G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
        h = opt.matrix(0.0, (n ,1))
        A = opt.matrix(1.0, (1, n))
        b = opt.matrix(float(1))
        
        # Calculate efficient frontier weights using quadratic programming
        self.optimzedWeightCombinations = [
            solvers.qp(opt.matrix(2*lambdaVal*C), 
            -opt.matrix((1-lambdaVal)*mu), 
            G, h, A, b)['x'] 
            for lambdaVal in lambdas]

        self.optimzedWeightCombinations = list(map(np.asarray, self.optimzedWeightCombinations))
        self.optimzedRisks, self.optimzedReturns = self.portfolio.calculatePortfolioCharacteristics(self.optimzedWeightCombinations)

        self.optimzedRisks, self.optimzedReturns, self.optimzedWeightCombinations = zip(*sorted(zip(self.optimzedRisks, self.optimzedReturns, self.optimzedWeightCombinations)))

        self.minRiskPortfolio = {"Risks":self.optimzedRisks[0], "Returns":self.optimzedReturns[0], "Weights":self.optimzedWeightCombinations[0]}

        prettyPrint(
            self.minRiskPortfolio["Risks"], 
            self.minRiskPortfolio["Returns"], 
            self.minRiskPortfolio["Weights"], 
            self.portfolio.stockNames, 
            "Point of minimum risk with randomly generated points:")
        
    def showGraph(self):
        super().showGraph()

        plt.plot(self.minRiskPortfolio["Risks"], self.minRiskPortfolio["Returns"],'r-p', label="Minimum risk using Optimizer (QPP)")
        plt.scatter(self.optimzedRisks, self.optimzedReturns,s=9,color='r', label="Risk/Return with Optimized weights for each lambda")
        
        edgeWeights = np.identity(self.portfolio.numberOfAssets)
        xEdge, yEdge = self.portfolio.calculatePortfolioCharacteristics(edgeWeights)
        plt.scatter(xEdge, yEdge, s=20, color='y', label="Points of portfolio with  one stock")
        
        plt.title("Output of Weighted Sum Optimization Model")
        plt.legend()
        plt.show()

# --------------------------------- #

class markowitzEfficientFrontierModel(portfolioModel):

    def __init__(self, portfolio) -> None:
        self.portfolio = portfolio

    def runAlgorithm(self):

        super().runAlgorithm()

        bounds= [(0,1) for _ in range(self.portfolio.numberOfAssets)]
        initGuess = [0.02]*self.portfolio.numberOfAssets

        self.frontierY = np.linspace(min(self.returns), max(self.returns), 200)
        self.frontierX = []
        for possibleReturn in self.frontierY:
            cons = ({'type':'eq', 'fun':self.checkSum},
            {'type':'eq', 'fun': lambda w: self.getReturn(w) - possibleReturn}) 

            result = minimize(self.minimizeVolatility,initGuess,method='SLSQP', bounds=bounds, constraints=cons)
            self.frontierX.append(result['fun'])


    def showGraph(self):
        super().showGraph()        
 
        plt.plot(self.frontierX,self.frontierY, 'r--', linewidth=3, label='Markowitz Efficient Frontier')
        
        plt.title("Markowitz Efficient Frontier Model")
        plt.legend()
        plt.show()

    @staticmethod
    def getReturn(weights):
        returns = portfolio.calculatePortfolioReturn(weights)
        return returns
    
    @staticmethod
    def minimizeVolatility(weights):
        risks = portfolio.calculatePortfolioRisk(weights)
        return risks
    
    @staticmethod
    def checkSum(weights):
        return np.sum(weights)-1


# --------------------------------- #

class optimizeRiskForReturnModel(portfolioModel):

    def __init__(self, portfolio, expectedReturn) -> None:
        self.portfolio = portfolio
        self.expectedReturn = expectedReturn
    
    def runAlgorithm(self):
        super().runAlgorithm()

        n = self.portfolio.numberOfAssets
        mu = self.expectedReturn/100 # converting to decimal

        S = opt.matrix(self.portfolio.covMatrix)
        pbar = opt.matrix(0.0, ((n,1)))
        G = -opt.matrix(np.eye(n))  
        h = opt.matrix(0.0, (n ,1))    

        # here i am basically combining eTw = 1 and mTw = u into one matrix
        a2 = np.asarray([np.mean(self.portfolio.stockHistoricalData)])
        a1 = np.ones((1, n))
        a = np.concatenate((a1, a2))
        A = opt.matrix(a)
        b = opt.matrix([float(1), mu])

        # solving for weight
        weights = solvers.qp(S, pbar, G, h, A, b)['x']
        portfolio.weights = weights.T
        
        self.optimalPortfolioRisk = self.portfolio.calculatePortfolioRisk()
        self.optimalPortfolioReturn = self.portfolio.calculatePortfolioReturn()

        prettyPrint(self.optimalPortfolioRisk, self.optimalPortfolioReturn, weights, stockNames,f"Optimal using Optimizer for {self.expectedReturn}%")
    
    def showGraph(self):
        super().showGraph()

        plt.plot(self.optimalPortfolioRisk, self.optimalPortfolioReturn, 'r-p', ms=5, label=f"Optimal for {self.expectedReturn}% return")
        plt.show()  


# --------------------------------- #

## TESTING ## 
# stockNames = ["ONGC", "HDBK", "TISC"]
# portfolio = Portfolio(stockNames)
# model = randomWeightsModel(portfolio)
# model = weightedSumOptimizationModel(portfolio)

# model = markowitzEfficientFrontierModel(portfolio)
# model = optimizeRiskForReturnModel(portfolio, 1.7)

# model.runAlgorithm()
# model.showGraph()



# --------------------------------- #