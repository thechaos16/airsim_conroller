
import argparse

import numpy as np

from airsim_client import AirsimClient


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--iteration', default=100, type=int)
    args.add_argument('--interval', default=5, type=int)
    args.add_argument('--move-type', default='velocity', type=str)
    config = args.parse_args()

    client = AirsimClient('drone', config.interval)
    client.start()
    states = [client.get_state()]

    # NOTE: it looks like position is reversed coordination
    for _ in range(config.iteration):
        vec = [np.random.uniform(-2, 2,), np.random.uniform(-2, 2,), np.random.uniform(-2, 2,)]
        client.move('velocity', *vec)
        cur_state = client.get_state()
        states.append(cur_state)

    client.destroy()
