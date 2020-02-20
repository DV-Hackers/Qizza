import randrange from random

class Environment:
    def __init__(self, size, obstacles, c_drop_loc , drop_locs, pick_loc, rewards):
        self.rewards = rewards
        self.state = {
            'x': randrange(size),
            'y': randrange(size),
            'pizza': False
        }
        self.obstacles = obstacles
        self.all_drop_locs = drop_locs
        self.c_drop_loc  
        self.pick_loc = pick_loc
        self.size = size
    
    def step(self, action): # different actions: 'drop', 'pick', 'l', 'r' ,'u', 'd'
        tempState = self.state.copy()
        
        if (action == 'pick'):
            if (self.state['x'] == self.pick_loc[0]) and (self.state['y'] == self.pick_loc[1]):
                tempState['pizza'] = True
            else:
                tempState['pizza'] = False
            
        return {
            'new_state': ,
            'reward': ,
            'done': 
        }