##########################################
#   Author: Aniruddha Mukherjee         #
#   Roll No. CSB21076                   #
#########################################


# We represent the DFA transition table with a dictionray
# DFA that accepts strings ending with 11
#      | 0  | 1 |
# -----|----|---|
# q0   | q1 | q2|
# q1   | q1 | q2|
# *q2  | q0 | q2|


dfa_transition_table = {
    'q0': {'0': 'q1', '1': 'q2'},
    'q1': {'0': 'q1', '1': 'q2'},
    'q2': {'0': 'q0', '1': 'q2'},
}

# The following function determines whether a given input string is accepted or rejected by a DFA.

# transition_table: the transition table of the DFA
# start_state: the starting state of the DFA
# end_states: a list of the accepting states of the DFA
# input_string: the input string to be processed by the DFA


def dfa_accepts(transition_table, start_state, end_states, input_string):
    curr_state = start_state
    for each_input in input_string:
        if each_input not in transition_table[curr_state]:
            return False
        curr_state = transition_table[curr_state][each_input]
    return curr_state in end_states


# test
if dfa_accepts(dfa_transition_table, 'q0', ['q2'], '00100011'):
    print("String Accepted", )
else:
    print("String Not Accepted")
