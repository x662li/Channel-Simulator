import numpy as np

class Cell():
    def __init__(self, row, col, cell_id):
        self.cell_id = cell_id # cell id (row + col)
        self.coord = (row, col) # coordinate
        self.neighbours = [] # neighbouring cell ids
        self.add_neighbours(row, col)
        self.available_freqs = [] # for static
        self.users = [] # list of users in cell
    
    def get_coord(self):
        return self.coord
    
    def get_neighbours(self):
        return self.neighbours
    
    def set_freqs(self, freqs):
        self.available_freqs = freqs
        
    def add_user_static(self, user): # add user in static case
        if self.available_freqs:
            user.set_cellid(self.cell_id)
            user.assign_freq(self.available_freqs.pop(0))
            self.users.append(user)
            return True
        else:
            return False
    
    def add_user_dynamic(self, user): # add user dynamic case (no assign freq)
        user.set_cellid(self.cell_id) 
        self.users.append(user)
        return True
    
    def remove_user(self, user): # remove user from cell
        self.users.remove(user)
        self.available_freqs.append(user.get_freq())
    
    # def calc_coord(self, x, y):
    #     return ((np.sqrt(3)*x)+((np.sqrt(3)/2)*y), (3/2)*y)
    
    def add_neighbours(self, row, col): # identify neighbours for the cell
        all_adjs = [(row, col+1), (row, col-1), (row+1, col), (row-1, col), (row+1, col-1), (row-1, col+1)]
        for item in all_adjs:
            if (item[0] >= 0) & (item[0] <= 7) & (item[1] >= 0) & (item[1] <= 7):
                self.neighbours.append(str(item[0])+str(item[1]))
            