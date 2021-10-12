#!/usr/bin/python3
#############################
#    Randomized Rounding    #
# Dagny, Luke, Elise, Kylee #
#############################

import random
import scipy.optimize
import sys

###########################
#  Part 1: inputs  #
###########################
def generate_input(n, num_subsets, max_subset_length):
    num_items_in_union = n # english translation because all of these n's are ~*confusing*~
    subsets = []
    weights = []
    for i in range(0,num_subsets):
        # make subsets
        sub_temp = []
        rand_sub_len = random.randint(1,max_subset_length)
        for j in range(0,rand_sub_len):
            sub_temp.append(random.randint(1,n))
        subsets.append(list(set(sub_temp)))

        # make weight list
        weights.append(random.randint(1,1000)) # making up fake weights

    contents_of_subsets = [item for sublist in subsets for item in sublist]
    contents_of_subsets = list(set(contents_of_subsets))
    union = list(range(1, num_items_in_union+1 ))
    while (contents_of_subsets != union): # if not all of the numbers are in the subsets, replace last subset until they are
        # make subsets
        sub_temp = []
        rand_sub_len = random.randint(1,max_subset_length)
        for j in range(0,rand_sub_len):
            sub_temp.append(random.randint(1,n))
        subsets.pop()
        subsets.append(sub_temp)

        # update contents_of_sets
        contents_of_subsets = [item for sublist in subsets for item in sublist]
        contents_of_subsets = list(set(contents_of_subsets))

    return (subsets, weights, num_items_in_union, num_subsets)

def print_input_to_file(num_elements, subsets, weights):
    output_file = open("rando-algs-input-small.txt", 'w')
    output_file.write(str(num_elements)+"\n")
    output_file.write(str(len(subsets))+"\n")
    counter = -1
    for subset in subsets: # for each subset in the subset array
        counter+=1
        temp_sub_str = ""
        for i in range(0,len(subset)): # create a string out of the subset elements
            temp_sub_str=temp_sub_str+str(subset[i])
            if (i<(len(subset)-1)):
                temp_sub_str=temp_sub_str+" "
        output_file.write(temp_sub_str+"\n") # add that string version of the subset to the outfile
        output_file.write(str(weights[counter])+"\n") # this is hardcoded to insert the first element of weights, change
    output_file.close()

def read_input_file(filename):
    with open(filename) as file:
        lines = file.readlines()
    stripped = []
    for line in lines:
        stripped.append(line.rstrip())

    n = int(stripped.pop(0))
    set_number = int(stripped.pop(0))
    sets = []
    weights = []

    on_set = True
    for line in stripped:
        if on_set:
            sets.append([int(s) for s in line.split(' ')])
            on_set = False
        else:
            weights.append(float(line))
            on_set = True

    return (sets, weights, n, set_number)

####################################
#    Part 2: Linear Programming    #
# finding the partial set Solution #
####################################
def mathematica_solve(sets, weights, n, set_number):
    # Mathematica uses A.x >= b rather than A.x <= b
    A = [[1 if j in s else 0 for s in sets] for j in range(1, n+1)]
    b = [1 for i in range(n)]
    c = weights
    lu = [[0, 1] for i in range(set_number)]
    
    # turns python-style vectors and matrices into mathematica
    def mize(v):
        return str(v).replace('[', '{').replace(']', '}')

    return f"""
        A = {mize(A)};
        c = {mize(c)};
        b = {mize(b)};
        LU = {mize(lu)};
        LinearProgramming[c, A, b, LU, Integers]
    """

def mathematica_parse(sets, weights, n, set_number):
    input_string = "{0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, \
1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, \
0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, \
0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}"

    parsed = input_string.replace("{", "").replace("}", "").split(",")
    parsed = [int(i) for i in parsed]
    final = ""
    
    weight = 0
    for i, xi in enumerate(parsed):
        if xi == 1:
            weight += weights[i]
            final += f"{i} "

    print(weight)
    print(final)

    
# x* = simplex(...)
def simplex_solver(sets,weights,n,set_number):
    A = [[-1 if j in s else 0 for s in sets] for j in range(1, n+1)]
    b = [-1 for i in range(n)]
    X_star = scipy.optimize.linprog(weights,A_ub=A,b_ub=b,bounds=(0,1))
    return X_star.x

###############################
# Part 3: Randomized Rounding #
#   finding a valid solution  #
###############################

