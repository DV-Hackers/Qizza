from random import randrange

class Environment:
  def __init__(self, size, obstacles, drop_locs, pick_loc, rewards):
    self.rewards = rewards
    self.state = {
      'loc': (randrange(size), randrange(size)),
      'pizza': False
    }
    self.obstacles = obstacles # dict type [{'loc':(x, y), 'dir': char}, ...] char is: u, d, l, r. Example:  [{'loc':(1, 3), 'dir': 's'}, {'loc':(1, 3), 'dir': 'n'}]
    self.all_drop_locs = drop_locs # list of tuples of (x, y)
    self.c_drop_loc = self.all_drop_locs[randrange(len(self.all_drop_locs) - 1)] # Change later. of type (x, y)
    self.pick_loc = pick_loc # tuple (x, y)
    self.size = size # length and width of square
    self.graphic.fill(d = self.all_drop_locs, D = self.c_drop_loc, p = self.pick_loc, o = self.obstacles, s = self.state['loc'])
  
  def step(self, action): # different actions: 'drop', 'pick', 'l', 'r' ,'u', 'd'
    tempState = self.state.copy()
    reward = self.rewards['move']
    done = False
    
    if action == 'pick':
      if self.state['loc'] == self.pick_loc:
        reward = self.rewards['c_pick']
        tempState['pizza'] = True
      else:
        reward = self.rewards['i_pick']
        tempState['pizza'] = False
    
    elif action == 'drop':
      if self.state['loc'] == self.c_drop_loc:
        reward = self.rewards['c_drop']
        done = True
        tempState['pizza'] = False
      else:
        reward = self.rewards['i_drop']
        tempState['pizza'] = True
    
    else:
      hitObstacle = False
      for obstacle in self.obstacles:
        if self.coordSet(self.state['loc'], action) == self.coordSet(obstacle['loc'], obstacle['dir']):
          hitObstacle = True
          break
      if hitObstacle == False:
        tempState['loc'] = self.locWithDir(self.state['loc'], action)
    
    # print(tempState)
    self.state = tempState # is this needed?
    
    self.graphic.clear()
    self.graphic.fill(d = self.all_drop_locs, D = self.c_drop_loc, p = self.pick_loc, o = self.obstacles, s = self.state['loc'])
    return {
        'new_state': tempState,
        'reward': reward,
        'done': done
    }
    
  def coordSet(self, loc, dir):
    return {loc, self.locWithDir(loc, dir)}
    
  def locWithDir(self, loc, dir, inc = 1):
    if dir == 'u':
      return (loc[0], loc[1] - inc)
    elif dir == 'd':
      return (loc[0], loc[1] + inc)
    elif dir == 'l':
      return (loc[0] - inc, loc[1])
    elif dir == 'r':
      return (loc[0] + inc, loc[1])

  # coord example: {'n': (1,2), 'l': (3,4)}
  

      
if __name__ == "__main__":
  testEnv = Environment(
    size = 5,
    obstacles = [{'loc': (1, 3), 'dir': 'd'}, {'loc':(1, 2), 'dir': 'l'}],
    drop_locs = [(1,4),(2,3)],
    pick_loc = (0,0),
    rewards = {
      'c_drop': 10,
      'i_drop': -10,
      'c_pick': 10,
      'i_pick': -10,
      'move': -1
    })