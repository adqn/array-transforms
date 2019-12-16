#
# Gives a class for transforming elements within an NxN array
# Handles 45 degree multiples for rotation function
# Returns "rotated" (shifted) NxN array for odd N
#
# If given grid contains '2' in any subarray it will be treated as an axis
# and left unchanged
# Shift operations operate by replacing '0' (empty) with '1' (filled)
# and vice versa (for now)
# Rotation function works with an implicit axis at the center
#
# Also, only operates within bounds of array size; will not shift elements 'outside'
# of the grid (for now)
#
# TODO:
# - Add exception handling for out of bounds operations
# - Shift all non-zero characters
# - Allow shifting out of bounds
#

import numpy


class Transformation_Grid:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid)
        self.dist_from_axis = int(numpy.floor(len(grid) / 2))
        self.axis_index = self.dist_from_axis + 1

        self.indices = []
        self.indices.extend(range(self.width))

        self.indices_reverse = self.indices.copy()
        self.indices_reverse.reverse()

        self.dist_indices = self.indices.copy()[:self.dist_from_axis]
        self.dist_reverse = self.indices_reverse.copy()[self.dist_from_axis +
                                                        1:]

    # Shift methods will shift positions by one
    # Shift single elements
    def shift_up(self, grid, subarray, position, offset):
        if grid[subarray][position] == 1:
            try:
                grid[subarray][position] = 0
                grid[subarray - offset][position] = 1
            except:
                pass
        return grid

    def shift_down(self, grid, subarray, position, offset):
        if grid[subarray][position] == 1:
            try:
                grid[subarray][position] = 0
                grid[subarray + offset][position] = 1
            except:
                pass
        return grid

    def shift_left(self, grid, subarray, position, offset):
        if grid[subarray][position] == 1:
            try:
                grid[subarray][position] = 0
                grid[subarray][position - offset] = 1
            except:
                pass
        return grid

    def shift_right(self, grid, subarray, position, offset):
        if grid[subarray][position] == 1:
            try:
                grid[subarray][position] = 0
                grid[subarray][position + offset] = 1
            except:
                pass
        return grid

    # Shift all elements
    def shift__all_up(self, grid):
        for i in range(self.width - 1):
            for j in range(self.width):
                if grid[i + 1][j] == 1:
                    grid[i + 1][j] = 0
                    grid[i][j] = 1

    def shift_all_down(self, grid):
        for i in self.indices_reverse[:self.width - 1]:
            for j in range(self.width):
                if grid[i - 1][j] == 1:
                    grid[i - 1][j] = 0
                    grid[i][j] = 1

    def shift_all_left(self, grid):
        for i in range(self.width):
            for j in range(self.width - 1):
                if grid[i][j + 1] == 1:
                    grid[i][j + 1] = 0
                    grid[i][j] = 1

    def shift_all_right(self, grid):
        for i in range(self.width):
            for j in self.indices_reverse[:self.width - 1]:
                if grid[i][j - 1] == 1:
                    grid[i][j - 1] = 0
                    grid[i][j] = 1

    # Splits input grid into 4 quadrants and returns separate image for each
    # Should handle NxN for odd N > 2
    # Give this a clockwise/counter-clockwise argument
    def shift45deg_cw(self, grid, quadrant):
        temp_grid = []
        temp_grid.extend(range(len(grid)))

        for i in temp_grid:
            temp_grid[i] = []
            for j in range(len(grid)):
                temp_grid[i].append(0)

        # Shift down by k subarrays
        if quadrant == 1:
            dist_reverse_last = self.indices_reverse.copy()[:self.
                                                            dist_from_axis]

            for i in range(self.dist_from_axis):
                j = dist_reverse_last[i]
                k = j - self.dist_from_axis

                if grid[self.dist_from_axis][j] == 1:
                    temp_grid[self.dist_from_axis][j] = 1
                    temp_grid = self.shift_down(temp_grid, self.dist_from_axis,
                                                j, k)

                if grid[self.dist_from_axis - k][j] == 1:
                    temp_grid[self.dist_from_axis - k][j] = 1
                    temp_grid = self.shift_down(temp_grid,
                                                self.dist_from_axis - k, j, k)

        # Shift right by k positions
        if quadrant == 2:
            for i in range(self.dist_from_axis):
                j = self.dist_reverse[i]
                k = abs(j - self.dist_from_axis)

                # Middle elements
                if grid[j][self.dist_from_axis] == 1:
                    temp_grid[j][self.dist_from_axis] = 1
                    temp_grid = self.shift_right(temp_grid, j,
                                                 self.dist_from_axis, k)

                # Diagonal elements
                if grid[j][self.dist_from_axis - k] == 1:
                    temp_grid[j][self.dist_from_axis - k] = 1
                    temp_grid = self.shift_right(temp_grid, j,
                                                 self.dist_from_axis - k, k)

        # Shift up by k subarrays
        if quadrant == 3:
            for i in range(self.dist_from_axis):
                j = self.dist_reverse[i]
                k = abs(j - self.dist_from_axis)

                # Middle elements
                if grid[self.dist_from_axis][j] == 1:
                    temp_grid[self.dist_from_axis][j] = 1
                    temp_grid = self.shift_up(temp_grid, self.dist_from_axis,
                                              j, k)

                # Diagonal elements
                if grid[self.dist_from_axis + k][j] == 1:
                    temp_grid[self.dist_from_axis + k][j] = 1
                    temp_grid = self.shift_up(temp_grid,
                                              self.dist_from_axis + k, j, k)

        # Shift left by k positions
        # This one's a bit cheesy
        if quadrant == 4:
            dist_reverse_last = self.indices_reverse.copy()[:self.
                                                            dist_from_axis]

            for i in range(self.dist_from_axis):
                j = dist_reverse_last[i]
                l = self.indices[self.dist_from_axis + 1:][i]
                k = l - self.dist_from_axis

                if grid[l][self.dist_from_axis] == 1:
                    temp_grid[l][self.dist_from_axis] = 1
                    temp_grid = self.shift_left(temp_grid, l,
                                                self.dist_from_axis, k)

                if grid[l][self.dist_from_axis + k] == 1:
                    temp_grid[l][self.dist_from_axis + k] = 1
                    temp_grid = self.shift_left(temp_grid, l,
                                                self.dist_from_axis + k, k)

        return temp_grid

    # Call clockwise shift on each quadrant
    # Reassemble images from each operation
    # ???
    # Profit
    def rotate_right(self):
        grid = self.grid.copy()

        temp_grid = []
        temp_grid.extend(range(len(grid)))

        for i in temp_grid:
            temp_grid[i] = []
            for j in range(len(grid)):
                temp_grid[i].append(0)

        grid1 = self.shift45deg_cw(grid, 1)
        grid2 = self.shift45deg_cw(grid, 2)
        grid3 = self.shift45deg_cw(grid, 3)
        grid4 = self.shift45deg_cw(grid, 4)

        for i in range(self.width):
            for j in range(self.width):
                current_char = 0

                if grid1[i][j] != 0:
                    current_char = grid1[i][j]

                if grid2[i][j] != 0:
                    current_char = grid2[i][j]

                if grid3[i][j] != 0:
                    current_char = grid3[i][j]

                if grid4[i][j] != 0:
                    current_char = grid4[i][j]

                temp_grid[i][j] = current_char

        # Put center element back lol
        temp_grid[self.width - 1 - self.dist_from_axis][
            self.width - 1 - self.dist_from_axis] = self.grid[
                self.width - 1 - self.dist_from_axis][self.width - 1 -
                                                      self.dist_from_axis]

        self.grid = temp_grid

    # Eventually
    def rotate_left(self):
        True
