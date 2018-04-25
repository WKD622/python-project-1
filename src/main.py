# dozwolone operatory:
# * iloczyn
# + suma
# - suma wykluczająca
# > implikacja
# mała litera
# = równoważność
# ( ) nawiasy
import itertools

ops = {"+", "-", "*", "~"}


# operations

# logic "and" operator
def _and(X, Y):
    return X * Y


# logic "or" operator
def _or(X, Y):
    if X == 1 or Y == 1: return 1


# logic "xor" operator
def _xor(X, Y):
    if (X == 0 and Y == 1) or (Y == 0 and X == 1):
        return 1
    else:
        return 0


# logic "negation" operator
def _neg(X):
    if X == 0:
        return 1
    else:
        return 0


# logic "impication" operator
def _implication(X, Y):
    if (X == 1 and Y == 0):
        return 1
    else:
        return 0


# logic "equivalence" operator
def _equivalence(X, Y):
    if X == Y:
        return 1
    else:
        return 0


# deletes white spaces in token
def delete_spaces(tokens):
    return tokens.replace(' ', '')


# converts infix notation to postfix notation
def infix_postfix(tokens):
    prec = {'~': 10, '*': 5, '+': 4, '(': 0, ')': 0}
    output = []
    stack = []
    for item in tokens:
        # pop elements while elements have lower precedence
        if item in ops:
            while stack and prec[stack[-1]] >= prec[item]:
                output.append(stack.pop())
            stack.append(item)
        # delay precedence. append to stack
        elif item == "(":
            stack.append("(")
        # flush output until "(" is reached
        elif item == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            # should be "("
            stack.pop()
        # operand. append to output stream
        else:
            output.append(item)
    # flush stack to output54m
    while stack:
        output.append(stack.pop())
    return output


# returns a set of variables from token
def set_of_variables(tokens):
    return {x for x in tokens if x not in ops}


# returns a list lists of all variatons for variables
def list_of_variations(length):
    return ["".join(item) for item in itertools.product("10", repeat=length)]


# creates dictionary of values for all variables
def dictionary_of_values_for_variables(variables, values):
    val_dict = {}
    for i in range(len(variables)):
        val_dict[variables[i]] = values[i]
    return val_dict


# converts char to number
def char_to_num(c):
    if c == '0':
        return 0
    else:
        return 1


# checks one solution for token
def check_solution(token, variation, variables_list):
    stack = []
    variables_dict = dictionary_of_values_for_variables(variables_list, variation)
    for c in token:
        if c not in ops:
            stack.append(char_to_num(variables_dict[c]))
        else:
            if c == '~':
                A = stack.pop()
                stack.append(_neg(A))
            else:
                A = stack.pop()
                B = stack.pop()
                if c == '+':
                    stack.append(_or(A, B))
                elif c == '-':
                    stack.append(_xor(A, B))
                elif c == '*':
                    stack.append(_and(A, B))
    if stack.pop() == 1:
        return True
    else:
        return False


# finds all solutions for token
def find_solutions(token, variables_list, variations):
    solutions = []

    for v in variations:
        if check_solution(token, v, variables_list) == 1:
            solutions.append(v)
    list_of_dictionaries = []
    for s in solutions:
        list_of_dictionaries.append(dictionary_of_values_for_variables(variables_list, s))
    return list_of_dictionaries


# counts 1 in dictionary
def count_ones(dictionary):
    count = 0
    for value in dictionary.values():
        if value == '1':
            count = count + 1
    return count


# divides solutions for lists with same amount of 1
def divide_for_groups(list_of_dictionaries):
    groups = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
              [], [], []]
    for element in list_of_dictionaries:
        c = count_ones(element)
        groups[c].append(element)
    return groups


# counts differences between two dictionaries of variables and their values
def count_differences(dict_a, dict_b):
    count = 0
    for key in dict_a.keys():
        if dict_b[key] != dict_a[key]:
            count = count + 1
    return count


# crosses out differences between dictionaries and returns new dictionarie
def cross_out_differences(dict_a, dict_b):
    dict_c = dict_a.copy()
    for key in dict_a.keys():
        if dict_b[key] != dict_a[key]:
            dict_c[key] = '*'
        else:
            dict_c[key] = dict_a[key]
    return dict_c


# count stars
def count_stars(dictionarie):
    count = 0
    for val in dictionarie.values():
        if val == '*':
            count = count + 1
    return count


# compares choosen groups of solutions, with different number of 1
def compare_groups(group_a, group_b, together):
    out = []
    for dict_a in group_a:
        for dict_b in group_b:
            if count_differences(dict_a, dict_b) == 1:
                if dict_a in together:
                    together.remove(dict_a)
                if dict_b in together:
                    together.remove(dict_b)
                dict_c = cross_out_differences(dict_a, dict_b)
                out.append(dict_c)
    return out


def groups_to_one_list(groups):
    new_list = []
    for element1 in groups:
        for element2 in element1:
            new_list.append(element2)
    return new_list


# Quines-McCluskey algorithm
def quine_mc_cluskey(solutions, number_of_variables):
    check = True
    crossed = []
    not_used = []
    groups = divide_for_groups(solutions)
    while (check):
        crossed_copy = crossed
        for num in range(number_of_variables):
            together = groups[num] + groups[num + 1]
            crossed.append(compare_groups(groups[num], groups[num + 1], together))
            not_used.append(together)
        groups = divide_for_groups(groups_to_one_list(crossed))
        if crossed_copy == crossed:
            not_used.append(groups_to_one_list(groups))
            return groups_to_one_list(not_used)


