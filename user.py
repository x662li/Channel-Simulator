import numpy as np

class User():
    
    def __init__(self, cell_id):
        self.cell_id = cell_id # id of the residing cell (row + col)
        self.freq = None # frequency assigned to user
    
    def get_cellid(self):
        return self.cell_id
    
    def get_freq(self):
        return self.freq
    
    def set_cellid(self, cell_id):
        self.cell_id = cell_id
        
    def assign_freq(self, freq):
        self.freq = freq
        