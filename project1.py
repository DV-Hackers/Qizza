class Environment:
  def __init__(self, size, obstacles, dropoff_loc, pickup_loc, rewards):
    self.board_size = [size][size]
    self.obstacles = [
      (random.randrange(0, 4, 1), random.randrange(0, 4, 1), char),
      (x, y, board_size),
      #.......etc.
    ]
    self.dropoff_loc = [
      (random.randrange(0, 4, 1), random.randrange(0, 4, 1)),
      (random.randrange(0, 4, 1), random.randrange(0, 4, 1)),
      #.......etc.
    ]
    self.pickup_loc = [
      (random.randrange(0, 4, 1), random.randrange(0, 4, 1)),
      (random.randrange(0, 4, 1), random.randrange(0, 4, 1)),
      #.......etc.
    ]
    self.rewards = {
      'c_drop' : 10,
      'i_drop' : -10,
      'c_pick' : 10,
      'i_pick' : -10,
      'time' : -10
    }

  def step(action):
    return {
      'new_state':(x, y),
      'reward':int,
      'done':bool
    }
