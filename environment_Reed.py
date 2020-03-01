from random import randrange


class Environment:
    actions = ['left', 'right', 'up', 'down', 'pickup', 'dropoff']

    def __init__(self, size, rewards, obstacles, homes, store):
        self.size = size
        self.rewards = rewards
        self.obstacles = obstacles
        self.homes = homes
        self.store = store

        self.goal = homes[randrange(len(self.homes))]

        start_loc = (randrange(size), randrange(size))
        bad_starts = homes + [store]
        while start_loc in bad_starts:
            start_loc = (randrange(size), randrange(size))

        self.state = {
            'x': start_loc[0],
            'y': start_loc[1],
            'pizza': False
        }

    def step(self, action):
        # default return values, possibly changed in body
        reward = rewards['time']
        done = False

        cur_x, cur_y, has_pizza = self.state['x'], self.state['y'], self.state['pizza']

        if action in ['left', 'right', 'up', 'down']:
            if not self.is_collision(action):
                if action == 'left' and cur_x - 1 >= 0:
                    self.state['x'] = cur_x - 1
                elif action == 'right' and cur_x + 1 < self.size:
                    self.state['x'] = cur_x + 1
                elif action == 'up' and cur_y - 1 >= 0:
                    self.state['y'] = cur_y - 1
                elif action == 'down' and cur_y + 1 < self.size:
                    self.state['y'] = cur_y + 1
        elif action == 'pickup':
            if (cur_x, cur_y) == self.store and not has_pizza:
                self.state['pizza'] = True
                reward = rewards['pickup']['pos']
            else:
                reward = rewards['pickup']['neg']
        elif action == 'dropoff':
            if (cur_x, cur_y) == self.goal and has_pizza:
                self.state['pizza'] = False
                done = True
                reward = rewards['dropoff']['pos']
            else:
                reward = rewards['dropoff']['neg']

        return {'reward': reward,
                'done': done
                }

    def is_collision(self, action):
        collision_obs = 0  # obstacle necessary for a collision
        cur_x, cur_y = self.state['x'], self.state['y']

        if action == 'left':
            collision_obs = ((cur_x, cur_y), 'vert')
        elif action == 'right':
            collision_obs = ((cur_x + 1, cur_y), 'vert')
        elif action == 'up':
            collision_obs = ((cur_x, cur_y), 'horiz')
        elif action == 'down':
            collision_obs = ((cur_x, cur_y + 1), 'horiz')

        for obs in self.obstacles:
            if obs == collision_obs:
                return True
        return False


# driver code

# rewards
rewards = {
    'pickup': {'pos': 10, 'neg': -10},
    'dropoff': {'pos': 10, 'neg': -10},
    'time': -1
}

# obstacles
obstacles = {((1, 0), 'vert'),
             ((1, 1), 'vert'),
             ((1, 2), 'horiz')
             }

# homes
homes = [(0, 1),
         (3, 2),
         (4, 3)
         ]

# store
store = (2, 2)

env = Environment(5, rewards, obstacles, homes, store)

done = False
epochs = penalties = 0
while not done:
    action = randrange(6)
    result = env.step(Environment.actions[action])
    if result['reward'] == -10:
        penalties += 1
    done = result['done']
    epochs += 1

print("Time steps taken: {}".format(epochs))
print("Penalties incurred: {}".format(penalties))
