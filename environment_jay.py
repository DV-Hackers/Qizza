import random
from server.util import table
class Environment:
  num_of_pizza_place = 2
  num_of_possible_action = 6

  def __init__(self, size, obstacles, home,rewards,store):
    self.size = size
    self.obstacles = obstacles
    self.home = home
    self.rewards = rewards
    self.store = store
    self.current_state = 0
    self.goal = 0

    action_space = size ** 2 * self.num_of_pizza_place * self.num_of_possible_action






