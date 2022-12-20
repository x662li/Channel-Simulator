import numpy as np
import cell

class Map():
    def __init__(self, size, min_dist):
        self.cells = {} # cell dict {id (row + col): cell}
        self.size = size # map size (8x8)
        self.min_dist = min_dist # min reuse dist
        
    def get_cellids(self):
        return list(self.cells.keys())
    
    def get_cell(self, id):
        return self.cells[id]
    
    def create_map_static(self): # create map and assign frequencies
        num_chan = 90 // (self.min_dist ** 2) # number of channels for each cell
        for row in range(self.size):
            for col in range(self.size):
                cell_id = str(row)+str(col)
                new_cell = cell.Cell(row, col, cell_id)
                freq_ind = (row % self.min_dist) * self.min_dist + (col % self.min_dist)
                new_cell.set_freqs([freq_ind * num_chan + x for x in range(num_chan)]) # assign freq to cells
                self.cells[cell_id] = new_cell
    
    def create_map_dynamic(self): # create map without assign frequencies
        for row in range(self.size):
            for col in range(self.size):
                cell_id = str(row)+str(col)
                new_cell = cell.Cell(row, col, cell_id)
                self.cells[cell_id] = new_cell