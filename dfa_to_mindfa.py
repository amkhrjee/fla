##########################################
#   Author: Aniruddha Mukherjee         #
#   Roll No. CSB21076                   #
#########################################

# Note: by default table formatting is disabled.
# after adding beautifultable via `pip install beautifultable` to the environment
# you can uncomment the relevant portions to see the formatted table as the output

# from beautifultable import BeautifulTable as btable

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
    # base case: checks equality of nested lists
    if is_equal(prev_equivalence_list, equivalence_list):
        return equivalence_list
    else:
        # creates new list containing the new equivalence classes
        temp_list = []
        new_list = []
        temp_state_for_input_zero = ''
        temp_state_for_input_one = ''
        # goes through each equivalence class in the list
        for group in equivalence_list:
            curr_group = group
            # used to check whether two members have the same transition state for the same input
            temp_state_for_input_zero = transition_table[group[0]]['0']
            temp_state_for_input_one = transition_table[group[0]]['1']
            # checks for each member of the equivalence class
            for member in group:
                # checks whether the transition state belongs to the same equivalence class
                for input in transition_table[member]:
                    # checks whether the transition state on input are the same for the members
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


def dfa_to_mindfa(dfa_transition_table, start_state, end_states):
    transition_table = dfa_transition_table
    # the final list of equivalence classes
    equivalence_lists = [
        [x for x in transition_table if x not in end_states], [x for x in end_states]]
    equivalent_list = get_equivalent_states(
        transition_table, [], equivalence_lists)
    new_state_str_list = []
    # goes through each equivalence class
    for group in equivalent_list:
        # makes new state and replaces the equivalent states
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
            # removes the old states
            del transition_table[member]
        # adds the new state
        transition_table[new_state_str] = {
            '0': "".join(sorted(input_zero)),
            '1': "".join(sorted(input_one))}
    return (transition_table, start_state, end_states)


# test
dfa_table, start_state, end_states = dfa_to_mindfa(
    dfa_transition_table, 'a', ['e'])

# table = btable()
# for state in dfa_table:
#     if start_state in state:
#         table.rows.append(
#             ["-> " + state, dfa_table[state]['0'], dfa_table[state]['1']])
#     elif state in end_states:
#         table.rows.append(
#             ["* " + state, dfa_table[state]['0'], dfa_table[state]['1']])
#     else:
#         table.rows.append(
#             [state, dfa_table[state]['0'], dfa_table[state]['1']])

# table.columns.header = ["States", "0", "1"]
# print(table)

# without formatting:
for state in dfa_table:
    if start_state in state:
        print("-> " + state + " = " + "['0' : " + dfa_table[state]
              ['0'] + ", '1' : " + dfa_table[state]['1'] + "]")
    elif state in end_states:
        print("* " + state + " = " + "['0' : " + dfa_table[state]
              ['0'] + ", '1' : " + dfa_table[state]['1'] + "]")
    else:
        print(state + " = " + "['0' : " + dfa_table[state]
              ['0'] + ", '1' : " + dfa_table[state]['1'] + "]")
