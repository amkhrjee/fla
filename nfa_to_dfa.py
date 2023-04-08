##########################################
#   Author: Aniruddha Mukherjee         #
#   Roll No. CSB21076                   #
#########################################
from beautifultable import BeautifulTable as btable

nfa_transition_table = {
    'q0': {'0': ['q0'], '1': ['q0', 'q1']},
    'q1': {'0': [], '1': ['q2']},
    'q2': {'0': [], '1': []}
}


def nfa_to_dfa(transition_table, start_state, end_states):
    dfa_transition_table = {}
    untracked_states = [start_state]
    for curr_state in untracked_states:
        if isinstance(curr_state, list):
            curr_state_str = "".join(sorted(curr_state))
            states_for_zero = set()
            states_for_one = set()
            for state in curr_state:
                states_for_zero.update(transition_table[state].get('0', []))
                states_for_one.update(transition_table[state].get('1', []))
            if len(states_for_zero):
                zero_str = "".join(sorted(states_for_zero))
            else:
                zero_str = 'z'

            if len(states_for_one):
                one_str = "".join(sorted(states_for_one))
            else:
                one_str = 'z'

            dfa_transition_table[curr_state_str] = {
                '0': zero_str,
                '1': one_str
            }

            if sorted(list(states_for_zero)) not in untracked_states:
                untracked_states.append((sorted(list(states_for_zero))))
            if sorted(list(states_for_one)) not in untracked_states:
                untracked_states.append(sorted(list(states_for_one)))
        elif curr_state == 'z':
            dfa_transition_table['z'] = {'0': 'z', '1': 'z'}
        else:
            dfa_transition_table.update({curr_state: {'0': None, '1': None}})
            for symbol in transition_table[curr_state]:
                target_states = transition_table[curr_state][symbol]
                if len(target_states) == 0:
                    dfa_transition_table[curr_state][symbol] = 'z'
                    if 'z' not in untracked_states:
                        untracked_states.append('z')
                elif len(target_states) == 1:
                    state_str = "".join(target_states)
                    dfa_transition_table[curr_state][symbol] = state_str
                    if state_str not in untracked_states:
                        untracked_states.append(state_str)
                else:
                    target_state_str = "".join(sorted(target_states))
                    dfa_transition_table[curr_state][symbol] = target_state_str
                    if sorted(target_states) not in untracked_states:
                        untracked_states.append(sorted(target_states))
    dfa_end_states = []
    for each_end_state in end_states:
        for each_state in dfa_transition_table:
            if each_end_state in each_state:
                dfa_end_states.append(each_state)
    return (dfa_transition_table, start_state, dfa_end_states)


dfa_table, start_state, end_states = nfa_to_dfa(
    nfa_transition_table, 'q0', ['q2'])
table = btable()


for state in dfa_table:
    if state is start_state:
        table.rows.append(
            ["->" + state, dfa_table[state]['0'], dfa_table[state]['1']])
    elif state in end_states:
        table.rows.append(
            ["*" + state, dfa_table[state]['0'], dfa_table[state]['1']])
    else:
        table.rows.append(
            [state, dfa_table[state]['0'], dfa_table[state]['1']])

table.columns.header = ["States", "0", "1"]
print(table)
