
import argparse

import numpy as np

from client.drone_client import DroneClient


def parse_state(state):
    gps = state.gps_location
    kinematic = state.kinematics_estimated
    time_stamp = state.timestamp
    return gps, kinematic, time_stamp


def detect_collision(collision):
    has_collide = collision.has_collided
    position = collision.position
    position = position.x_val, position.y_val, position.z_val
    return [has_collide, *position]


def get_position(kinematic):
    pos = kinematic.position
    return pos.x_val, pos.y_val, pos.z_val


def get_gps_info(gps_val):
    return gps_val.altitude, gps_val.latitude, gps_val.longitude


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--iteration', default=50, type=int)
    args.add_argument('--interval', default=1, type=int)
    args.add_argument('--move-type', default='velocity', type=str)
    config = args.parse_args()

    client = DroneClient(config.interval)
    client.start()
    states = [client.get_state()]

    # NOTE: it looks like position is reversed coordination
    for _ in range(config.iteration):
        vec = [np.random.uniform(-2, 2,), np.random.uniform(-2, 2,), np.random.uniform(-2, 2,)]
        client.move('velocity', *vec)
        cur_state = client.get_state()
        collision = client.get_collision_info()
        gps, kinematic, time_stamp = parse_state(cur_state)
        collide, x, y, z = detect_collision(collision)
        if collide:
            print('Collision!!!!')
        states.append(cur_state)

    client.destroy()
