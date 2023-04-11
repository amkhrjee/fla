##########################################
#   Author: Aniruddha Mukherjee         #
#   Roll No. CSB21076                   #
#########################################

# Note: by default table formatting is disabled.
# after adding beautifultable via `pip install beautifultable` to the environment
# you can uncomment the relevant portions to see the formatted table as the output

# from beautifultable import BeautifulTable as btable

nfa_transition_table = {
    'q0': {'0': ['q0'], '1': ['q0', 'q1']},
    'q1': {'0': [], '1': ['q2']},
    'q2': {'0': [], '1': []}
}


def nfa_to_dfa(transition_table, start_state, end_states):
    # initialization
    dfa_transition_table = {}
    untracked_states = [start_state]
    for curr_state in untracked_states:
        # checks if there are multiple states
        if isinstance(curr_state, list):
            curr_state_str = "".join(sorted(curr_state))
            # declaring as sets for performing union
            states_for_zero = set()
            states_for_one = set()
            # performing union for each input
            for state in curr_state:
                states_for_zero.update(transition_table[state].get('0', []))
                states_for_one.update(transition_table[state].get('1', []))
            # producing the strings for the table
            if len(states_for_zero):
                zero_str = "".join(sorted(states_for_zero))
            else:
                zero_str = 'z'

            if len(states_for_one):
                one_str = "".join(sorted(states_for_one))
            else:
                one_str = 'z'
            # adding the strings to the table
            dfa_transition_table[curr_state_str] = {
                '0': zero_str,
                '1': one_str
            }
            # adding the new states encountered to our list of untracked states
            if sorted(list(states_for_zero)) not in untracked_states:
                untracked_states.append((sorted(list(states_for_zero))))
            if sorted(list(states_for_one)) not in untracked_states:
                untracked_states.append(sorted(list(states_for_one)))
        # dealing with empty states
        elif curr_state == 'z':
            dfa_transition_table['z'] = {'0': 'z', '1': 'z'}
        # dealing with single state
        else:
            dfa_transition_table.update({curr_state: {'0': None, '1': None}})
            # dealing with each input
            for symbol in transition_table[curr_state]:
                target_states = transition_table[curr_state][symbol]
                # for empty states
                if len(target_states) == 0:
                    dfa_transition_table[curr_state][symbol] = 'z'
                    if 'z' not in untracked_states:
                        untracked_states.append('z')
                # for single states on input
                elif len(target_states) == 1:
                    state_str = "".join(target_states)
                    dfa_transition_table[curr_state][symbol] = state_str
                    if state_str not in untracked_states:
                        untracked_states.append(state_str)
                # for multiple states on input
                else:
                    target_state_str = "".join(sorted(target_states))
                    dfa_transition_table[curr_state][symbol] = target_state_str
                    if sorted(target_states) not in untracked_states:
                        untracked_states.append(sorted(target_states))
    dfa_end_states = []
    # dealing with end states
    for each_end_state in end_states:
        for each_state in dfa_transition_table:
            if each_end_state in each_state:
                dfa_end_states.append(each_state)
    return (dfa_transition_table, start_state, dfa_end_states)


# test
dfa_table, start_state, end_states = nfa_to_dfa(
    nfa_transition_table, 'q0', ['q2'])

# table = btable()
# for state in dfa_table:
#     if state is start_state:
#         table.rows.append(
#             ["->" + state, dfa_table[state]['0'], dfa_table[state]['1']])
#     elif state in end_states:
#         table.rows.append(
#             ["*" + state, dfa_table[state]['0'], dfa_table[state]['1']])
#     else:
#         table.rows.append(
#             [state, dfa_table[state]['0'], dfa_table[state]['1']])

# table.columns.header = ["States", "0", "1"]
# print(table)

# without formatting:
for state in dfa_table:
    if state in start_state:
        print("-> " + state + " = " + "['0' : " + dfa_table[state]
              ['0'] + ", '1' : " + dfa_table[state]['1'] + "]")
    elif state in end_states:
        print("* " + state + " = " + "['0' : " + dfa_table[state]
              ['0'] + ", '1' : " + dfa_table[state]['1'] + "]")
    else:
        print(state + " = " + "['0' : " + dfa_table[state]
              ['0'] + ", '1' : " + dfa_table[state]['1'] + "]")
