import random

class Environment ():

  def __init__(self):
    self.size = 5
    self.obstacles = [(0,0,'R'),(0,1,'L')]
    self.dropoff_locs = [(random.randint(0,5),(random.randint(0,5))),((random.randint(0,5),(random.randint(0,5))))]
    self.rewards = {'c_del': 10,'i_del': -10, 'c_pick': 10, 'i_pick':-10, 'time': -1}
    self.pickup_loc = (random.randint(0, 5), (random.randint(0, 5)))

    state = {'x': random.randint(self.size), 'y': random.randint(self.size), 'pizza': None }

  def step(self,action):

    pass



