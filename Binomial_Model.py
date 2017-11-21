# -*- coding: utf-8 -*-

import numpy as np
import math
import seaborn as sns
from matplotlib import pylab

__author__ = 'Henry'
__date__ = '2017-11-5'


class BinomialTree:
    def __init__(self, spot, riskFree, dividend, tSteps, maturity, sigma, treeTraits, strike):
        self.dt = maturity / tSteps
        self.spot = spot
        self.r = riskFree
        self.d = dividend
        self.tSteps = tSteps
        self.discount = math.exp(-self.r*self.dt)
        self.v = sigma
        self.strike = strike
        self.up = treeTraits.up(self)
        self.down = treeTraits.down(self)
        self.upProbability = treeTraits.upProbability(self)
        self.downProbability = 1.0 - self.upProbability
        self._build_lattice()

    def _build_lattice(self):
        self.lattice = np.zeros((self.tSteps+1, self.tSteps+1))
        self.lattice[0][0] = self.spot
        for i in range(self.tSteps):
            for j in range(i+1):
                self.lattice[i+1][j+1] = self.up * self.lattice[i][j]
            self.lattice[i+1][0] = self.down * self.lattice[i][0]

    def roll_back(self):
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.lattice[i-1][j-1] = self.discount * (self.upProbability * max(self.lattice[i][j] - self.strike, 0) + self.downProbability * max(self.lattice[i][j-1] - self.strike, 0))
                else:
                    self.lattice[i-1][j-1] = self.discount * (self.upProbability *  self.lattice[i][j] + self.downProbability * self.lattice[i][j-1])

    def roll_back_put(self):
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.lattice[i-1][j-1] = self.discount * (self.upProbability * max(self.strike - self.lattice[i][j], 0) + self.downProbability * max(self.strike - self.lattice[i][j-1], 0))
                else:
                    self.lattice[i-1][j-1] = self.discount * (self.upProbability *  self.lattice[i][j] + self.downProbability * self.lattice[i][j-1])


    def plot_tree(self):
        self.tree = np.zeros((self.tSteps+1, self.tSteps+1))
        #pylab.figure(figsize = (12, 8))
        #pylab.plot(self.roll_back(pay_off))
        #pylab.show()
        #print self.roll_back(pay_off)



class JarrowRuddTraits:
    @staticmethod
    def up(tree):
        return math.exp((tree.r - tree.d - 0.5*tree.v*tree.v)*tree.dt + tree.v*math.sqrt(tree.dt))

    @staticmethod
    def down(tree):
        return math.exp((tree.r - tree.d - 0.5*tree.v*tree.v)*tree.dt - tree.v*math.sqrt(tree.dt))

    @staticmethod
    def upProbability(tree):
        return 0.5


class CRRTraits:
    @staticmethod
    def up(tree):
        return math.exp(tree.v * math.sqrt(tree.dt))

    @staticmethod
    def down(tree):
        return math.exp(-tree.v * math.sqrt(tree.dt))

    @staticmethod
    def upProbability(tree):
        return 0.5 + 0.5 * (tree.r - tree.d - 0.5 * tree.v*tree.v) * tree.dt / tree.v / math.sqrt(tree.dt)


'''
def pay_off(spot):
    global strike
    return max(spot - strike, 0.0)

def pay_off_put(spot):
    global strike
    return max(strike - spot, 0.0)
'''


class ExtendBinomialTree(BinomialTree):   # America

    def roll_back_american(self):

        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    europeanValue = self.discount * (self.upProbability * max(self.lattice[i][j] - self.strike, 0) + self.downProbability * max(self.lattice[i][j-1] - self.strike, 0))
                else:
                    europeanValue = self.discount * (self.upProbability *  self.lattice[i][j] + self.downProbability * self.lattice[i][j-1])
                exerciseValue = max(self.lattice[i-1][j-1] - self.strike, 0)
                self.lattice[i-1][j-1] = max(europeanValue, exerciseValue)

    def roll_back_american_put(self):

        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    europeanValue = self.discount * (self.upProbability * max(self.strike - self.lattice[i][j], 0) + self.downProbability * max(self.strike - self.lattice[i][j-1], 0))
                else:
                    europeanValue = self.discount * (self.upProbability *  self.lattice[i][j] + self.downProbability * self.lattice[i][j-1])
                exerciseValue = max(self.strike - self.lattice[i-1][j-1], 0)
                self.lattice[i-1][j-1] = max(europeanValue, exerciseValue)


