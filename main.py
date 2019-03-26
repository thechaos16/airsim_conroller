
import argparse

from agents.random_walker import RandomWalker
from agents.vision_flyer import VisionFlyer
from client.drone_client import DroneClient


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--interval', default=1, type=int)
    args.add_argument('--move-type', default='velocity', type=str)
    config = args.parse_args()

    client = DroneClient(config.interval, root_path='./images')
    # agent = RandomWalker(client, config.move_type, (-2, 2))
    agent = VisionFlyer(client, config.move_type)
    agent.run(10)
    client.destroy()
