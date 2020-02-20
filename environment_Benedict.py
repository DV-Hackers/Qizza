import randrange from random

class Environment:
  def __init__(self, size, obstacles, c_drop_loc , drop_locs, pick_loc, rewards):
    self.rewards = rewards
    self.state = {
      'loc': (randrange(size), randrange(size)),
      'pizza': False
    }
    self.obstacles = obstacles # dict type [{'loc':(x, y), 'dir': char}, ...] char is: u, d, l, r. Example:  [{'loc':(1, 3), 'dir': 's'}, {'loc':(1, 3), 'dir': 'n'}]
    self.all_drop_locs = drop_locs # list of tuples of (x, y)
    self.c_drop_loc = None # Change later. of type (x, y)
    self.pick_loc = pick_loc # tuple (x, y)
    self.size = size # length and width of square
  
  def step(self, action): # different actions: 'drop', 'pick', 'l', 'r' ,'u', 'd'
    tempState = self.state.copy()
    reward = -1
    done = False
    
    if action == 'pick':
      if self.state['loc'] == self.pick_loc:
        reward = 10
        tempState['pizza'] = True
      else:
        reward = -10
        tempState['pizza'] = False
    
    elif action == 'drop':
      if self.state['loc'] == self.c_drop_loc:
        reward = 10
        tempState['pizza'] = False
      else:
        reward = 10
        tempState['pizza'] = True
    
    else:
      hitObstacle = False
      for obstacle in self.obstacles:
        if coordSet(self.state['loc'], action) == coordSet(obstacle['loc'], obstacle['dir'])
          hitObstacle = True
          break
      if hitObstacle == False
        tempState = coordNext(self.state['loc'], action)
  
    return {
        'new_state': tempState,
        'reward': reward,
        'done': False
    }
    
    def coordSet(self, loc, dir):
      return {loc, coordNext(loc, dir)}
      
    def coordNext(loc, dir):
      if dir == 'n':
        return = (loc[0] + 1, loc[1])
      elif dir == 's':
        return = (loc[0] - 1, loc[1])
      elif dir == 'l':
        return = (loc[0], loc[1] - 1)
      elif dir == 'r':
        return = (loc[0], loc[1] + 1)

  