def randomized_rounding(sets, weights, n, set_number, simp_array):
    U = list(range(1, n+1 ))
    X_star = simp_array #simplex_solver(sets,weights,n,set_number) #1D array of probs
    cover_weight = 0
    cover = []
    cover_inds = []
    UB_weight_sum = sum([weights[i]*X_star[i] for i in range(set_number)])
    unused_set_inds = list(range(0,set_number))
    flat_list = []
    while( len(list(set(flat_list))) != n ):
        if(cover_weight >= (4 * set_number * UB_weight_sum)):
            cover = []
            cover_inds = []
            cover_weight = 0
            unused_set_inds = list(range(0,set_number))
            flat_list = []
        else:
            for index in unused_set_inds:
                if random.random() <= X_star[index]:
                    cover.append(sets[index])
                    cover_inds.append(index+1) # as per the problem statement, 1-indexing subsets in final answer
                    cover_weight += weights[index]
                    unused_set_inds.remove(index)
            flat_list = [item for sublist in cover for item in sublist]
            flat_list = list(set(flat_list))

    return (cover, cover_weight, cover_inds)

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

# def run_random_trials():

#     # test list of 3
#     sets = [[1,2], [1,3], [2,3]]
#     set_number = 3
#     weights = [1,1,1]
#     n = 3 #U constructor

#     print(randomized_rounding(sets, weights, n, set_number))

#     # test list of 5
#     sets = [[1,2], [1,3], [2,3], [5], [1,4], [5,3], [4,2]]
#     set_number = 7
#     weights = [1,9,1,5,8,2,2]
#     n = 5 #U constructor

#     print(randomized_rounding(sets, weights, n, set_number))

#     # test list of 10
#     sets = [[1,2], [1,3], [2,3], [4,5], [6,7], [8,9], [9,10], [1,2,3], [4,8,3,2], [1,4,8], [4,2,5]]
#     set_number = 11
#     weights = [1,5,7,3,4,6,8,4,3,7,3]
#     n = 10 #U constructor

#     print(randomized_rounding(sets, weights, n, set_number))

def run_random_rounding_n_times(iters, sets, weights, n, set_number):
    best_cover = []
    best_cover_weight = 99999
    cover_frequency = {}
    weight_frequency = {}
    best_cov_inds = []
    simp = simplex_solver(sets,weights,n,set_number) #1D array of probs
    for i in range(1,iters+1):
        print("Running trial #"+str(i))
        (cover, cover_weight, cover_inds) = randomized_rounding(sets, weights, n, set_number, simp)
        cover.sort()
        # print("Cover has "+str(len(cover))+" items and weight "+str(cover_weight))
        # count cover frequency
        if (str(cover) in cover_frequency):
            cover_frequency[str(cover)]+=1
        else:
            cover_frequency[str(cover)] = 1
        # count cover weight frequency
        if (cover_weight in weight_frequency):
            weight_frequency[cover_weight]+=1
        else:
            weight_frequency[cover_weight]=1
        if (cover_weight < best_cover_weight):
            best_cover_weight = cover_weight
            best_cover = cover
            best_cov_inds = cover_inds
    print("Best cover has "+str(len(best_cover))+" items and weight "+str(best_cover_weight))
    return(best_cover, best_cover_weight, cover_frequency,weight_frequency, best_cov_inds)

#########################
# Part 7: Verify Output #
#########################

def verify_output(sets, weights, n, set_number, outputfile):
    goodAnswer = True
    with open(outputfile) as file:
        unclean_lines = file.readlines()
    lines = []
    for line in unclean_lines:
        lines.append(line.rstrip())
        
    U = list(range( 1, n+1 ))
    soln_weight = lines[0]
    chosen_set_inds = [(int(s) - 1 ) for s in lines[1].split(' ')]

    weight = 0
    chosen_sets = []
    for ind in chosen_set_inds:
        weight += weights[ind]
        chosen_sets.append(sets[ind])
        
    if (weight != int(soln_weight)):
        print("Solution weight (", soln_weight, ") does not match the weights of the chosen sets (", int(weight), ")")
        goodAnswer = False
    flattened_sets = list(set([j for sub in chosen_sets for j in sub]))
    flattened_sets = sorted(flattened_sets)
    if ( flattened_sets != U):
        print("set cover (", flattened_sets, ") != U (", U, ")")
        goodAnswer = False
    return goodAnswer

