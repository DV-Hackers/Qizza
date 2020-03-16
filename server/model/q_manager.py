from random import random, randrange
from server.model.agent import Agent
from server.model.environment import Environment


class QManager:
  def __init__(self, explore_rate, learn_rate, discount_factor, size, homes, store, obstacles, rewards):
    self.explore_rate = explore_rate

    self.env = Environment(size, homes, store, obstacles, rewards)

    num_states = self.env.state_space
    num_actions = self.env.action_space
    self.agent = Agent(learn_rate, discount_factor, num_states, num_actions)

  def step(self):
    init_state = self.env.curr_state

    # action = -1
    if random() <= self.explore_rate:
      action = randrange(0, 6)
    else:
      action = self.agent.get_best_action(init_state)

    action_result = self.env.step(action)

    reward = action_result['reward']
    max_future_reward = self.env.get_max_reward()

    self.agent.update(init_state, action, reward, max_future_reward)

    done = False
    if action_result['done']:
      return True

    return {'done': done, 'reward': reward}

  def episode(self):
    done = False
    steps = 0
    penalties = 0

    while not done:
      step_result = self.step()
      done = step_result['done']
      if step_result['reward'] == -10:
        penalties += 1
      steps += 1

    return {'steps': steps, 'penalties': penalties}

  def train(self, num_eps):
    # perform multiple episodes of training up to a desired fitness (currently a number of episodes)
    ep_count = 0
    for i in range(num_eps):
      episode_result = self.episode()
      print('episode ', ep_count, ':')
      print('total steps: ', episode_result['steps'])
      print('penalties: ', episode_result['penalties'], '\n')
      ep_count += 1

      self.explore_rate -= 0.01
      self.agent.learn_rate -= 0.01
      # self.agent.discount_factor -= 0.01


#### TEST DRIVER ####

size = 5

homes = [
  (0, 1),
  (3, 2),
  (4, 3)
]

store = (2, 2)

obstacles = {
  (0, 0): 1,
  (0, 1): 2
}

rewards = {
  'pickup': {'pos': 10, 'neg': -10},
  'drop': {'pos': 10, 'neg': -10},
  'time': -1
}

explore_rate = 1
learn_rate = 0.1
discount_factor = 0.6

qm = QManager(explore_rate, learn_rate, discount_factor, size, homes, store, obstacles, rewards)