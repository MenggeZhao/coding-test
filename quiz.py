#!/usr/bin/env python3


def custom_compare(a, b):
    """
    Custom comparison to handle mixed data types
    """
    try:
        return a > b
    except TypeError:
        # Convert to string if direct comparison fails

        return str(a) > str(b) 

def merge(left, right):
    """
    Merge the split sub-lists.
    """
    sorted_list = []
    i = j = 0

    while i < len(left) and j < len(right):
        if custom_compare(left[i], right[j]):
            sorted_list.append(right[j])
            j += 1
        else:
            sorted_list.append(left[i])
            i += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list


def merge_sort(arr):
    """
    Sort the reversed list manually using Merge Sort
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)




def reverse_list(l: list):
    """
    TODO: Reverse a list without using any built in functions

    The function should return a sorted list.
    Input l is a list which can contain any type of data.
    """

    # reverse the list
    reversed_list = l[::-1]

    return merge_sort(reversed_list)



##=========================Sudoku=================================

def is_valid(board, row, col, num):
    """
    Check if num can be placed at board[row][col]
    return: bool - Returns True num can be placed at board[row][col]. Returns False otherwise.
    """
    box_row, box_col = row // 3 * 3, col // 3 * 3

    # Row check
    if num in board[row]:
        return False

    # Column check
    if num in (board[i][col] for i in range(9)):
        return False

    # Box check
    if num in (board[r][c] for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3)):
        return False

    return True




def find_empty_cell(board):
    """
    Finds the empty cell with the least possible values
    return: tuple - Returns a tuple consisting of row_num, col_num and a set of possible num
    """
    # Max of min_option is 9
    min_options = 9  

    best_cell = None

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                options = {num for num in range(1, 10) if is_valid(board, r, c, num)}
                if len(options) < min_options:
                    min_options = len(options)
                    best_cell = (r, c, options)

                # Fastest possible choice
                if min_options == 1:  
                    return best_cell

    # Returns (row_num, col_num, a set of possible num) or None if solved
    return best_cell  


def backtrack(board):
    """
    Depth-First Search Recursive function to fill in the numbers.

    return: boolean - Returns True if num can be filled in the cell. Returns False otherwise.
    """
    # Find the best empty cell to fill num first
    empty_cell = find_empty_cell(board)

    if not empty_cell:
        # Solved
        return True  

    row, col, options = empty_cell  

    # Try numbers from least-constrained set
    for num in options:  
        board[row][col] = num

        if backtrack(board):
            return True

        # go back to be empty cell
        board[row][col] = 0  

    # No valid number found, backtrack
    return False  

def final_check(board):
    """
    Check if the solution keeps the rules of Sudoku
    return: boolean - Returns True if solution keeps the rules of Sudoku. Returns False otherwise.
    """
    
    
    # check row sum == 45
    for i in range(len(board)):
        if sum(board[i]) != sum(range(1, 9+1)): return False
        
        
    # check col sum == 45
    for j in range(len(board[0])):
        col_sum = 0
        for i in range(len(board)):
            col_sum += board[i][j]
          
        if col_sum != sum(range(1, 9+1)): return False
        
    # check box sum == 45
    for i in range(3):
        for j in range(3):
            box_sum = 0
            box_sum += board[3*i][3*j] + board[3*i + 1][3*j] + board[3*i + 2][3*j] + board[3*i][3*j + 1] + board[3*i + 1][3*j + 1] + board[3*i + 2][3*j + 1] + board[3*i][3*j + 2] + board[3*i + 1][3*j + 2] + board[3*i + 2][3*j + 2]
            
            if box_sum != sum(range(1, 9+1)): return False
            
        
      
    return True

def solve_sudoku(matrix):
    """
    TODO: Write a programme to solve 9x9 Sudoku board.
 
    Sudoku is one of the most popular puzzle games of all time. The goal of Sudoku is to fill a 9×9 grid with numbers so that each row, column and 3×3 section contain all of the digits between 1 and 9. As a logic puzzle, Sudoku is also an excellent brain game.

    The input matrix is a 9x9 matrix. You need to write a program to solve it.
    
    param matrix: List[List[int]] - A 9x9 Sudoku grid with 0s representing empty cells.
    return: bool - Returns True if the Sudoku is solved, False otherwise.

    """
    if backtrack(matrix) and final_check(matrix):
        # Return solved Sudoku board
        return matrix  
    else:
        # No solution exists
        return None  

def test_reverse_list():
    """
    Test reverse_list(l: list) with multiple cases
    """
    test_cases = [
        {
            "name": "Reverse a list single data type",
            "input": [3, 1, 4, 1, 5, 9, 12, 34, 15],
            "expected": [1, 1, 3, 4, 5, 9, 12, 15, 34]
        },
       
        {
            "name": "Reverse a list with mixed data types",
            "input": ["apple", 3, "banana", 1],
            "expected": [1, 3, 'apple', 'banana'] # numbers first, then strings
        },
        {
            "name": "Reverse an empty list",
            "input": [],
            "expected": []
        },
        {
            "name": "Reverse a list with a single element",
            "input": [42],
            "expected": [42]
        },
        {
            "name": "Reverse a list with mixed data types",
            "input": [True, False, 10, "hello"],
            "expected": [False, True, 10, 'hello'] # Boolean follows integer logic: False=0, True=1
        },
        {
            "name": "Reverse a list with nested lists",
            "input": [[5, 6], [3, 4], [1, 2]],
            "expected": [[1, 2], [3, 4], [5, 6]]
        }
    ]

    for test in test_cases:
        print(f"Running test: {test['name']}")
        
        result = reverse_list(test["input"])
        
        assert result == test["expected"], f"Failed: Expected {test['expected']}, but got {result}"
    
        
        print("Passed.")




    
def test_solve_sudoku():
    """
    Test solve_sudoku(matrix) with multiple cases
    """
    
    test_cases = [
        {
            "name": "solvable puzzle",
            "input": [
               
                    [0, 0, 3, 0, 2, 0, 6, 0, 0],
                    [9, 0, 0, 3, 0, 5, 0, 0, 1],
                    [0, 0, 1, 8, 0, 6, 4, 0, 0],
                    [0, 0, 8, 1, 0, 2, 9, 0, 0],
                    [7, 0, 0, 0, 0, 0, 0, 0, 8],
                    [0, 0, 6, 7, 0, 8, 2, 0, 0],
                    [0, 0, 2, 6, 0, 9, 5, 0, 0],
                    [8, 0, 0, 2, 0, 3, 0, 0, 9],
                    [0, 0, 5, 0, 1, 0, 3, 0, 0]
                       ],
            "expected": [
                    [4, 8, 3, 9, 2, 1, 6, 5, 7],
                    [9, 6, 7, 3, 4, 5, 8, 2, 1],
                    [2, 5, 1, 8, 7, 6, 4, 9, 3],
                    [5, 4, 8, 1, 3, 2, 9, 7, 6],
                    [7, 2, 9, 5, 6, 4, 1, 3, 8],
                    [1, 3, 6, 7, 9, 8, 2, 4, 5],
                    [3, 7, 2, 6, 8, 9, 5, 1, 4],
                    [8, 1, 4, 2, 5, 3, 7, 6, 9],
                    [6, 9, 5, 4, 1, 7, 3, 8, 2]
                        ]
        },
        {
            "name": "Already solved puzzle",
            "input": [
                [4, 8, 3, 9, 2, 1, 6, 5, 7],
                [9, 6, 7, 3, 4, 5, 8, 2, 1],
                [2, 5, 1, 8, 7, 6, 4, 9, 3],
                [5, 4, 8, 1, 3, 2, 9, 7, 6],
                [7, 2, 9, 5, 6, 4, 1, 3, 8],
                [1, 3, 6, 7, 9, 8, 2, 4, 5],
                [3, 7, 2, 6, 8, 9, 5, 1, 4],
                [8, 1, 4, 2, 5, 3, 7, 6, 9],
                [6, 9, 5, 4, 1, 7, 3, 8, 2]
            ],
            "expected": [
                [4, 8, 3, 9, 2, 1, 6, 5, 7],
                [9, 6, 7, 3, 4, 5, 8, 2, 1],
                [2, 5, 1, 8, 7, 6, 4, 9, 3],
                [5, 4, 8, 1, 3, 2, 9, 7, 6],
                [7, 2, 9, 5, 6, 4, 1, 3, 8],
                [1, 3, 6, 7, 9, 8, 2, 4, 5],
                [3, 7, 2, 6, 8, 9, 5, 1, 4],
                [8, 1, 4, 2, 5, 3, 7, 6, 9],
                [6, 9, 5, 4, 1, 7, 3, 8, 2]
            ]
        },
        {
            "name": "Unsolvable puzzle",
            "input": [
                # Duplicated 3 in row 1, and col 4, and box 2
                [0, 0, 3, 3, 2, 0, 6, 0, 0],
                [9, 0, 0, 3, 0, 5, 0, 0, 1],
                [0, 0, 1, 8, 0, 6, 4, 0, 0],
                [0, 0, 8, 1, 0, 2, 9, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 8],
                [0, 0, 6, 7, 0, 8, 2, 0, 0],
                [0, 0, 2, 6, 0, 9, 5, 0, 0],
                [8, 0, 0, 2, 0, 3, 0, 0, 9],
                [0, 0, 5, 0, 1, 0, 3, 0, 0]
            ],
            # No solution exists
            "expected": None  
        },
        {
            "name": "Empty puzzle",
            # All cells are empty
            "input": [[0] * 9 for _ in range(9)],  
            "expected": None 
        }
    ]

    for test in test_cases:
        print(f"Running test: {test['name']}")
        print(test["input"])
        result = solve_sudoku(test["input"])
        
        assert result == test["expected"], f"Failed: Expected {test['expected']}, but got {result}"

        print("Passed.")




def main():
    
    print("Running testing cases for reverse_list(l: list)")
    
    # Run the test function
    test_reverse_list()
    
    
    print("Running testing cases for solve_sudoku(matrix)")
    
    # Run the tests
    test_solve_sudoku()

if __name__ == "__main__":
    main()