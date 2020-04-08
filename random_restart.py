# random restarts hill climbing
# author: Charles Nicholson

# student name: Michael Montalbano
# date: 3/30/2020

import copy
from random import Random
import numpy as np
import random
import sys
import itertools

restarts = 10000 # number of random restarts
seed = 5113
myPRNG = Random(seed)

# [0,1]: myPRNG.random()
# [l,u]: myPRNG.uniform(lwrBnd,upprBnd)
# int [l,u]: myPRNG.randint(lwrBnd,upprBnd)

# number of elements in a solution
n = 150

# initialize instance of knapsack problem
value = []
for i in range(0,n):
    value.append(round(myPRNG.triangular(5,1000,200),1))
    
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(10,200,60),1))

#define max weight for the knapsack
maxWeight = 1500

#*******************************************************
#*******************************************************

#monitor the number of solutions evaluated
solutionsChecked = 0

#function used to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)
    totalValue = np.dot(a,b)    # compute the value of the knapsack selection
    totalWeight = np.dot(a,c)   # compute the weight

    # what do we do if it is infeasible?
    if totalWeight > maxWeight:
        totalValue = 0


    return [totalValue, totalWeight]

def neighborhood(x):
    nbrhood = []
    for i in range(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
    return nbrhood

#create the initial solution
def initial_solution(seed):
    myPRNG = Random(seed)
    x = []
    for i in range(0,n):
        x.append(myPRNG.randint(0,1))   # random list of 0's and 1's, 
    for idx, a in enumerate(x): # take items out of knapsack until totalWeight < maxWeight
        x[idx] = 0
        if evaluate(x)[0] != 0:
            break
    return x

solutionsChecked = 0

x_curr = initial_solution(seed)
x_best = x_curr[:]
f_curr = evaluate(x_curr)

f_best = f_curr[:]

c_best = f_best # best of all random restarts
t_best = x_best # best of all random restarts

# begin local search overall logic ------------
i=0
for _ in itertools.repeat(None, restarts):  #add outer loop, which runs 'restarts' number of times (thats what itertools.repeats() does)
    if i == 0:
        seed = 5113                         #use stock seed first time around
    else:
        seed = random.randint(1000,10000)   #thereafter, generate a random int to use as seed
    i=+1
    x_curr = initial_solution(seed)
    x_best = x_curr[:]
    f_curr = evaluate(x_curr)

    f_best = f_curr[:]  
    done = 0
    while done == 0:
        Neighborhood = neighborhood(x_curr) #create a list of all neighbors in the neighborhood of x_curr

        for s in Neighborhood:
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]
                f_best = evaluate(s)[:]
            
        if f_best == f_curr:
            done = 1
        else:
            x_curr = x_best[:]
            f_curr = f_best[:]

        print("\nTotal number of solutions checked: ", solutionsChecked)
        print("Best value found so far: ", f_best)

    print("Best value found: ", f_best[0])
    print ("Weight is: ", f_best[1])
    print ("Total number of items selected: ", np.sum(x_best))
    print ("Best solution: ", x_best)

    #keep track of best solution thus far
    if f_best[0] > c_best[0]:   #if the best solution of this restart is better than the global best
        c_best[0] = f_best[0]   #reset to current best
        c_best[1] = f_best[1]   
        t_best = x_best
print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", c_best[0])
print ("Weight is: ", c_best[1])
print ("Total number of items selected: ", np.sum(t_best))
print ("Best solution: ", t_best)