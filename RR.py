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
    X_star = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] #REMOVE
    cover_weight = 0
    cover = []
    UB_weight_sum = sum([weights[i]*X_star[i] for i in range(set_number)])
    unused_set_inds = list(range(0,set_number))
    flat_list = []
    # THE LINE BELOW HANGS SOMETIMES
    while( len(list(set(flat_list))) != n ): #check this comparison 
        if(cover_weight >= (4 * set_number * UB_weight_sum)):
            cover = []
            cover_weight = 0
            unused_set_inds = list(range(0,set_number))
            flat_list = []
        else:
            for index in unused_set_inds:
                if random.random() <= X_star[index]:
                    cover.append(sets[index])
                    cover_weight += weights[index]
                    unused_set_inds.remove(index)
            flat_list = [item for sublist in cover for item in sublist]
            flat_list = list(set(flat_list))

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

################################
# Part 6: Testing RR Algorithm #
################################

def run_random_trials():

    # test list of 3
    sets = [[1,2], [1,3], [2,3]]
    set_number = 3
    weights = [1,1,1]
    n = 3 #U constructor

    print(randomized_rounding(sets, weights, n, set_number))

    # test list of 5
    sets = [[1,2], [1,3], [2,3], [5], [1,4], [5,3], [4,2]]
    set_number = 7
    weights = [1,9,1,5,8,2,2]
    n = 5 #U constructor

    print(randomized_rounding(sets, weights, n, set_number))

    # test list of 10
    # doesn't always get all 10 elements, likes to skip 6 and 7
    sets = [[1,2], [1,3], [2,3], [4,5], [6,7], [8,9], [9,10], [1,2,3], [4,8,3,2], [1,4,8], [4,2,5]]
    set_number = 11
    weights = [1,5,7,3,4,6,8,4,3,7,3]
    n = 10 #U constructor

    print(randomized_rounding(sets, weights, n, set_number))





# randomized_rounding(sets, weights, n, set_number)

run_random_trials()
