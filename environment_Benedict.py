from random import randrange

class Environment:
  def __init__(self, size, obstacles, drop_locs, pick_loc, rewards):
    '''
    Parameter Variables
    :pram size:tuple, x and y sizes of environment (x, y)
    :param obstacles: list, dict that represent the obstacle coords [(x, y), ...]
    :param drop_locs: list, tuples that represent drop locations [(x, y), ...]
    :param pic_loc: tuple, pickup location coordinates (x, y)
    :param rewards: dict, rewards for all actions {'c_drop': 10, 'i_drop': -10, 'c_pick': 10, 'i_pick': -10, 'move': -1}
    
    Function Variables
    :self.rewards: store rewards from parameter {'c_drop': 10, 'i_drop': -10, 'c_pick': 10, 'i_pick': -10, 'move': -1}
    :self.state: dict, current state {'loc': (x, y), 'pizza': False}
    '''
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
    self.rewards_table = [[x for x in range(6)] for y in range((size ** 2) * len(drop_locs) * 2)]
  
  def step(self, action): # different actions: 'drop', 'pick', 'l', 'r' ,'u', 'd'
    '''
    :param action: str ['u','d','l', 'r', 'pick', 'drop']
    '''
    self.state = self.rewards_table[self.encode({'state': self.state, 'c_drop_loc': self.c_drop_loc})][action]['new_state']
    return self.state
    
    
  def createRewardsTable(self):
    for x in range(self.x):
      for y in range(self.y):
        for pizza in [False, True]:
          for drop_loc in self.all_drop_locs:
            for action in enumerate(['u', 'd' , 'l', 'r', 'pick', 'drop']):
              tempState = self.state.copy()
              reward = self.rewards['move']
              done = False
              
              if action[1] == 'pick':
                if self.state['loc'] == self.pick_loc:
                  reward = self.rewards['c_pick']
                  tempState['pizza'] = True
                else:
                  reward = self.rewards['i_pick']
                  tempState['pizza'] = False
              
              elif action[1] == 'drop':
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
                  if self.coordSet(self.state['loc'], action[1]) == self.coordSet(obstacle['loc'], obstacle['dir']):
                    hitObstacle = True
                    break
                if hitObstacle == False:
                  tempState['loc'] = self.locWithDir(self.state['loc'], action[1])
              
              
              self.rewards_table[self.encode({'state':{'loc': (x, y), 'pizza': pizza}, 'c_drop_loc': drop_loc})][action[0]] = {
                'new_state': tempState,
                'reward': reward, 
                'done': done
              } # assigns values to rewards tables
            
    
    
  def encode(self, info):
    '''
    Returns integer of state. Currently only works with size and total drop locations are 10 and below (I think)
    :param info: dict, state and current drop location {'state':{'loc': (x, y), 'pizza': bool}, 'c_drop_loc': (x, y)} 
    :return: int, unique identification number
    '''
    index = 0
    index += info['state']['loc'][0]
    index *= self.size
    index += info['state']['loc'][1]
    index *= 2
    index += 1 if info['state']['pizza'] else 0
    index *= len(self.all_drop_locs)
    index += self.all_drop_locs.index(info['c_drop_loc'])
    
    return index
  
  def decode(self, index):
    newInfo = {'state': {'loc': (0,0), 'pizza': False}, 'c_drop_loc': (0,0)}
    
    newInfo['c_drop_loc'] = self.all_drop_locs[index % len(self.all_drop_locs)] # setting correct drop location (x,y)
    index //= len(self.all_drop_locs) # removing number of locations and truncating to remove the correct location
    newInfo['state']['pizza'] = True if index % 2 == 1 else False
    index //= 2
    newInfo['state']['loc'][1] = index % self.size # setting current y
    index //= self.size # removing y size and truncating to leave x
    newInfo['state']['loc'][0]  # setting current x
    
    return newInfo
    
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