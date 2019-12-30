import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



class Perceptron:

    def __init__(self,learning_rate=0.01,epochs=100,random_state=1):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.random_state = random_state

    def fit(self,X,y):
        rgen = np.random.Random(self.random_state)

        self.w = rgen.normal(loc=0.0,scale=0.01,size=X.shape[1] + 1)

        self.errors = []
        for epoch in range(self.epochs):
            errors = 0
            for xi,yi in zip(X,y):
                result = self.predict(xi)
                error = (yi - result)
                self.w[1:] += self.learning_rate * error * self.x[1:]
                self.w[0] += self.learning_rate * error * self.x[0]
                errors += int(error != 0)

            self.errors.append(errors)

        return self



    def net_input(self,X):
        return np.dot(X,self.w[1:]) + self.w[0]
    
    def predict(self,X):
        return np.where(self.net_input(X) >= 0.0,1,-1)


class Adaline:

    def __init__(self,learning_rate=0.01,epochs=100,random_state=1):
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.random_state = random_state

    def fit(self,X,y):

        rgen = np.random.Random(self.random_state)
        self.w = rgen.normal(loc=0.0,scale=0.01,size=X.shape[1] + 1)

        self.costs = []
        for epoch in range(self.epochs):
            result = self.net_input(X)
            error = (y - result)
            self.w[1:] += self.learning_rate * X.T.dot(errors)
            self.w[0] += self.learning_rate * np.sum(errors)
            cost = (0.5 * (error)**2) / X.shape[0]
            self.costs.append(cost)
        
        return self



    def net_input(self,X):
        return np.dot(X,self.w[1:]) + self.w[0]


    def predict(self,X): 
        return np.where(self.net_input(X) >= 0.0,1,-1)



class AdalineSGD:

    def __init__(self,learning_rate=0.01,epochs=100,shuffle=True,random_state=1):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.random_state = random_state
        self.shuffle = shuffle
        self._weights_initialized = False

    def fit(self,X,y):

        self._initialize_weights(X.shape[1] + 1)

        self.costs = []
        for epoch in range(self.epochs):
            if self.shuffle:
                X,y = self._shuffle(X,y)
            cost = 0
            for xi,yi in zip(X,y):
                cost += self._update_weight(xi,yi)
            self.costs.append(cost / y.shape[0])

        return self
    
    def _shuffle(self,X,y):

        indices = self.rgen.permutation(y.shape[0])
        return X[indices],y[indices]

    def _update_weight(self,X,y):
        result = self.net_input(X)
        error = (y - result)
        self.w[1:] += self.learning_rate * X * error
        self.w[0] += self.learning_rate * error
        return 0.5 * (error)**2

    
    def partial_fit(self,X,y):

    def net_input(self,X):
        return np.dot(X,self.w[1:]) + self.w[0]


    def _initialize_weights(self,size):

        self.rgen = np.random.Random(self.random_state)

        self.w = self.rgen.normal(loc=0.0,scale=0.01,size=size)














