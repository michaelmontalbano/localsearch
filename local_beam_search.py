# local beam search

# student name: Michael Montalbano
# date: 3/30/2020

import copy
from random import Random
import numpy as np
import random
import sys
import itertools
from heapq import heappush, heappushpop

iterations = 100 # number of times to run
beams = 3 # number of beams
first_seed = 5113
myPRNG = Random(first_seed)

n = 150

# initialize instance of knapsack problem
value = []
for i in range(0,n):
    value.append(round(myPRNG.triangular(5,1000,200),1))
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(10,200,60),1))
maxWeight = 1500
solutionsChecked = 0

#function used to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)
    totalValue = np.dot(a,b)    # compute the value of the knapsack selection
    totalWeight = np.dot(a,c)   # compute the weight

    if totalWeight > maxWeight:
        totalValue = 0
    return [totalValue, totalWeight]

#create the initial solution
def initial_solution(s):
    myPRNG = Random(s)
    x = []
    for i in range(0,n):
        x.append(myPRNG.randint(0,1))   # random list of 0's and 1's, 
    for idx, a in enumerate(x): # take items out of knapsack until totalWeight < maxWeight
        x[idx] = 0
        if evaluate(x)[0] != 0:
            break
    return x

def solutions(b):
    '''
    Generates b solutions, each using a different random seed
    Returns a list containing b solutions
    '''
    solutions = []
    for _ in itertools.repeat(None,beams):
        seed = myPRNG.randint(1000,10000)
        s = initial_solution(seed)
        solutions.append(s)
    return solutions

def find_neighbors(solutions):
    '''
    Finds the neighbors of all solutions by finding the neighborhood of each solution
    Returns a list containing n neighbors for each solution
    '''
    nbrhood = []
    for s in solutions:
        neighbors = neighborhood(s)     # n is a list containing the neighbors of s
        for n in neighbors:
            nbrhood.append(n)           # append each neighbor to a list containing the entire neighborhood, for all solutions
    return nbrhood

def neighborhood(x):
    nbrhood = []
    for i in range(0,n):
        nbrhood.append(x[:]) 
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
    return nbrhood    

def find_best(nbrhood, beams, x_heap, f_heap):
    '''
    finds n best solutions out of a list of solutions
    '''
    for s in nbrhood:
        if f_heap[0][0]-evaluate(s)[0] < 0:     #if the solution is an improvement (i.e. the difference between the current best and current is negative)
            x_best = s[:]                       #basic hill climbing
            f_best = evaluate(s)[:]
            if len(f_heap) < beams:             #if there are less solutions than the required b, psuh this best one onto the list (heap)
                heappush(x_heap, x_best[:])     #push the solution
                heappush(f_heap, f_best)        #push the objective value and weight
            else:
                heappushpop(x_heap, x_best[:])  #pop from the list, push onto list
                heappushpop(f_heap,f_best)
    x_heap = sorted(x_heap, reverse=True)       #sort in reverse order, i.e. with the highest first
    f_heap = sorted(f_heap, reverse=True)
    return x_heap, f_heap

#find k solutions
x_curr = solutions(beams) #generate a solution for each beam
x_heap = x_curr
f_heap = []

#find values
for x in x_heap:
    f_heap.append(evaluate(x)) 

#execute beam search
for _ in itertools.repeat(None, iterations): # repeat iterations times
    nbrhood = find_neighbors(x_heap)                            #find neighbors
    x_heap, f_heap = find_best(nbrhood, beams, x_heap, f_heap)  #find the best of all neighbors, beam times
    solutionsChecked = solutionsChecked + beams*n               #update number of solutions
    
    print("\nTotal number of solutions checked: ", solutionsChecked)
    print("Best value found so far: ", f_heap)

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_heap[0][0])
print ("Weight is: ", f_heap[0][1])
print ("Total number of items selected: ", np.sum(x_heap[0]))
print ("Best solution: ", x_heap[0])
