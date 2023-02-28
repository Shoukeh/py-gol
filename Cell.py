# in_data: input data to be checked, matrix: active matrix out of which data is extracted
# Check and correct row coordinates (Out of bound corrections)
# Note that to check last index overflows len(var)-1 is used for both the row and column function
def check_row_bound(in_data, matrix):
    in_data = len(matrix) - 1 if in_data < 0 else in_data  # If row index is negative, make it the last row index
    in_data = 0 if in_data > len(matrix) - 1 else in_data  # If row index is larger than the end index, set it to 0
    return in_data


# Check and correct column coordinates (Out of bound corrections)
def check_col_bound(in_data, matrix):
    in_data = len(matrix[0]) - 1 if in_data < 0 else in_data  # If col index is negative, make it the last col index
    in_data = 0 if in_data > len(matrix[0]) - 1 else in_data  # If col index is larger than the end index, set it to 0
    return in_data


# Class for all cells. A matrix is made of up instances of this class
class Cell:
    # Init with row and column coordinate as well as the cells state
    def __init__(self, row, col, state):
        self.row = int(row)
        self.col = int(col)
        self.state = state

    # method for checking the neighbours around the cell
    # old_matrix: input of the "old" matrix that is used as a lookup to perform the next generation of the simulation
    # Returns an integer which indicates how many alive neighbours the cell has
    def check_neighbours(self, old_matrix):
        alive_neighbours = 0  # Keeps count of how many alive neighbours the input cell has
        for row_offset in range(self.row - 1, self.row + 2):  # Loop that runs for every row (above, own, below)
            row_offset = check_row_bound(row_offset, old_matrix)  # Range check

            for col_offset in range(self.col - 1, self.col + 2):  # Loop that checks each cell in row (left, mid, right)
                col_offset = check_col_bound(col_offset, old_matrix)  # Range check

                if old_matrix[row_offset][col_offset].state:  # if the neighbour that is currently being looked
                    alive_neighbours += 1  # at is alive, add 1 to the counter "alive_neighbours"

                    if self.col == col_offset and self.row == row_offset:  # If the method is checking itself,
                        alive_neighbours -= 1  # remove one from counter  (not a neighbour)

        return alive_neighbours

    # Prints out a "-" or "o" depending on the state
    def __str__(self):
        if self.state:  # ALIVE
            return "o"
        else:           # DEAD
            return "-"