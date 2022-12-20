import random
import numpy as np
import map
import cell
import user

class Utils():
    def __init__(self, map_created):
        self.map = map_created # map created
        self.tot_ops = 0 # operation counter
        self.num_blocked = 0 # blocked counter
        self.num_dropped = 0 # dropped counter
        self.tot_users = [] # existing users
        self.freq_reuses = { # frequency usage counter
            freq : 0 for freq in range(90)
        }
        self.freq_assigns = { # freqency assignment for dynamic case
            freq: set() for freq in range(90)
        }
        
    def generate_user_static(self):
        self.tot_ops += 1
        cellid_picked = random.sample(self.map.get_cellids(), 1)[0] # pick a cell
        cell_picked = self.map.get_cell(cellid_picked)
        new_user = user.User(cellid_picked) # create user
        if not cell_picked.add_user_static(new_user): # check for block
            self.num_blocked += 1
            # print("user in cell " + str(cellid_picked) + " is blocked")
        else:
            self.tot_users.append(new_user) # not blocked, add to cell
            self.freq_reuses[new_user.get_freq()] += 1
            
    def hand_over_satic(self):
        if self.tot_users: # check existing user
            self.tot_ops += 1
            user_picked = random.sample(self.tot_users, 1)[0] # pick a user
            from_cellid = user_picked.get_cellid()
            to_cellid = random.sample(self.map.get_cell(from_cellid).get_neighbours(), 1)[0] # pick a neighbouring cell
            to_cell = self.map.get_cell(to_cellid)
            if not to_cell.add_user_static(user_picked): # check for drop 
                self.num_dropped += 1
                # print("user in cell " + str(from_cellid) + " is dropped")
            else:
                self.map.get_cell(from_cellid).remove_user(user_picked) # not dropped, move to new cell
                # print("user in cell " + str(from_cellid) + " moved to cell " + str(to_cellid))
    
    def remove_user_static(self):
        if self.tot_users:
            user_picked = self.tot_users.pop(random.randint(0, len(self.tot_users)-1)) # pick a user
            user_cell = self.map.get_cell(user_picked.get_cellid()) 
            user_cell.remove_user(user_picked) # remove from cell
    
    def check_dist(self, coord_1, coord_2): # check distance for dynamic case
        dist = np.sqrt((coord_1[0] - coord_2[0])**2 + (coord_1[1] - coord_2[1])**2)
        return dist >= 3
    
    def generate_user_dynamic(self):
        self.tot_ops += 1
        cellid_picked = random.sample(self.map.get_cellids(), 1)[0]
        cell_picked = self.map.get_cell(cellid_picked)
        new_user = user.User(cellid_picked)
        chan_picked = random.randint(0, 89) # pick a channel
        for other_coord in self.freq_assigns[chan_picked]: # check for blocking
            if not self.check_dist(cell_picked.get_coord(), other_coord):
                self.num_blocked += 1
                # print("user in cell " + str(cellid_picked) + " is blocked")
                return
        new_user.assign_freq(chan_picked) # not blocked, add user to cell
        cell_picked.add_user_dynamic(new_user)
        self.tot_users.append(new_user)
        self.freq_assigns[chan_picked].add(cell_picked.get_coord())
        self.freq_reuses[new_user.get_freq()] += 1
        
    def hand_over_dynamic(self):
        if self.tot_users:
            self.tot_ops += 1
            user_picked = random.sample(self.tot_users, 1)[0]
            from_cellid = user_picked.get_cellid()
            from_cell = self.map.get_cell(from_cellid)
            to_cellid = random.sample(self.map.get_cell(from_cellid).get_neighbours(), 1)[0]
            to_cell = self.map.get_cell(to_cellid)
            
            self.freq_assigns[user_picked.get_freq()].remove(from_cell.get_coord())
            chan_picked = random.randint(0, 89) # pick a channel
            
            for other_coord in self.freq_assigns[chan_picked]: # check for dropping 
                if not self.check_dist(to_cell.get_coord(), other_coord):
                    self.num_dropped += 1
                    self.freq_assigns[user_picked.get_freq()].add(from_cell.get_coord())
                    # print("user in cell " + str(from_cellid) + " is dropped")
                    return
            to_cell.add_user_dynamic(user_picked) # not dropped, add to user
            user_picked.assign_freq(chan_picked)
            self.map.get_cell(from_cellid).remove_user(user_picked)
            self.freq_assigns[chan_picked].add(to_cell.get_coord())
            # print("user in cell " + str(from_cellid) + " moved to cell " + str(to_cellid))
            
    def remove_user_dynamic(self):
        if self.tot_users:
            user_picked = self.tot_users.pop(random.randint(0, len(self.tot_users)-1))
            user_cell = self.map.get_cell(user_picked.get_cellid())
            user_cell.remove_user(user_picked) # remove user
            self.freq_assigns[user_picked.get_freq()].remove(user_cell.get_coord()) # update freq assignment
    
    def calc_metrics(self): # calculate metrics
        drop_rate = self.num_dropped / self.tot_ops 
        block_rate = self.num_blocked / self.tot_ops
        freq_reuse_rate = sum(self.freq_reuses.values()) / self.tot_ops
        # print("==========")
        # print("blocking rate: " + str(block_rate))
        # print("dropping rate: " + str(drop_rate))
        # print("frequency reuse rate: " + str(freq_reuse_rate))
        # print("==========")
        return [block_rate, drop_rate, freq_reuse_rate]
            
            
            
    

            