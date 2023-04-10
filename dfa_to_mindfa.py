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
    if len(equivalence_list) > 0:
        # print(equivalence_list)
        if is_equal(prev_equivalence_list, equivalence_list):
            return equivalence_list
        else:
            temp_list = []
            new_list = []
            temp_state_for_input_zero = ''
            temp_state_for_input_one = ''
            for group in equivalence_list:
                # print("OG Group: " + str(group))
                curr_group = group
                if len(group) > 1:
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
                    # print("CurrGroup: " + str(curr_group))
                    new_list.append(curr_group)
            if len(temp_list) > 0:
                # print("temp_list: " + str(temp_list))
                new_list.append(temp_list)
            return get_equivalent_states(
                transition_table, equivalence_list, sorted(new_list))


def dfa_to_mindfa(transition_table, start_state, end_states):
    equivalence_lists = [
        [x for x in transition_table if x not in end_states], [x for x in end_states]]
    equivalent_list = get_equivalent_states(
        transition_table, [], equivalence_lists)
    print(equivalent_list)
    for group in equivalent_list:
        if len(group) > 1:
            new_state_str = "".join(sorted(group))
            for state in group:
                input_zero = set()
                input_one = set()
                input_zero.add(transition_table[state]['0'])
                input_one.add(transition_table[state]['1'])
                del transition_table[state]
            transition_table[new_state_str] = {
                '0': "".join(sorted(input_zero)),
                '1': "".join(sorted(input_one))
            }
    return (transition_table, start_state, end_states)


# test
dfa_table, start_state, end_states = dfa_to_mindfa(
    dfa_transition_table, 'a', ['e'])
table = btable()

for state in dfa_table:
    if state is start_state:
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
