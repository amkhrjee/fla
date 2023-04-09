##########################################
#   Author: Aniruddha Mukherjee         #
#   Roll No. CSB21076                   #
#########################################

dfa_transition_table = {
    'a': {'0': 'b', '1': 'c'},
    'b': {'0': 'b', '1': 'd'},
    'c': {'0': 'b', '1': 'c'},
    'd': {'0': 'b', '1': 'e'},
    'e': {'0': 'b', '1': 'c'},
}


# def get_equivalent_states(transition_table, start_state, end_states, equivalence_lists):


def dfa_to_mindfa(transition_table, start_state, end_states):
    equivalence_lists = []
    equivalent_states = get_equivalent_states(
        transition_table, start_state, end_states, equivalence_lists)
    for states in equivalent_states:
        new_state_str = "".join(sorted(states))
        zero_str = set()
        one_str = set()
        for state in states:
            zero_str.add(transition_table[state]['0'])
            one_str.add(transition_table[state]['1'])
            del transition_table[state]
        transition_table[new_state_str] = {
            '0': "".join(zero_str),
            '1': "".join(one_str)
        }
    return (transition_table, start_state, end_states)