#####################
# Part 7: Code Time #
#####################

def elise_verbose_output(): # this prints useful info and the input file to elise_verbose_out.txt
    output_file = open("elise_verbose_out.txt", 'w')
    input_num_max = 1000
    input_num_of_subs = 500
    input_max_sub_size = 100
    num_trials_to_run = 1000
    output_file.write("Input details:\nMax number: "+str(input_num_max)+"\nNumber of subsets: "+str(input_num_of_subs)+"\nMax subset size: "+str(input_max_sub_size)+"\n\n")
    (subs, dubs, n, num_subs) = generate_input(input_num_max, input_num_of_subs, input_max_sub_size)
    print_input_to_file(n, subs, dubs)
    output_file.write("Running "+str(num_trials_to_run)+" trials\n\n")
    (best_cover, best_cover_weight, cov_freq, cov_weight_freq, cov_inds) = run_random_rounding_n_times(num_trials_to_run, subs, dubs, n, num_subs)
    from collections import Counter
    output_file.write("Freq of cover trial covers: "+str(Counter(cov_freq.values()))+"\n")
    output_file.write("Freq of cover trial weights: "+str(Counter(cov_weight_freq.values()))+"\n")
    output_file.write("\n")
    output_file.write("Best cover has "+str(len(best_cover))+" items and weight "+str(best_cover_weight)+"\n\n")
    output_file.write("Best cover contents as indexes: \n"+str(cov_inds)+"\n\n")
    output_file.write("Input used attached below\n")
    output_file.write("\n")
    output_file.close()

    f1 = open("elise_verbose_out.txt", 'a+')
    f2 = open("rando-algs-input.txt", 'r')
    
    f1.write(f2.read())

    f1.close()
    f2.close()

#elise_verbose_output()

def run_RR(inputfile):
    input_params = read_input_file(inputfile)
    sets = input_params[0]
    weights = input_params[1]
    n = input_params[2]
    set_number = input_params[3]
    alg_output = run_random_rounding_n_times(100, sets, weights, n, set_number)
    output_file = open("answer.txt", 'w')
    output_file.write(str(int(alg_output[1])))
    output_file.write("\n")
    for index in alg_output[4]:
        output_file.write(str(index) + " ")
    output_file.close()

    goodAnswer = verify_output(sets, weights, n, set_number, "answer.txt")
    '''
    if(goodAnswer == False):
        output_file.open("answer.txt", 'w')
        output_file.write("BAD ANSWER")
        output_file.close()
        '''


# test list of 10
# sets = [[1,2], [1,3], [2,3], [4,5], [6,7], [8,9], [9,10], [1,2,3], [4,8,3,2], [1,4,8], [4,2,5]]
# set_number = 11
# weights = [1,5,7,3,4,6,8,4,3,7,3]
# n = 10 #U constructor
# run_random_rounding_n_times(10, sets, weights, n, set_number)

# test the input generator
# (subs, dubs, n, num_subs) = generate_input(5, 10, 3)
# print("Subsets: "+str(subs)+"\nWeights: "+str(dubs)+"\nN: "+str(n)+"\nNumber of Subsets: "+str(len(subs)))
# print_input_to_file(n, subs, dubs)

# test a max input generator file
# (subs, dubs, n, num_subs) = generate_input(1000, 500, 250)
# print_input_to_file(n, subs, dubs)

# test a max big input on the RR alg (params: n<=1000, num_subsets<=500, max_subset_size=n)
# (subs, dubs, n, num_subs) = generate_input(1000, 500, 250)
# (cov_freq, cov_weight_freq) = run_random_rounding_n_times(10000, subs, dubs, n, num_subs)
# from collections import Counter
# print("Freq of cover trial covers: "+str(Counter(cov_freq.values())))
# print("Freq of cover trial weights: "+str(Counter(cov_weight_freq.values())))

#elise_verbose_output()

# test file input parsing
sets, weights, n, set_number = read_input_file("rando-algs-input.txt");
#print(mathematica_solve(sets, weights, n, set_number))
mathematica_parse(sets, weights, n, set_number)
run_RR("rando-algs-input.txt")

# input_num_max = 500
# input_num_of_subs = 200
# input_max_sub_size = 50
# (subs, dubs, n, num_subs) = generate_input(input_num_max, input_num_of_subs, input_max_sub_size)
# print_input_to_file(n, subs, dubs)
