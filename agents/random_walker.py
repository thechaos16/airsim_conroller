
import numpy as np

from agents.agent import Agent


class RandomWalker(Agent):
    def __init__(self, client, move_type, random_range):
        super(RandomWalker, self).__init__(client, move_type)
        self.client.start()
        self.random_range = random_range

    def get_state(self):
        return self.client.get_state()

    def act(self):
        target_vel = [
            np.random.uniform(*self.random_range,),
            np.random.uniform(*self.random_range,),
            np.random.uniform(*self.random_range,)
        ]
        self.client.move(self.move_type, *target_vel)

    def run(self, loop_cnt=100):
        for _ in range(loop_cnt):
            cur_state = self.get_state()
            self.act()
            print(cur_state)
