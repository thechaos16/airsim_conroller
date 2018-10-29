
import argparse

import airsim
import numpy as np


def create_client(agent_type=''):
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    return client


def destroy_client(client):
    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)


def get_state(client):
    # TODO: get type of client
    return client.getMultirotorState()


def start_client(client):
    # TODO: get type of client
    client.takeoffAsync().join()


def move_client(client, move_type, *args):
    if move_type == 'position':
        client.moveToPositionAsync(*args).join()
    elif move_type == 'velocity':
        client.moveByVelocityAsync(*args).join()
    else:
        raise NotImplementedError()


def get_images(client, image_type=''):
    responses = client.simGetImages([
        airsim.ImageRequest('0', airsim.ImageType.DepthVis),  # depth visualization image
        airsim.ImageRequest('1', airsim.ImageType.DepthPerspective, True),  # depth in perspective projection
        airsim.ImageRequest('1', airsim.ImageType.Scene),  # scene vision image in png format
        airsim.ImageRequest('1', airsim.ImageType.Scene, False, False)  # scene vision image in uncompressed RGBA array
    ])
    return responses


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--iteration', default=100, type=int)
    args.add_argument('--duration', default=5, type=int)
    args.add_argument('--move-type', default='velocity', type=str)
    config = args.parse_args()

    client = create_client()
    start_client(client)
    states = [get_state(client)]

    # NOTE: it looks like position is reversed coordination
    for _ in range(config.iteration):
        vec = [np.random.uniform(-2, 2,), np.random.uniform(-2, 2,), np.random.uniform(-2, 2,), config.duration]
        move_client(client, config.move_type, *vec)
        cur_state = get_state(client)
        states.append(cur_state)

    client.armDisarm(False)
    client.reset()
    destroy_client(client)
