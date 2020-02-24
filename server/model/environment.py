import random
from util.table import Table

"""
IMPLEMENTATION NOTES:

- I did end up using the Matrix classes that you made to store the reward table, I call it Table instead of Matrix tho.
This is because I store dicts at each index not numbers and Matrices are only for storing numbers.

- I realized last night that creating a table storing all possible action results (reward_table) is better than computing
the result of an action on the fly because we will potentially have to compute the same action thousands of times. So
this implementation reflects that.

- rewards parameter structure:
  {
    'pickup': {'pos': positive_reward, 'neg': negative_reward}},
    'dropoff': {'pos': pos_reward, 'neg': neg_reward}},
    'time': time_reward
  }

- obstacles parameters structure:
  {
    (x, y): 0 | 1 | 2,
    ...
  }
  + for simplicity obstacles can only be on top, right, or both top & right sides of a coordinate.
  + This is done so that multiple coordinates can't map to the same obstacle.
  + 0 means obstacle on top of coord, 1 means on right, 2 means both.

- homes parameter structure: [(x, y), (x, y), ...]

- store parameter structure: (x, y)

- For simplicity is that a goal can only be one of the homes, not the store.The agent will learn to go to the store 
before dropping off by telling it that it doesn't have a pizza.
"""


class Environment:
  action_space = 6  # number of possible actions
  action_enum = ['up', 'right', 'down', 'left', 'pickup', 'dropoff']  # mapping of actions number to what it means to us
  pizza_space = 2  # number of places pizza can be

  def __init__(self, size, homes, store, obstacles, rewards):
    """
    Creates an environment.
    :param size: int, number of rows/cols in env
    :param homes: list, list of all drop off locations in form (x, y)
    :param store: tuple, pickup location (x, y)
    :param obstacles: dict, dict of all obstacles in form (x, y): side, side can only be 0(top) or 1(right) or 2(both)
    :param rewards: dict, dict of all rewards. {'pickup': {'pos': int, 'neg': int},'drop': {'pos': int, 'neg': int},
    'time': int}
    """
    self.size = size
    self.homes = homes
    self.store = store
    self.obstacles = obstacles
    self.rewards = rewards
    self.curr_state = 0
    self.goal = 0

    state_space = self.size ** 2 * self.pizza_space * len(self.homes)
    self.reward_table = Table(state_space, self.action_space)

    self.reset()
    self.init_table()

  def reset(self):
    """
    pick new random goal and create new random state.
    :return: int, new state
    """
    self.goal = random.randint(0, len(self.homes) - 1)

    curr_location = (random.randint(0, self.size-1), random.randint(0, self.size-1))
    bad_starts = self.homes + [self.store]

    while curr_location in bad_starts:
      curr_location = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

    self.curr_state = self.encode(*curr_location, 0, self.goal)
    return self.curr_state

  def init_table(self):
    """
    initializes rewards table.
    :return: None
    """
    for x in range(self.size):
      for y in range(self.size):
        for pizza in range(self.pizza_space):
          for dest_idx in range(len(self.homes)):
            state = self.encode(x, y, pizza, dest_idx)
            for action in range(self.action_space):
              # defaults for every state
              new_x, new_y, new_pizza = x, y, pizza
              reward = self.rewards['time']
              done = False

              obstacle_loc = self.obstacles.get((x, y), -1)
              left_coord_obstacle = self.obstacles.get((x - 1, y), -1)
              down_coord_obstacle = self.obstacles.get((x, y - 1), -1)

              # going up or right
              if 1 >= action != obstacle_loc and obstacle_loc != 2:
                if action == 0:
                  new_y = min(self.size - 1, y + 1)
                else:
                  new_x = min(self.size - 1, x + 1)

              # down
              elif action == 2 and down_coord_obstacle != 2 and down_coord_obstacle != 0:
                new_y = max(0, y - 1)

              # left
              elif action == 3 and left_coord_obstacle != 2 and left_coord_obstacle != 1:
                new_x = max(0, x - 1)

              # pickup
              elif action == 4:
                if (x, y) == self.store and not pizza:  # if at store and don't have a pizza
                  new_pizza = 1
                  reward = self.rewards['pickup']['pos']
                else:
                  reward = self.rewards['pickup']['neg']

              # dropoff
              elif action == 5:
                if (x, y) == self.homes[dest_idx] and pizza: # if at dest and have pizza
                  new_pizza = 0
                  done = True
                  reward = self.rewards['drop']['pos']
                else:
                  reward = self.rewards['drop']['neg']

              new_state = self.encode(new_x, new_y, new_pizza, dest_idx)
              # print('old state:', self.decode(state), '  action', self.action_enum[action], '  new state', self.decode(new_state), '  reward', reward)
              self.reward_table.set(state, action, {
                'result': new_state,
                'reward': reward,
                'done': done
              })

  def step(self, action):
    """
    perform one time step in environment with one action.
    :param action: int, action agent takes
    :return: dict, result of action {new state, reward, done}
    """
    res = self.reward_table.get(self.curr_state, action)

    self.curr_state = res['result']

    return res

  def encode(self, x, y, pizza_loc, dest_idx):
    """
    Encodes a state to a unique integer.
    :param x: int, x-coord
    :param y: int, y-coord
    :param pizza_loc: int, [0, 1] whther pizza is at store or in car
    :param dest_idx: int, index of the destination
    :return: int, unique integer state.
    """
    i = x
    i *= self.size
    i += y
    i *= self.pizza_space
    i += pizza_loc
    i *= len(self.homes)
    i += dest_idx

    return i

  def decode(self, i):
    """
    decodes unique integer state to dictionary state.
    :param i: int, state
    :return: dict, {x, y, pizza, dest}
    """
    out = {}
    out['dest'] = i % len(self.homes)
    i //= len(self.homes)
    out['pizza'] = i % self.pizza_space
    i //= self.pizza_space
    out['y'] = i % self.size
    i //= self.size
    out['x'] = i

    return out


#### TEST DRIVER ####

obstacles = {
  (0, 0): 1,
  (0, 1): 2
}

rewards = {
  'pickup': {'pos': 10, 'neg': -10},
  'drop': {'pos': 10, 'neg': -10},
  'time': -1
}

homes = [
  (0, 1),
  (3, 2),
  (4, 3)
]

store = (2, 2)

env = Environment(5, homes, store, obstacles, rewards)

# epochs = penalties = rewards = 0
#
# done = False
#
# print(len(env.reward_table.arr[0]))
# while not done:
#   action = random.randint(0, 5)
#   # print('action:', action)
#   res = env.step(action)
#   # print('result:', res)
#
#   if res['reward'] == -10:
#     penalties += 1
#
#   epochs += 1
#
# print("Time steps taken: {}".format(epochs))
# print("Penalties incurred: {}".format(penalties))
