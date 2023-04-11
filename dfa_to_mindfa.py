##########################################
#   Author: Aniruddha Mukherjee         #
#   Roll No. CSB21076                   #
#########################################
from beautifultable import BeautifulTable as btable

dfa_transition_table = {
    'a': {'0': 'b', '1': 'c'},
    'b': {'0': 'b', '1': 'd'},
    'c': {'0': 'b', '1': 'c'},
    'd': {'0': 'b', '1': 'e'},
    'e': {'0': 'b', '1': 'c'},
}


def is_equal(item_a, item_b):
    if type(item_a) != type(item_b):
        return False
    else:
        if not (isinstance(item_a, list) and isinstance(item_b, list)):
            if item_a == item_b:
                return True
            else:
                return False
        else:
            if len(item_a) != len(item_b):
                return False
            else:
                for each_a, each_b in zip(item_a, item_b):
                    if is_equal(each_a, each_b):
                        return True
                    else:
                        return False


def get_equivalent_states(transition_table, prev_equivalence_list, equivalence_list):
    if is_equal(prev_equivalence_list, equivalence_list):
        return equivalence_list
    else:
        temp_list = []
        new_list = []
        temp_state_for_input_zero = ''
        temp_state_for_input_one = ''
        for group in equivalence_list:
            curr_group = group
            temp_state_for_input_zero = transition_table[group[0]]['0']
            temp_state_for_input_one = transition_table[group[0]]['1']
            for member in group:
                for input in transition_table[member]:
                    if input == '0':
                        if transition_table[member][input] != temp_state_for_input_zero:
                            curr_group.remove(member)
                            temp_list.append(member)
                    elif input == '1':
                        if transition_table[member][input] != temp_state_for_input_one:
                            curr_group.remove(member)
                            temp_list.append(member)
            if len(curr_group) > 0:
                new_list.append(curr_group)
        if len(temp_list) > 0:
            new_list.append(temp_list)
        return get_equivalent_states(
            transition_table, equivalence_list, sorted(new_list))


def dfa_to_mindfa(transition_table, start_state, end_states):
    equivalence_lists = [
        [x for x in transition_table if x not in end_states], [x for x in end_states]]
    equivalent_list = get_equivalent_states(
        transition_table, [], equivalence_lists)
    new_state_str_list = []
    for group in equivalent_list:
        new_state_str = "".join(sorted(group))
        new_state_str_list.append(new_state_str)
        for member in group:
            input_zero = transition_table[member]['0']
            input_one = transition_table[member]['1']
            for each_str in new_state_str_list:
                if transition_table[member]['0'] in each_str:
                    input_zero = each_str
                if transition_table[member]['1'] in each_str:
                    input_one = each_str
            del transition_table[member]
        transition_table[new_state_str] = {
            '0': "".join(sorted(input_zero)),
            '1': "".join(sorted(input_one))}
    return (transition_table, start_state, end_states)


# test
dfa_table, start_state, end_states = dfa_to_mindfa(
    dfa_transition_table, 'a', ['e'])
table = btable()

for state in dfa_table:
    if start_state in state:
        table.rows.append(
            ["-> " + state, dfa_table[state]['0'], dfa_table[state]['1']])
    elif state in end_states:
        table.rows.append(
            ["* " + state, dfa_table[state]['0'], dfa_table[state]['1']])
    else:
        table.rows.append(
            [state, dfa_table[state]['0'], dfa_table[state]['1']])

table.columns.header = ["States", "0", "1"]
print(table)
