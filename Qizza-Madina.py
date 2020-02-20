import random

class Qizza:
    def __init__ (self, size, obstacles, dropoff_locs, rewards, pick_up_loc):

        #........

        self.rows = size
        self.cols = size
        self.obstacles = obstacles
        self.dropoff_locs = dropoff_locs
        self.rewards = {'c_drop': +10, 'i_drop': -10, 'c_pick': +1, 'i_pick': 10}
        self.pick_up_loc = pick_up_loc

        state = {'x': random.randint(0,4), 'y':random.randint(0, 4) , 'pizza': False}

    def step(self, action):

        if action == self.pick_up_loc:
            if state
            #check
            #then you return a reward for the bad
