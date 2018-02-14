import numpy as np
import sys

def unpack(N, t, backtrack):
    tags = np.zeros(N)
    i = N-1

    while i >= 0:
        tags[i] = t
        if i == 0:
            break
        t = backtrack[(t,i)]
        i -= 1
    return tags



def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    y = np.zeros(N,dtype=int)             # zero vector of size N

    # print "Emission scores:"
    # for row in emission_scores:
    #     print row
    #
    # print "Transition scores:"
    # for row in trans_scores:
    #     print row
    #
    # print "Start scores:"
    # for row in start_scores:
    #     print row
    #
    # print "End scores:"
    # for row in end_scores:
    #     print row

    table = {}
    backtrack = {}

    # filling up first column (first word)
    for t in range(L):
        table[(t,0)] = start_scores[t] + emission_scores[0][t]

    # rest of the columns
    for i in range(1,N):
        for t in range(L):
            table[(t,i)] = -sys.maxint      # Initialization to find max value

            for t_prev in range(L):         # loop over all previous tags
                temp_score = table[(t_prev, i-1)] + trans_scores[t_prev][t] + emission_scores[i][t]
                if temp_score > table[(t,i)]:
                    table[(t, i)] = temp_score  # update the entry
                    backtrack[(t, i)] = t_prev  # add backpointer
            #table[(t, i)] += emission_scores[i][t]

    # last tag -> end of sentence
    best_tag = 0                # dummy initialization
    best_score = -sys.maxint    # Initialization to find max value
    for t_prev in range(L):     # loop over tags of last word
        temp_score = table[(t_prev, N - 1)] + end_scores[t_prev]
        if temp_score > best_score:
            best_score = temp_score             # update best_score
            backtrack[(0, int(N))] = t_prev     # add backpointer
            best_tag = t_prev                   # update best_tag

    #best_score = table[(0, N)]

    # backtracking to find the best_sequence y
    for i in range(N-1, -1, -1):
        y[i] = best_tag
        if i == 0:
            break
        # go to previous tag
        best_tag = backtrack[(best_tag, i)]

    return (best_score, y)
