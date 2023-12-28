from typing import Dict



# find_value function takes a string word and a dictionary assigned,
# where keys are characters in word and values are the assigned digits.
# It returns the numerical value represented by the string word based on the assigned digits.
def find_value(word: str, assigned: Dict[str, int]) -> int:
    num = 0
    for char in word:
        num = num * 10
        num += assigned[char]
    return num


#  is_valid_assignment function in your code checks whether a partial assignment of values
# to letters is valid. Specifically, it ensures that the leading digits in the addition operation
# are not assigned the value zero. Here's a breakdown of the
def is_valid_assignment(word1: str, word2: str, result: str, assigned: Dict[str, int]) -> bool:
    if assigned[word1[0]] == 0 or assigned[word2[0]] == 0 or assigned[result[0]] == 0:
        return False
    return True

def calculate_degree_heuristic(word1: str, word2: str, result: str, variable: str) -> int:
    # Calculate the degree by counting occurrences of the variable in the words
    degree = sum(word.count(variable) for word in (word1, word2, result))
    return degree

def minimum_remaining_value(letters, assigned, word1, word2, result):
    # Sort the letters based on the length of their remaining possible values (MRV heuristic)
    letters.sort(key=lambda x: (len(x[1]), calculate_degree_heuristic(word1, word2, result, x[0])))

    # Select the variable with the minimum remaining values and sort in increasing order

    cur_letter, remaining_values = min(letters, key=lambda x: sorted(x[1]))
    return cur_letter

def cryptarithmetic_backtracking(word1: str, word2: str, result: str, letters: str, assigned: Dict[str, int], solutions: list):
    if not letters:
        if is_valid_assignment(word1, word2, result, assigned):
            num1 = find_value(word1, assigned)
            num2 = find_value(word2, assigned)
            num_result = find_value(result, assigned)
            if num1 + num2 == num_result:
                solutions.append((f'{num1} + {num2} = {num_result}', assigned.copy()))

        return

    cur_letter = minimum_remaining_value(letters, assigned, word1, word2, result)

    #The loop for num in range(10): iterates over the possible values (0 to 9) that can be assigned
    # to the current letter (cur_letter). Before assigning the value, it checks if the value is not
    # already assigned to any other letter (if num not in assigned.values():). This condition ensures
    # that each digit is used only once in the assignment

    for num in range(10):
        if num not in assigned.values():
            assigned[cur_letter] = num
            cryptarithmetic_backtracking(word1, word2, result, letters[1:], assigned, solutions)
            assigned.pop(cur_letter)

def write_solution_to_file(solution, output_file):
    with open(output_file, 'w') as file:
        for key, value in solution.items():
            file.write(f'{key}: {value}\n')


# preprocessing  it reads input file and odes input validation for number of lines = 3
# checks if each word is alphabetic characters
# generates letters tuple list
#Each tuple consists of a character from the puzzle words and a set of values from 0 to 9,
# representing the possible digits that can be assigned to that character.
# calls backtracking fun  and print and write solutions.
def preprocessing_input(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) != 3:
            print('Invalid input file. It should contain three lines.')
            return

        word1 = lines[0].strip().upper()
        word2 = lines[1].strip().upper()
        result = lines[2].strip().upper()

        if not word1.isalpha() or not word2.isalpha() or not result.isalpha():
            print('Invalid input. Inputs should only consist of alphabets.')
            return

    letters = [(char, set(range(10))) for char in sorted(set(word1) | set(word2) | set(result))]
    if len(result) > max(len(word1), len(word2)) + 1 or len(letters) > 10:
        print('0 Solutions!')
        return

    solutions = []
    cryptarithmetic_backtracking(word1, word2, result, letters, {}, solutions)
    if solutions:
        print('\nSolutions:')
        for soln in solutions:
            print(f'{soln[0]}\t{soln[1]}')

        # Write the first solution to an output file
        output_file = 'output_sol.txt'
        write_solution_to_file(soln[1], output_file)
        print(f'Solution written to {output_file}')
    else:
        print('No solutions found.')

if __name__ == '__main__':
    print('CRYPTARITHMETIC PUZZLE SOLVER (CSP)')

    # Specify the input file path
    input_file_path = 'input4.txt'

    # Call the  function with the input file path
    preprocessing_input(input_file_path)

