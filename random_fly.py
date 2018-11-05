
import argparse

import numpy as np

from airsim_client import AirsimClient


def parse_state(state):
    collision = state.collision
    gps = state.gps_location
    kinematic = state.kinematics_estimated
    time_stamp = state.timestamp
    return collision, gps, kinematic, time_stamp


def detect_collision(state):
    collision, _, _, _ = parse_state(state)
    has_collide = collision.has_collided
    position = collision.position
    x, y, z = position.x_val, position.y_val, position.z_val
    return has_collide, x, y, z


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--iteration', default=50, type=int)
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
        collide, x, y, z = detect_collision(cur_state)
        if collide:
            print('Collision!!!!')
        states.append(cur_state)

    client.destroy()
