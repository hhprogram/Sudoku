assignments = []

rows = 'ABCDEFGHI'
rev_rows = 'IHGFEDCBA'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# just adding the 2 diagonals as 2 units to be added to unitlist
diag1 = [[a+b for a,b in zip(rows,cols)]]
diag2 = [[a+b for a,b in zip(rev_rows, cols)]]
unitlist = row_units + column_units + square_units + diag1 + diag2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# print(unitlist)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # print(values)
    # display(values)

    # Find all instances of naked twins
    for unit in unitlist:
        for box in unit:
            possible_twin = values[box]
            twins = []
            if len(possible_twin) == 2:
                # didn't have this intially and then all my TWINS lists would just be of length 1
                # because had the twin but not the original box that the twin was equal to
                twins.append(box)
                for peer in unit:
                    if box != peer and possible_twin == values[peer]:
                        twins.append(peer)
            # if twins:
            #     print(twins, unit)
            if twins and len(twins) == 2:
                for peer2 in unit:
                    for digit in possible_twin:
                        if peer2 not in twins and digit in values[peer2]:
                            # same thing as the elimnate method - need to reassign because replace
                            # doesn't make the change in place
                            values[peer2] = values[peer2].replace(digit,'')
    # print("solution:")
    # display(values)
    return values
    # Eliminate the naked twins as possibilities for their peers



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will
             be '123456789'.
    """
    values = []
    digits = '123456789'
    for num in grid:
        if num == '.':
            values.append(digits)
        else:
            values.append(num)
    # note this makes each element in boxes a key, and then the corresponding element in values its 
    # value   
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from 
    the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for key in values:
        if len(values[key]) == 1:
            for box in peers[key]:
                # remember to reassign to values[box] - before just did:
                # values[box].replace(values[key],'') and was getting a terribly wrong board
                values[box] = values[box].replace(values[key],'')
    return values



def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, 
    assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
                # values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        # values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values): 
    values = reduce_puzzle(values)
    if values is False:
        return False
    solved = True
    for box in values:
        if len(values[box]) > 1:
            solved = False
    if solved:
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    min_length = 10
    for keys in values:
        possible = len(values[keys])
        if possible > 1 and possible < min_length:
            unsolved = keys
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for num in values[unsolved]:
        new_values = dict(values)
        new_values[unsolved] = num
        new_values = search(new_values)
        if new_values:
            return new_values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    dict_board = grid_values(grid)
    solution_board = search(dict_board)
    # display(solution_board)
    return solution_board


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
