import random

"""
IMPLEMENTATION NOTES

rewards list indices -
0: go up
1: go right
2: go down
3: go left
4: pickup
5: dropoff
6: time

I realized last night that creating a table storing all possible action results (reward_table) is better than computing
the result of an action on the fly because we will potentially have to compute the same action thousandss of times. So
this class reflects that.

for simplicity obstacles can only be on top, right, or both top & right sides of a coordinate.
This is done so that multiple coordinates can't map to the same obstacle.

Another thing for simplicity is that a goal can only be one of the homes, not the store.
The agent will learn to go to the store before dropping off by telling it that it doesn't have a pizza.
"""


class Table:
  def __init__(self, rows, cols):
    self.arr = [[0 for _ in range(cols)] for _ in range(rows)]

  def set(self, x, y, val):
    self.arr[x][y] = val


class Environment:
  def __init__(self, size, homes, store, obstacles, rewards):
    """
    Creates an environment.
    :param size: int, number of rows/cols in env
    :param homes: list, list of all dropoff locations in form (x, y)
    :param store: tuple, pickup location (x, y)
    :param obstacles: dict, dict of all obstacles in form (x, y): side, sides can only be 0 (top) or 1 (right) or 2 (both)
    :param rewards: list, every type of actions rewards, each item is an int or tuple corresponding to
    (+ action, - action).
    """
    self.size = size
    self.homes = homes
    self.store = store
    self.obstacles = obstacles
    self.rewards = rewards

    self.reset()
    self.init_table()

  def reset(self):
    self.goal = random.randint(0, len(self.homes) - 1)
    # TODO: set random starting state

  def init_table(self):
    """
    initializes rewards table
    :return: None
    """
    state_space = self.size ** 2 * len(self.homes) * 2
    self.reward_table = Table(state_space, len(self.rewards))
    for x in range(self.size):
      for y in range(self.size):
        for p in range(2):
          for d in range(len(self.homes)):
            state = self.encode(x, y, p, d)
            for action in range(len(self.rewards[:-1])):
              # defaults for every state
              new_x, new_y, new_pizza = x, y, p
              reward = self.rewards[-1]
              done = False

              obstacle_loc = self.obstacles.get((x, y), -1)
              left_coord_obstacle = self.obstacles.get((x - 1, y), -1)
              down_coord_obstacle = self.obstacles.get((x, y - 1), -1)

              if 1 >= action != obstacle_loc and obstacle_loc != 2:
                if action == 0:
                  new_y = max(0, y - 1)
                else:
                  new_x = min(self.size - 1, x + 1)

              elif action == 2 and left_coord_obstacle != 2 and left_coord_obstacle != 1:
                new_x = max(0, x - 1)

              elif action == 3 and down_coord_obstacle != 2 and down_coord_obstacle != 0:
                new_y = max(0, y - 1)

              elif action == 4:  # pickup
                if (x, y) == self.store and not p:  # if at store and don't have a pizza
                  new_pizza = 1
                  reward = self.rewards[4][0]
                else:
                  reward = self.rewards[4][1]

              elif action == 5:  # dropoff
                if (x, y) == self.homes[d] and p:
                  new_pizza = 0
                  done = True
                  reward = self.rewards[5][0]
                else:
                  reward = self.rewards[5][1]

              new_state = self.encode(new_x, new_y, new_pizza, d)
              self.reward_table.set(state, action, {
                'result': new_state,
                'reward': reward,
                'done': done
              })

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
    i *= 2
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
    out = {'x', 'y', 'pizza', 'dest'}
    out['dest'] = i % len(self.homes)
    i //= len(self.homes)
    out['pizza'] = i % 2
    i //= 2
    out['y'] = i % self.size
    i //= self.size
    out['x'] = i % self.size

    return out

  def step(self, action):
    """
    perform one time step action.
    :param action: int, action taken by agent
    :return: dict, {new state, reward, done}
    """
    # TODO: Complete this method
    pass

# test driver

obstacles = {
  (0, 0): 1,
  (0, 1): 2
}
env = Environment(5, [(0, 0), (1, 1)], (0, 0), obstacles, [0, 1, 1, 1, 1])

for x in range(5):
  for y in range(5):
    for p in range(2):
      for d in range(2):
        print(env.encode(x, y, p, d))

print(env.reward_table.arr)