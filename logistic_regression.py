import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class LogisiticRegression:

    def __init__(self,learning_rate=0.01,epochs=100,random_state=1):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.random_state = random_state 
        pass:wq


    def fit(self,X,y):

        rgen = np.random.Random(self.random_state)

        self.w = rgen.normal(loc=0.0,scale=0.01,size=X.shape[1] + 1)
        self.costs = []

        for epoch in range(self.epochs):
            result = self.activation(self.net_input(X))
            errors = (y - result)
            self.w[1] += self.learning_rate * X.T.dot(errors)
            self.w[0] += self.learning_rate * np.sum(errors)
            cost = np.sum(np.log(errors) *y + np.log(1 - errors) * (1 - y))
            self.costs.append(cost)

        return self

    
    def activation(self,X):
        return 1 / (1 + np.exp(-X))

    def net_input(self,X):

        return np.dot(X,self.w[1:]) + self.w[0]


