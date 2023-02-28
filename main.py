# Conways Game Of Life
# Grade Goal: B
# @author: Juris Homickis
# 0210309134, COPEN, KTH

import copy
from Cell import Cell, check_row_bound, check_col_bound


# Type and range checks inputs. Only a lower bound "lb" is used as an upper bound is not needed in this program
# in_data: input to be checked, lb: lower bound
# Returns the input data with corrections, if any
def check_input_int(in_data, lb):
    # Endless loop that breaks when type and range checks have passed
    while True:
        try:
            in_data = int(in_data)  # Check if the input is an integer, if not, skip to ValueError exception
            if in_data < lb:  # Check if its within range if integer check passes. Fix it otherwise.
                in_data = int(
                    input("Range error! Please enter a valid integer larger than or equal to " + str(lb) + ": "))
            else:
                break  # Type and range check pass, break loop
        except ValueError:  # If the input is not an int let the user correct it
            in_data = input("Type error! Please enter a valid integer larger than or equal to " + str(lb) + ": ")
    return in_data


# Create a matrix based on user input, populate it with "dead" (.state = False) instances of the Cell class
# Returns the matrix
def create_matrix(row, col):
    matrix = []
    i = 0
    while i < row:
        temp_row = []  # Temporary row var that gets filled with each iteration, then cleared upon new iteration start
        j = 0
        while j < col:
            cell = Cell(i, j, False)
            temp_row.append(cell)  # Populates the matrix with a dead field, i.e. all "-"
            j += 1
        matrix.append(temp_row)  # Adds the "temporary" row to the matrix
        i += 1
    return matrix


# Populates the matrix with cells from provided .txt. Each row with coordinates represents a live cell, coord format
# being ROW, COL. Negative values have a separate check due to the simulation correcting negative coordinates later.
# Returns the matrix
def populate_matrix(matrix, filename):
    file = open(filename, 'r')  # Open the file where the properties are stored
    for item in file:  # iterate for each row in the text file
        item = item.strip()  # Formatting
        list_item = item.split(",")  # Split the string using the comma as a marker "where to cut it"

        # Aforementioned negative value check
        if int(list_item[0]) < 0 or int(list_item[1]) < 0:
            print("Skipping cell at", str(list_item), "- Negative value!")
            continue

        matrix[int(list_item[0])][int(list_item[1])].state = True  # Set cell at given coords as alive

    return matrix


# Creates the initial list with alive cells and their neighbours, only gets called at the start
# Returns a list with instances
def create_check_list(matrix):
    cells_to_check = []
    rows, columns = len(matrix) - 1, len(matrix[0]) - 1  # -1 due to index starting from 0, and len starting from 1

    for row in range(rows):
        for col in range(columns):
            if matrix[row][col].state:
                # Adds cells from own, above and below rows.
                for row_offset in range(row - 1, row + 2):  # y
                    for col_offset in range(col - 1, col + 2):  # x
                        if matrix[row_offset][col_offset] not in cells_to_check:  # Check if cell is already present
                            cells_to_check.append(matrix[row_offset][col_offset])

    return cells_to_check


# Updates the list of cells to check by adding the provided cell plus its neighbours
def update_list(cell_list, row, col, matrix):
    for row in range(row - 1, row + 2):
        row = check_row_bound(row, matrix)  # Check for out of bounds value, correct if needed
        for col in range(col - 1, col + 2):
            col = check_col_bound(col, matrix)  # Check for out of bounds value, correct if needed
            if matrix[row][col] not in cell_list:  # If the cell is not already in the list, add it, skip otherwise
                cell_list.append(matrix[row][col])