class GetHedgeRatio:
    def __init__(self, spot, riskFree, dividend, tSteps, maturity, sigma, treeTraits, strike):
        self.dt = maturity / tSteps
        self.spot = spot
        self.r = riskFree
        self.d = dividend
        self.tSteps = tSteps
        self.discount = math.exp(-self.r*self.dt)
        self.v = sigma
        self.strike = strike
        self.up = treeTraits.up(self)
        self.down = treeTraits.down(self)
        self.upProbability = treeTraits.upProbability(self)
        self.downProbability = 1.0 - self.upProbability
        #self._build_lattice()
        self._build_node()

    def _build_node(self):
        self.node = np.zeros((self.tSteps+1, self.tSteps+1))
        self.cash = np.zeros((self.tSteps+1, self.tSteps+1))
        self.stock = np.zeros((self.tSteps+1, self.tSteps+1))
        self.node[0][0] = self.spot
        for i in range(self.tSteps):
            for j in range(i+1):
                self.node[i+1][j+1] = self.up * self.node[i][j]
            self.node[i+1][0] = self.down * self.node[i][0]
        self.stock[0][0] = self.spot
        for i in range(self.tSteps):
            for j in range(i+1):
                self.stock[i+1][j+1] = self.up * self.stock[i][j]
            self.stock[i+1][0] = self.down * self.stock[i][0]

    def build_node_euroCall(self):
        tree = BinomialTree(self.spot, self.r, self.d, self.tSteps, self.dt*self.tSteps, self.v, JarrowRuddTraits, self.strike)
        tree.roll_back()
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.stock[i-1][j-1] = (max(self.node[i][j]-self.strike, 0)-max(self.node[i][j-1]-self.strike, 0))/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*((self.node[i][j]*max(self.node[i][j-1]-self.strike, 0)-self.node[i][j-1]*max(self.node[i][j]-self.strike, 0))/(self.node[i][j]-self.node[i][j-1]))
                else:
                    self.stock[i-1][j-1] = (tree.lattice[i][j]-tree.lattice[i][j-1])/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*(self.node[i][j]*tree.lattice[i][j-1]-self.node[i][j-1]*tree.lattice[i][j])/(self.node[i][j]-self.node[i][j-1])

    def build_node_euroPut(self):
        tree = BinomialTree(self.spot, self.r, self.d, self.tSteps, self.dt*self.tSteps, self.v, JarrowRuddTraits, self.strike)
        tree.roll_back_put()
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.stock[i-1][j-1] = (max(self.strike-self.node[i][j], 0)-max(self.strike-self.node[i][j-1], 0))/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*((self.node[i][j]*max(self.strike-self.node[i][j-1], 0)-self.node[i][j-1]*max(self.strike-self.node[i][j], 0))/(self.node[i][j]-self.node[i][j-1]))
                else:
                    self.stock[i-1][j-1] = (tree.lattice[i][j]-tree.lattice[i][j-1])/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*(self.node[i][j]*tree.lattice[i][j-1]-self.node[i][j-1]*tree.lattice[i][j])/(self.node[i][j]-self.node[i][j-1])

    def build_node_amerCall(self):
        tree = ExtendBinomialTree(self.spot, self.r, self.d, self.tSteps, self.dt*self.tSteps, self.v, JarrowRuddTraits, self.strike)
        tree.roll_back_american()
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.stock[i-1][j-1] = (max(self.node[i][j]-self.strike, 0)-max(self.node[i][j-1]-self.strike, 0))/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*((self.node[i][j]*max(self.node[i][j-1]-self.strike, 0)-self.node[i][j-1]*max(self.node[i][j]-self.strike, 0))/(self.node[i][j]-self.node[i][j-1]))
                else:
                    self.stock[i-1][j-1] = (tree.lattice[i][j]-tree.lattice[i][j-1])/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*(self.node[i][j]*tree.lattice[i][j-1]-self.node[i][j-1]*tree.lattice[i][j])/(self.node[i][j]-self.node[i][j-1])

    def build_node_amerPut(self):
        tree = ExtendBinomialTree(self.spot, self.r, self.d, self.tSteps, self.dt*self.tSteps, self.v, JarrowRuddTraits, self.strike)
        tree.roll_back_american_put()
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.stock[i-1][j-1] = (max(self.strike-self.node[i][j], 0)-max(self.strike-self.node[i][j-1], 0))/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*((self.node[i][j]*max(self.strike-self.node[i][j-1], 0)-self.node[i][j-1]*max(self.strike-self.node[i][j], 0))/(self.node[i][j]-self.node[i][j-1]))
                else:
                    self.stock[i-1][j-1] = (tree.lattice[i][j]-tree.lattice[i][j-1])/(self.node[i][j]-self.node[i][j-1])
                    self.cash[i-1][j-1] = self.discount*(self.node[i][j]*tree.lattice[i][j-1]-self.node[i][j-1]*tree.lattice[i][j])/(self.node[i][j]-self.node[i][j-1])



'''
# This is a test on convergence between different tree traits

stepSizes = range(1, 10,1)
jrRes = []
crrRes = []
for tSteps in stepSizes:
    # Jarrow - Rudd
    testTree = ExtendBinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits)
    testTree.roll_back_american(pay_off)
    jrRes.append(testTree.lattice[0][0])

    # Cox - Ross - Rubinstein
    testTree = ExtendBinomialTree(spot, r, d, tSteps, ttm, sigma, CRRTraits)
    testTree.roll_back_american(pay_off)
    crrRes.append(testTree.lattice[0][0])

#anyRes = [BSMPrice(1, strike, spot, r, d, sigma, ttm, rawOutput= True)[0]] * len(stepSizes)

pylab.figure(figsize = (16,8))
pylab.plot(stepSizes, jrRes, '-.', marker = 'o', markersize = 10)
pylab.plot(stepSizes, crrRes, '-.', marker = 'd', markersize = 10)
#pylab.plot(stepSizes, anyRes, '--')
pylab.legend([u'Jarrow - Rudd(America)', u'Cox - Ross - Rubinstein(America)'])
pylab.xlabel(u'Steps')
pylab.title(u'BinomialTree(A)', fontsize = 20)
pylab.show()
'''



'''
# Data for test
# Plot all possible paths together with option value at each node
ttm = 0.579365
tSteps = 100
r = 0.0187
d = 0.0124
sigma = 0.22
strike = 120
spot = 240.78

testTree = ExtendBinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits, strike)
testTree.roll_back_american()

print testTree.lattice[0][0]
'''

'''
# Loop in strike prices
# Return option values under different strike price
for t in range(120, 280, 5):
    strike = t
    testTree = BinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits)
    testTree.roll_back_put(pay_off_put)

    print u' %.4f' % testTree.lattice[0][0]
'''