# from {'B': '0', 'C': '0', 'A': '1'} to ['~', 'B', '~', 'C', 'A']
def dictionarie_to_list(dictionarie):
    string = []
    for key in dictionarie.keys():
        if dictionarie[key] == '1':
            string.append(key)
            string.append('*')
        elif dictionarie[key] == '0':
            string.append('~')
            string.append(key)
            string.append('*')
    del [string[-1]]
    return string


# from [{'B': '0', 'C': '0', 'A': '1'}, {'B': '1', 'C': '0', 'A': '1'}, {'B': '*', 'C': '0', 'A': '1'}] to
# [['~', 'B', '~', 'C', 'A'], ['B', '~', 'C', 'A'], ['~', 'C', 'A']]
def create_list_of_lists_of_options(to_choose_from):
    to_choose_from_list = []
    for dict in to_choose_from:
        to_choose_from_list.append(dictionarie_to_list(dict))
    return to_choose_from_list


def check_solution2(token, variables_dict):
    stack = []
    for c in token:
        if c not in ops:
            stack.append(char_to_num(variables_dict[c]))
        else:
            if c == '~':
                A = stack.pop()
                stack.append(_neg(A))
            else:
                A = stack.pop()
                B = stack.pop()
                if c == '+':
                    stack.append(_or(A, B))
                elif c == '-':
                    stack.append(_xor(A, B))
                elif c == '*':
                    stack.append(_and(A, B))
    if stack.pop() == 1:
        return True
    else:
        return False


def create_list_of_solutions_for_sentence(solutions, sentence):
    list = []
    for s in solutions:
        if check_solution2(sentence, s):
            list.append(s)
    return list


def create_list_of_sentences_for_solution(solution, sentences):
    list = []
    for s in sentences:
        if check_solution2(infix_postfix(s), solution):
            list.append(s)
    return list


# main
start_sentence = "A*B*~C+A*~B*~C"
sentence = infix_postfix(delete_spaces(start_sentence))
variables = set_of_variables(sentence)
variables_list = list(variables)
variations = list_of_variations(len(variables_list))
solutions = find_solutions(sentence, variables_list, variations)
to_choose_from = quine_mc_cluskey(solutions, len(variables_list))
to_choose_from_list = create_list_of_lists_of_options(to_choose_from)
list_of_solutions_for_sentences = []
list_of_sentences_for_solutions = []

for s in to_choose_from_list:
    list_of_solutions_for_sentences.append(create_list_of_solutions_for_sentence(solutions, infix_postfix(s)))

# print("TO CHOOSE FROM: ",to_choose_from_list)
# print("SOLUTIONS FOR SENETECES: ", list_of_solutions_for_sentences)
# print()
for s in solutions:
    list_of_sentences_for_solutions.append(create_list_of_sentences_for_solution(s, to_choose_from_list))

# print("SOLUTIONS: ", solutions)
# print("SENTENCES FOR SOLUTIONS: ", list_of_sentences_for_solutions)
# print()
# print()

output = []

# najpierw dodaje do output te elementy ktore tam na pewno beda i beda bo zajmuja jako jedyne kolumne
for sentences in list_of_sentences_for_solutions:
    if (len(sentences)) == 1:
        for elem in sentences:
            output.append(elem)

# teraz usuwam te elementy z tych ktore mam do wyboru
for elem in output:
    if elem in to_choose_from_list:
        to_choose_from_list.remove(elem)

# teraz usuwam wszystkie rozwiazania z listy ktore sa juz zalatwione
list_to_delete = []
for elem in output:
    for i in range(len(solutions)):
        if elem in list_of_sentences_for_solutions[i]:
            del (solutions[i])
            list_to_delete.append(i)

# teraz usuwam wszystkie rozwiazania z listy ktore sa juz zalatwione
list_to_delete.sort()
for i in reversed(list_to_delete):
    del (list_of_sentences_for_solutions[i])

#print("SENTENCES FOR SOLUTIONS: ", list_of_sentences_for_solutions)
#print("SOLUTIONS: ", solutions)

# tworze maski bitowe do sprawdzania wszystkich moliwosci z to_choose_from
list_of_lists_mask = []
list_of_masks = ["".join(item) for item in itertools.product("10", repeat=len(to_choose_from_list))]

for elem in list_of_masks:
    list_of_lists_mask.append(list(elem))

pom1 = True
for i in range(len(to_choose_from_list)+1):
    for elem1 in list_of_lists_mask:
        pom = []
        if elem1.count('1') == i:
            for j in range(len(elem1)):
                if elem1[j] == '1':
                    pom.append(to_choose_from_list[j])
        #print("POM:", pom)
        copy = list_of_sentences_for_solutions[:]
        #print("COPY:", copy)
        h = 0
        for elem2 in pom:
            for elem3 in copy:
                if elem2 in elem3:
                    h = h + 1
        #print(i);
        #print(len(copy))
        if h == len(copy) and pom1 == True:
            print("Wyrazeniem uproszczonym jest suma wyrazen w podlistach")
            print(output + pom)
            pom1 = False

