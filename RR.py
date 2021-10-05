#############################
#    Randomized Rounding    #
# Dagny, Luke, Elise, Kylee #
#############################

import random
import itertools

###########################
#  Part 1: Read in input  #
###########################

sets = [[1,2], [1,3], [2,3]]
set_number = 3
weights = [1,1,1]
n = 3 #U constructor

####################################
#    Part 2: Linear Programming    #
# finding the partial set Solution #
####################################

# x* = simplex(...)
def simplex_solver():
    return 0


###############################
# Part 3: Randomized Rounding #
#   finding a valid solution  #
###############################

def randomized_rounding(sets, weights, n, set_number):
    U = list(range(1, n+1 ))
    X_star = simplex_solver() #1D array of probs
    X_star = [0.5, 0.5, 0.5] #REMOVE
    cover_weight = 0
    cover = []
    UB_weight_sum = sum([weights[i]*X_star[i] for i in range(set_number)])
    unused_set_inds = list(range(0,set_number))
    while( len(list(set(list(itertools.chain.from_iterable(cover))))) != n ): #check this comparison
        if(cover_weight >= (4 * set_number * UB_weight_sum)):
            cover = []
            cover_weight = 0
            unused_set_inds = list(range(0,set_number))
        else:
            for index in unused_set_inds:
                if random.random() <= X_star[index]:
                    cover.append(sets[index])
                    cover_weight += weights[index]
                    unused_set_inds.remove(index)

    return (cover, cover_weight)


############################
# Part 4: Greedy Algorithm #
############################

def greedy(s, w):
    return 0


####################################
# Part 5: Trivial Random Algorithm #
####################################

def trivial_random(s, w):
    return 0








randomized_rounding(sets, weights, n, set_number)