# Generation logic and calls are contained here, is called from main to initiate the simulation
# gen: amount of generations, step: which generation is to be displayed to the user
def generation(matrix, cell_list, gen, step):
    draw_counter = 0  # Counter that ticks as to how many times a matrix has been updated
    i = 0
    while i < gen:
        draw_counter += 1
        # A copy is needed for proper simulation to happen. old_ variables store the previous state that is compared
        # and used to update the matrix/list. It is kind of a lookup table that you use to change your active table
        old_matrix = copy.deepcopy(matrix)  # Deep copies of the matrix and cell list. A deep copy is needed so
        old_list = copy.deepcopy(cell_list)  # that the lists within the list (matrix) get duplicated as well
        cell_list = []  # Reset main list

        # Use the check_neighbours method for each Cell class instance to update it. Add the new cells to a new list
        # thereafter.
        for cell in old_list:
            alive_neighbours = cell.check_neighbours(old_matrix)    # Check amount of alive neighbours, store it
            if cell.state:  # If the cell is alive, see if it should stay alive
                if alive_neighbours < 2:
                    matrix[cell.row][cell.col].state = False
                elif alive_neighbours > 3:
                    matrix[cell.row][cell.col].state = False
                else:   # If the cell stays alive, update the list
                    update_list(cell_list, cell.row, cell.col, matrix)
            else:   # If the cell was dead, see if it can be revived
                if alive_neighbours == 3:
                    matrix[cell.row][cell.col].state = True
                    update_list(cell_list, cell.row, cell.col, matrix)  # Update the list with it and its neighbours

        i += 1
        if draw_counter == step:  # If the current generation matches with the user input interval, display matrix
            print("Current Generation:")
            draw_ASCII(matrix)
            if i != gen:  # If it isn't the last generation, give the user the option to terminate,
                advance = input("Press ENTER to advance " + str(step) + " generations, e to terminate ")
                if advance == "e":
                    exit()
            draw_counter = 0
        elif i == gen:
            print("Gen step exceeds gen count, showing last generation instead:")
            draw_ASCII(matrix)


# Draws a given matrix via command line
def draw_ASCII(input_matrix):
    for row in input_matrix:
        print(*row)
    print()


# Calculate minimum input range. Range is determined as the longest dimension (w or h). Meaning
# if the imported pattern is 10x7, 10 is the minimum range, thus the grid will be at least 10x10
def calc_min_range():
    min_range = 0
    file = open("cells.txt", "r")

    for item in file:
        # print(item)
        split_item = item.split(",")
        for value in split_item:  # Goes through every line in the text file, if the value is bigger then the one set,
            min_range = int(value) if int(value) > min_range else min_range  # the bigger value is stored instead
    return min_range+1  # returns the minimum range as an int


# Main function. The menu is contained here
def main():
    # First section sets up the matrix variable inputs with type and range checks
    min_range = calc_min_range()
    row = input("Enter matrix height (row count): ")  # User enters row count
    row = check_input_int(row, min_range)  # The input is type and range checked
    col = input("Enter matrix width (column count): ")  # Ditto
    col = check_input_int(col, min_range)

    # Second section creates a matrix using the users input, populates it according to a text file, and creates a list
    # that will contain the coordinates of all cells of interest (cells that are alive plus their neighbours. This
    # speeds up the process somewhat because only the active area is checked instead of the entire matrix.)
    active_matrix = create_matrix(row, col)
    populate_matrix(active_matrix, "cells.txt")
    check_cell_list = create_check_list(active_matrix)
    print("Here's your matrix: ")  # Populated matrix is shown to the user
    draw_ASCII(active_matrix)

    # Third section handles user inputs for the generation logic, which is type and range (positive int only) checked
    gen_count = input("Enter amount of generations: ")
    gen_count = check_input_int(gen_count, 1)
    gen_step = input("Enter step length (every n:th generation will be displayed)\nNOTE: values larger than the "
                     "amount of generations will print the last generation directly: ")
    gen_step = check_input_int(gen_step, 1)

    # Lastly, the generation/simulation/game is activated. All the simulation logic is contained within the
    # generation() function
    generation(active_matrix, check_cell_list, gen_count, gen_step)

    print("--END SEQUENCE--")


# Call the main function and start the program
main()
