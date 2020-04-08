# random_walk hill climbing
# student name: Michael Montalbano
# date: 3/30/2020

import copy
from random import Random
import numpy as np
import random
import sys
import itertools

p = 0.2     #probability of choosing neighbor at random
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
def initial_solution():
    x = []
    for i in range(0,n):
        x.append(myPRNG.randint(0,1))   # random list of 0's and 1's, 
    for idx, a in enumerate(x): # take items out of knapsack until totalWeight < maxWeight
        x[idx] = 0
        if evaluate(x)[0] != 0:
            break
    return x

def shuffle(x):
    '''
    shuffles (randomizes order) of a list
    '''
    return random.sample(x,n) #uses sample method from random module to randomize the order of neighbors

solutionsChecked = 0

x_curr = initial_solution()
x_best = x_curr[:]
f_curr = evaluate(x_curr)

f_best = f_curr[:]

# begin local search overall logic ------------
done = 0
while done == 0:
    Neighborhood = neighborhood(x_curr) #create a list of all neighbors in the neighborhood of x_curr
    chance = myPRNG.random()            #generate random number between 0 and 1
    if chance < p:                      #if this is below p, hill climb as normal 
        for s in Neighborhood:
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]
                f_best = evaluate(s)[:]
    else:                               #otherwise, choose a random neighbor
        for idx, s in enumerate(shuffle(Neighborhood)): #randomizes order of neighborhood
            if evaluate(s)[0] != 0:                     #checks first to make sure the neighbor is feasible
                x_best = s[:]                           #if so, use this one
                f_best = evaluate(s)
                break                                   #break once a feasible solution is found

# I could have just chosen any neighbor, no matter whether it's feasible. I however thought this was better
# in the case that you are looking for the other version, here it is
#   else:   
#       s = shuffle(Neighborhood)
#       x_best = s[:]
#       f_best = evaluate(s)
#       break
        
    if f_best == f_curr:
        done = 1
    else:
        x_curr = x_best[:]
        f_curr = f_best[:]

    print("\nTotal number of solutions checked: ", solutionsChecked)
    print("Best value found so far: ", f_best)

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)